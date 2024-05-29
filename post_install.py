from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown

console = Console()

def create_models_yaml():
    instruct_dir = Path.home() / ".instruct"
    models_yaml = instruct_dir / "models.yaml"

    # Create the directory if it doesn't exist
    instruct_dir.mkdir(parents=True, exist_ok=True)

    # Create the file if it doesn't exist
    if not models_yaml.exists():
        # read the models-example-exhaustive.yaml file and write it to the models.yaml file
        models_example_exhaustive = Path(__file__).parent / "models-example-exhaustive.yaml"
        with open(models_example_exhaustive, "r") as f:
            models_yaml_content = f.read()
        with open(models_yaml, "w") as f:
            f.write(models_yaml_content)

    
        console.print(Markdown(f"[{models_yaml}]({models_yaml}) created with default configuration file."))
        console.print(Markdown(f"Update the configuration to start using the `instruct` CLI."))

# Call the function
create_models_yaml()
