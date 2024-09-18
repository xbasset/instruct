import logging
import typer
from rich.traceback import install
from rich.logging import RichHandler
from rich import print

# Setup logging and install Rich traceback for beautiful error reporting
logging.basicConfig(
    level="ERROR",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
install()

app = typer.Typer()

@app.command()
def run(
    file: str,
    input: str = typer.Option(None, help="Input file"),
    output: str = typer.Option(None, help="Output file"),
    temperature: float = typer.Option(0.7, help="Temperature value for the model"),
    max_tokens: int = typer.Option(1000, help="Maximum number of tokens"),
    feedback: bool = typer.Option(True, help="Whether to ask for feedback"),
    model: str = typer.Option(None, help="Model to use"),
    interactivity: bool = typer.Option(True, help="Enable interactivity")

):
    from instruct.run import run as run_instruct
    run_instruct(
        file, 
        input=input, 
        output=output, 
        temperature=temperature, 
        max_tokens=max_tokens, 
        model=model, 
        ask_feedback=feedback,
        interactivity=interactivity

        
    )

@app.command()
def sample(
    file: str,
    output: str = typer.Option(None, help="Output file"),
    model: str = typer.Option(None, help="Model to use")
):
    from instruct.sample import generate_sample_values, write_output
    if output:
        values = generate_sample_values(file, write_to_file=output, model=model)
        print(values)
    else:
        values = generate_sample_values(file, model=model)
        print(values)

def cli():
    app()

if __name__ == "__main__":
    app()
