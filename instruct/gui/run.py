from instruct.instruct import Instruct
from instruct.sample import generate_sample_values
from instruct.data_entry import DataEntry
import yaml
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
import os
import time


from instruct.gui.widgets.layout import InstructLayout

console = Console()

def launch_gui(filepath, input=None, output=None, temperature=0, max_tokens=200, model=None, ask_feedback=False, interactivity=True):
    try:
        # run the GUI
        start_time = time.time()

        if input:
            with open(input, "r") as f:
                values = yaml.load(f, Loader=yaml.FullLoader)
        else:
            values = generate_sample_values(os.path.abspath(filepath), console=console)
            if values:
                console.log(f"Generated input: [dim]{values}[/dim]")

        instruct = Instruct(filepath, forced_model=model, **values)
        result = instruct.run(temperature=temperature, max_tokens=max_tokens)


        app = InstructLayout(content=result, model=instruct.matching_model.name, max_tokens=str(max_tokens), temperature=str(temperature))
        app.run()

    except Exception as e:
        console.log(f"[bold red]Error running {filepath} > {e}[/bold red]")