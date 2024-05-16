# cli execution
import argparse
import logging
from rich.traceback import install
from rich.logging import RichHandler
from rich import print

logging.basicConfig(
    level="ERROR",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

# Install Rich traceback globally to handle exceptions beautifully
install()

def check(pt_filepath):
    from pt import PT
    pt = PT(pt_filepath)

    # Check if the template_values are available


def cli():
    # Example of command:
    # pt run hello_world.pt

    # Possible commands:
    # - run: read the file, parse it, load the model API and run the prompt
    # - sample: build a sample prompt with generated variables automatically extracted from the prompt template and display it

    parser = argparse.ArgumentParser(
        description="Prompt Templating for Querying Large Language Models")
    subparsers = parser.add_subparsers(dest="command")
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("file", type=str)
    run_parser.add_argument("--input", type=str)
    run_parser.add_argument("--output", type=str)
    run_parser.add_argument("--temperature", type=float, default=0.0)
    run_parser.add_argument("--max_tokens", type=int, default=200)
    run_parser.add_argument("--model", type=str)
    sample_parser = subparsers.add_parser("sample")
    sample_parser.add_argument("file", type=str)
    sample_parser.add_argument("--output", type=str)
    sample_parser.add_argument("--model", type=str)
    args = parser.parse_args()

    if args.command == "run":
        from src.run import run
        run(args.file, input=args.input if args.input else None, output=args.output if args.output else None , temperature=args.temperature, max_tokens=args.max_tokens, model=args.model)

    elif args.command == "sample":
        if args.output:
            from src.generate_sample_values import generate_sample_values, write_output
            values = generate_sample_values(
                args.file, write_to_file=args.output, model=args.model)
            print(values)
        else:
            from src.generate_sample_values import generate_sample_values
            values = generate_sample_values(args.file, model=args.model)
            print(values)
            
    else:
        parser.print_help()


if __name__ == "__main__":
    cli()
