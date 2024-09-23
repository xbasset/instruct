from instruct.instruct import Instruct
from instruct.sample import generate_sample_values
from instruct.data_entry import DataEntry
import yaml
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
import os


from instruct.gui.widgets.layout import InstructLayout

console = Console()

def run_gui(filepath, input=None, output=None, temperature=0, max_tokens=200, model=None, ask_feedback=False, interactivity=True):
    try:

        if input:
            with open(input, "r") as f:
                input = yaml.load(f, Loader=yaml.FullLoader)
        else:
            values = generate_sample_values(os.path.abspath(filepath), console=console)
            if values:
                console.log(f"Generated input: [dim]{values}[/dim]")

        

        app = InstructLayout(instruct_file=filepath, input=input, max_tokens=max_tokens, temperature=temperature, forced_model=model, **values)
        app.run()

    except Exception as e:
        console.log(f"[bold red]Error running {filepath} > {e}[/bold red]")