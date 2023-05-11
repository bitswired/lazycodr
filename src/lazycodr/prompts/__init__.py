from pathlib import Path

import jinja2


# Function to load templates from the templates folder
def load_template(template_name: str):
    """Load a template from the templates folder"""

    # Get the path relative to the current file
    templates_path = Path(__file__).parent.absolute() / "templates"

    templateLoader = jinja2.FileSystemLoader(searchpath=templates_path)
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(template_name)
    return template
