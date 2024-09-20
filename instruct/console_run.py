from instruct.instruct import Instruct
from instruct.sample import generate_sample_values
from instruct.data_entry import DataEntry
import yaml
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
import os
import time

console = Console()

def run(filepath, input=None, output=None, temperature=0, max_tokens=200, model=None, ask_feedback=False, interactivity=True):
    try:
        console.log(f"Running: [bold green]{filepath}[/bold green]")
        start_time = time.time()

        if input:
            console.log(f"Input file: [bold]{input}[/bold]")
            with open(input, "r") as f:
                values = yaml.load(f, Loader=yaml.FullLoader)
        else:
            values = generate_sample_values(os.path.abspath(filepath), console=console)
            if values:
                console.log(f"Generated input: [dim]{values}[/dim]")

        instruct = Instruct(filepath, forced_model=model, **values)
        console.log(f"[dim blue]Now running with: [/dim blue][bold green]{instruct.matching_model.name}[/bold green][dim blue] with Temp.: {temperature}, {max_tokens} tokens max[/dim blue]")
        result = instruct.run(temperature=temperature, max_tokens=max_tokens)

        console.print(Markdown(f"# Result with **{instruct.matching_model.name}** model:"))
        console.print(Markdown(f"```markdown\n{result}\n```"))

        if output and result:
            with open(output, "w") as f:
                f.write(result)
            console.print(f"Output written to [bold]{output}[/bold]")

        performance_text = Text(f"Total: {time.time() - start_time:.2f}s", style="italic dim")
        console.log(performance_text)

        if not interactivity:
            return
        feedback = console.input("Feedback (press Enter if satisfied): ") if ask_feedback else None
        feedback = feedback or "Default feedback: Satisfied with the result."

        DataEntry(filepath, query=instruct.prompt, response=result, evaluation=feedback, model=instruct.matching_model.name).save()

    except Exception as e:
        console.log(f"[bold red]Error running {filepath} > {e}[/bold red]")