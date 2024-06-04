from instruct.pt import PT
from instruct.sample import generate_sample_values
from instruct.data_entry import DataEntry
import yaml
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
import os

import time

# Initialize a Rich console object
console = Console()


def run(filepath, input=None, output=None, temperature=0, max_tokens=200, model=None, ask_feedback=False):
    try:
        console.log(
            f"Running: [bold green]{filepath}[/bold green]")

        start_time = time.time()

        # Load the input values from a file or generate sample values
        if input:
            console.log(f"Input file: [bold]{input}[/bold]")
            # Read values from the input file (assumed to be a YAML file)
            with open(input, "r") as f:
                values = yaml.load(f, Loader=yaml.FullLoader)
            # console.log(f"[italic]{values}[/italic]")
        else:
            # Generate sample values for the template
            absolute_path = os.path.abspath(filepath)
            values = generate_sample_values(absolute_path, console=console)
            if values:
                console.log(f"Generated input: [dim]{values}[/dim]")
        end_time_values = time.time()
        
        
        # Run the prompt template with the given values
        pt = PT(filepath, forced_model=model, **values)
        console.log(f"[dim blue]Now running with: [/dim blue][bold green]{pt.matching_model.name}[/bold green][dim blue] with Temp.: {temperature}, {max_tokens} tokens max[/dim blue]")
        result = pt.run(temperature=temperature, max_tokens=max_tokens)
        end_time_run = time.time()

        # Show the result
        console.print(
            Markdown(f"# Result with **{pt.matching_model.name}** model:"))
        console.print(Markdown(f"```markdown\n{result}\n```"))
        
        if output and result:
            with open(output, "w") as f:
                f.write(result)
            console.print(f"Output written to [bold]{output}[/bold]")

        performance_text = Text(
            f"Total: {end_time_run - start_time:.2f}s (Values: {end_time_values - start_time:.2f}s, Run:{end_time_run - end_time_values:.2f}s)", style="italic dim")
        console.log(performance_text)

        if ask_feedback:
            feedback = console.input("Feedback (press Enter if satisfied): ")
            if not feedback:
                feedback = "Default feedback: Satisfied with the result."
        else:
            feedback = None

        # Save the data entry
        data_entry = DataEntry(filepath, query=pt.prompt, response=result,
                               evaluation=feedback, model=pt.matching_model.name)
        data_entry.save()


    except Exception as e:
        console.log(f"[bold red]Error running {filepath} > {e}[/bold red]")
        return
