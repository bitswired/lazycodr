from pathlib import Path

from langchain.prompts import PromptTemplate


def load_template(name):
    path = Path(__file__).parent.absolute() / "templates" / f"{name}.prompt"
    template = path.open().read()
    return PromptTemplate.from_template(template)
