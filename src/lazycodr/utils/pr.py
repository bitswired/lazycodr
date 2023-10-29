from operator import itemgetter

import httpx
from github import Github
from langchain.callbacks.manager import trace_as_chain_group
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.text_splitter import TokenTextSplitter

from lazycodr.constants import (
    PR_REFINE_INIT_TEMPLATE_NAME,
    PR_REFINE_LOOP_TEMPLATE_NAME,
)
from lazycodr.prompts import load_template

from .credentials import use_credentials


@use_credentials
def get_pr_diff(credentials, repo_name, pr_number):
    g = Github(credentials["github_token"])
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    # Download the pr diff and store in a string variable, follow redirects
    with httpx.Client(follow_redirects=True) as client:
        response = client.get(pr.diff_url)
    return response.text


@use_credentials
def generate_pr(credentials, pr_diff: str, pr_template: str):
    refine_init_prompt = load_template(PR_REFINE_INIT_TEMPLATE_NAME).partial(
        pr_template=pr_template,
    )
    refine_loop_prompt = load_template(PR_REFINE_LOOP_TEMPLATE_NAME).partial(
        pr_template=pr_template,
    )

    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=credentials["openai_api_key"],
        model_name="gpt-3.5-turbo-16k",
        request_timeout=120,
    )

    refine_init_chain = (
        refine_init_prompt.partial(text=pr_diff) | llm | StrOutputParser()
    )

    refine_loop_chain = (
        {
            "existing_answer": itemgetter("prev_response"),
            "text": lambda x: x["doc"].page_content,
        }
        | refine_loop_prompt
        | llm
        | StrOutputParser()
    )

    def refine_loop(docs):
        with trace_as_chain_group("refine loop", inputs={"input": docs}) as manager:
            res = refine_init_chain.invoke(
                docs[0],
                config={"callbacks": manager, "run_name": "initial"},
            )
            for i, doc in enumerate(docs[1:]):
                res = refine_loop_chain.invoke(
                    {"prev_response": res, "doc": doc},
                    config={"callbacks": manager, "run_name": f"refine {i}"},
                )
            manager.on_chain_end({"output": res})
        return res

    text_splitter = TokenTextSplitter(chunk_size=4000, chunk_overlap=200)
    docs = text_splitter.create_documents([pr_diff])

    return refine_loop(docs)
