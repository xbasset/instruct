from src.pt import PT
import logging
import os
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
from rich.progress import track
import time
import yaml

console = Console()

# retrieve the content of each file in the example/data/rephrase folder
examples = []
list_files = os.listdir("examples/data/rephrase")
for file in list_files:
    with open(f"examples/data/rephrase/{file}", "r") as f:
        examples.append(f.read())


def run_rephrase(context: str, sentence: str, instructions: str, verbose: bool = False, model: str = None):
    
    try:
        pt = PT("examples/instructions/rephrase.pt", context=context,
            sentence=sentence, instructions=instructions, forced_model=model)

        rephrase = pt.run(temperature=0.0, max_tokens=200)

        
        if verbose:
            console.print(Text(f"Example:", style="bold blue"))
            console.print(Text(f"Context: {context}", style="dim blue"))
            console.print(Text(f"Sentence: {sentence}", style="dim blue"))
            console.print(Text(f"Instructions: {instructions}", style="dim blue"))
            if rephrase:
                console.print(Markdown(f"# Rephrase"))
                console.print(Markdown(f"```markdown\n{rephrase}\n```"))
            # print a horizontal separator using Rich
            console.print(Text("—"*50, style="dim"))
        return rephrase
    except Exception as e:
        print(f"Error running rephrase > {e}")
        return None
    

if __name__ == "__main__":
    
    # print a progressbar using Rich
    console.print(Text("Rephrase Eval", style="bold blue"))
    console.print(Text("—"*50, style="dim"))
    
    model = "mistral"
    iterations = 1
    success = 0
    # eval the last example `iterations` times
    for i in track(range(iterations), description=f"Evaluating meeting_recap.pt/{model} with missing date information"):
        for example in examples:
            example_values = yaml.load(example.strip(), Loader=yaml.FullLoader)
            result = run_rephrase(example_values["context"], example_values["sentence"], example_values["instructions"], verbose=True, model=model)
        success += 1
    console.print(f"Success rate: {success}/{iterations} ({success/iterations*100:.2f}%)")
    # for example in examples:
    #     run_meeting_recap(example, verbose=True)