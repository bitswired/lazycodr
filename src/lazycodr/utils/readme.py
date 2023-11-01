import asyncio
import itertools as it
from pathlib import Path

import pathspec
import tiktoken
import typer
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.text_splitter import TokenTextSplitter
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, track
from rich.table import Table

from lazycodr.constants import (
    README_FILE_SUMMARY_GENERATE_TEMPLATE_NAME,
    README_FILE_SUMMARY_REFINE_INIT_TEMPLATE_NAME,
    README_FILE_SUMMARY_REFINE_LOOP_TEMPLATE_NAME,
)
from lazycodr.prompts import load_template

from .credentials import use_credentials


def tracked_files_generator(path: Path, user_ignore_patterns: list[str]):
    files = (x for x in path.relative_to(path).rglob("*"))

    gitignore_path = path / ".gitignore"
    ignore_patterns = []
    if gitignore_path.exists():
        ignore_patterns += gitignore_path.read_text().splitlines()
    ignore_patterns += user_ignore_patterns

    spec = pathspec.PathSpec.from_lines("gitwildmatch", ignore_patterns)

    for file_path in files:
        if not spec.match_file(file_path) and file_path.is_file():
            try:
                with file_path.open("r", encoding='utf"8') as f:
                    f.read()
                yield path / file_path
            except UnicodeDecodeError:
                continue


def batch_iterator(generator, batch_size):
    """Yield items from iterable in chunks of batch_size."""
    while True:
        chunk = list(it.islice(generator, batch_size))
        if not chunk:
            return None
        yield [str(x) + x.read_text() for x in chunk]


@use_credentials
def summarize_file(credentials, file_content: str):
    init_prompt = load_template(README_FILE_SUMMARY_REFINE_INIT_TEMPLATE_NAME)
    refine_prompt = load_template(README_FILE_SUMMARY_REFINE_LOOP_TEMPLATE_NAME)

    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=credentials["openai_api_key"],
        model_name="gpt-4",
        request_timeout=120,
    )

    text_splitter = TokenTextSplitter.from_tiktoken_encoder(
        chunk_size=6000,
        chunk_overlap=200,
    )
    split_docs = text_splitter.create_documents(texts=[file_content])

    chain = load_summarize_chain(
        llm=llm,
        chain_type="refine",
        question_prompt=init_prompt,
        refine_prompt=refine_prompt,
        return_intermediate_steps=True,
        input_key="input_documents",
        output_key="output_text",
    )

    return (
        {"input_documents": lambda _: split_docs} | chain | (lambda x: x["output_text"])
    )


def exec_batch(batch):
    async def f():
        tasks = [summarize_file(x).ainvoke("") for x in batch]
        return await asyncio.gather(*tasks)

    return asyncio.run(f())


def num_tokens_from_string(string: str, model: str) -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(string))


@use_credentials
def generate_readme(credentials, repo_path: str, user_ignore_patterns: list[str]):
    batch_size = 10
    tracked_files = tracked_files_generator(repo_path, user_ignore_patterns)
    batched_tracked_files = batch_iterator(tracked_files, batch_size)

    tokens = []
    total_tokens = 0
    for x in tracked_files_generator(repo_path, user_ignore_patterns):
        x.read_text()
        n = num_tokens_from_string(x.read_text(), "gpt-3.5-turbo-16k")
        tokens.append((x, n))
        total_tokens += n
    tokens.sort(key=lambda x: x[1], reverse=True)

    table = Table(title="Tokens Per File Matched")
    table.add_column("Path", justify="right", style="cyan", no_wrap=True)
    table.add_column("Tokens", style="magenta")
    table.add_row("TOTAL", str(total_tokens))
    for path, n_tokens in tokens:
        table.add_row(str(path), str(n_tokens))
    console = Console()
    console.print(table)

    message = (
        "LazyCodr will use AI to generate a sumary of each file matched aboved.\n"
        "Then it will combine all these summaries into a single context and use"
        "AI to generate the README.md"
    )
    typer.echo(message)
    typer.confirm("Proceed?", abort=True)

    summarized_files = []
    for batch in track(
        list(batched_tracked_files),
        description=f"Summarizing files (batch of {batch_size} parallelized) ...",
    ):
        res = exec_batch(batch)
        summarized_files += res

    context = "\n".join(summarized_files)

    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=credentials["openai_api_key"],
        model_name="gpt-4",
        request_timeout=120,
    )
    prompt = load_template(README_FILE_SUMMARY_GENERATE_TEMPLATE_NAME).format(
        context=context,
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Generating README.md ...", total=None)
        runnable = llm | StrOutputParser()
        return runnable.invoke(prompt)
