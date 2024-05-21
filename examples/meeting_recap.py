from src.pt import PT
import logging
import os
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
from rich.progress import track
import time

console = Console()

# retrieve the content of each file in the example/data/meeting_recap folder
examples = []
list_files = os.listdir("examples/data/meeting_recap")
for file in list_files:
    with open(f"examples/data/meeting_recap/{file}", "r") as f:
        examples.append(f.read())


def run_meeting_recap(notes: str, verbose: bool = True):
    pt = PT("examples/instructions/meeting_recap.pt",
            notes=notes)
    meeting_recap_run = pt.run(temperature=0.0, max_tokens=1000)
    
    # meeting_recap.pt run output can be either <meeting_recap> tag or <question_to_ask> tag
    # As the models tend to talk more, we parse the output to extract only the tags
    try:
        meeting_recap, question_to_ask, scratchpad = None, None, None

        # Now, we can implement logic to the program
        if "<meeting_recap>" in meeting_recap_run:
            meeting_recap = meeting_recap_run.split("<meeting_recap>")[1].split("</meeting_recap>")[0]
        if "<question_to_ask>" in meeting_recap_run:
            question_to_ask = meeting_recap_run.split("<question_to_ask>")[1].split("</question_to_ask>")[0]
        if "<scratchpad>" in meeting_recap_run:
            scratchpad = meeting_recap_run.split("<scratchpad>")[1].split("</scratchpad>")[0]


        if verbose:
            console.print(Text(f"Example: {notes}", style="bold blue"))
            if meeting_recap:
                console.print(Markdown(f"# Meeting Recap"))
                console.print(Markdown(f"```markdown\n{meeting_recap}\n```"))

            if question_to_ask:
                console.print(Text(f"Question to Ask: {question_to_ask}", style="bold green"))

            if scratchpad:
                console.print(Text(f"Scratchpad: {scratchpad}", style="dim" ))
            # print a horizontal separator using Rich
            console.print(Text("—"*50, style="dim"))
            console.print(Text(meeting_recap_run, style="dim blue"))
        return(meeting_recap, question_to_ask, scratchpad)
        
        
    except Exception as e:
        print(f"Error parsing the output: {e}")
        print(meeting_recap_run)

if __name__ == "__main__":
    
    # print a progressbar using Rich
    console.print(Text("Meeting Recap Examples", style="bold blue"))
    console.print(Text("—"*50, style="dim"))
    
    
    iterations = 10
    success = 0
    # eval the last example `iterations` times
    for i in track(range(iterations), description="Evaluating meeting_recap.pt/mistral with missing date information"):
        meeting_recap, question_to_ask, scratchpad = run_meeting_recap(examples[-1], verbose=False)
        if question_to_ask and not meeting_recap:
            success += 1
    console.print(f"Success rate: {success}/{iterations} ({success/iterations*100:.2f}%)")
    # for example in examples:
    #     run_meeting_recap(example, verbose=True)