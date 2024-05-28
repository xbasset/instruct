# post_install.py
import os
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text

console = Console()

def create_models_yaml():
    instruct_dir = Path.home() / ".instruct"
    models_yaml = instruct_dir / "models.yaml"

    # Create the directory if it doesn't exist
    instruct_dir.mkdir(parents=True, exist_ok=True)

    # Create the file if it doesn't exist
    if not models_yaml.exists():
        with models_yaml.open("w") as file:
            file.write("""ollama:
  mistral:
    ollama_endpoint: "http://localhost:11434"
""")
        console.print(Markdown(f"Created defaut models.yaml at {models_yaml} with default `ollama` configuration."))
        console.print(f"Please update the configuration with your own API keys and endpoints. See the documentation for more details: https://github.com/xbasset/instruct")

# Call the function
create_models_yaml()
