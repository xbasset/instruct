## ./python_content.py

```python
import os
import fnmatch

def load_gitignore_patterns(gitignore_path):
    with open(gitignore_path, 'r') as file:
        patterns = [line.strip() for line in file if line.strip() and not line.startswith('#')]
    return patterns

def is_ignored(path, patterns):
    for pattern in patterns:
        if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(path, os.path.join('**', pattern)):
            return True
    return False

def write_markdown(output_file, root_dir, gitignore_patterns):
    with open(output_file, 'w') as markdown_file:
        for root, dirs, files in os.walk(root_dir):
            # Create relative path from root directory for pattern matching
            rel_root = os.path.relpath(root, root_dir)
            # Filter out directories to be ignored
            dirs[:] = [d for d in dirs if not is_ignored(os.path.join(rel_root, d), gitignore_patterns)]

            for file in files:
                rel_file = os.path.join(rel_root, file)
                if file.endswith('.py') and not is_ignored(rel_file, gitignore_patterns):
                    file_path = os.path.join(root, file)
                    markdown_file.write(f'## {file_path}\n\n')
                    try:
                        with open(file_path, 'r', errors='ignore') as py_file:
                            content = py_file.read()
                            markdown_file.write(f'```python\n{content}\n```\n\n')
                    except Exception as e:
                        markdown_file.write(f'Error reading file {file_path}: {e}\n\n')

def main():
    root_directory = '.'  # Change this to the directory you want to start the tree from
    output_file = 'python_files.md'
    gitignore_path = os.path.join(root_directory, '.gitignore')

    gitignore_patterns = []
    if os.path.exists(gitignore_path):
        gitignore_patterns = load_gitignore_patterns(gitignore_path)

    write_markdown(output_file, root_directory, gitignore_patterns)

if __name__ == '__main__':
    main()

```

## ./setup.py

```python
from setuptools import setup, find_packages
from pathlib import Path
import pkg_resources

setup(
    name='instruct',
    version='0.1',
    packages=find_packages(),
    description="Craft, Run, Evaluate Instructions for Large Language Models",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    readme="README.md",
    python_requires=">=3.10",
    author="Xavier Basset",
    url="https://github.com/xbasset/instruct",
    license="MIT",
      entry_points={
        "console_scripts": ["instruct=main:cli",],
    },
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            Path(__file__).with_name("requirements.txt").open()
        )
    ],
    
)

```

## ./main.py

```python
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
    from instruct.pt import PT
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
        from instruct.run import run
        run(args.file, input=args.input if args.input else None, output=args.output if args.output else None , temperature=args.temperature, max_tokens=args.max_tokens, model=args.model)

    elif args.command == "sample":
        if args.output:
            from instruct.sample import generate_sample_values, write_output
            values = generate_sample_values(
                args.file, write_to_file=args.output, model=args.model)
            print(values)
        else:
            from instruct.sample import generate_sample_values
            values = generate_sample_values(args.file, model=args.model)
            print(values)
            
    else:
        parser.print_help()


if __name__ == "__main__":
    cli()

```

## ./examples/meeting_recap.py

```python
from instruct.pt import PT
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
```

## ./examples/translations.py

```python
from instruct.pt import PT
import logging

pt = PT("examples/instructions/translation.pt",
        text="Bonjour tout le monde !", language="english")


translation = pt.run(temperature=0.7, max_tokens=200)

print(translation)

```

## ./examples/rephrase.py

```python
from instruct.pt import PT
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
```

## ./src/run.py

```python
from instruct.pt import PT
from instruct.sample import generate_sample_values
import yaml
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text

import time

# Initialize a Rich console object
console = Console()


def run(filepath, input=None, output=None, temperature=0, max_tokens=200, model=None):
    try:
        console.print(
            f"Running: [bold green]{filepath}[/bold green]")

        start_time = time.time()

        # Load the input values from a file or generate sample values
        if input:
            console.print(f"Input file: [bold]{input}[/bold]")
            # Read values from the input file (assumed to be a YAML file)
            with open(input, "r") as f:
                values = yaml.load(f, Loader=yaml.FullLoader)
            # console.print(f"[italic]{values}[/italic]")
        else:
            # Generate sample values for the template
            console.log("No input file provided, generating sample values")
            values = generate_sample_values(filepath)
            console.print(f"Generated input: [dim]{values}[/dim]" if values else "")
        end_time_values = time.time()
        
        console.print(
            f"[dim]Temp.: {temperature}, {max_tokens} tokens max[/dim]"
        )
        
        # Run the prompt template with the given values
        pt = PT(filepath, forced_model=model, **values)
        console.print(f"[dim blue]Model: {pt.matching_model.name} / forced_model={model}[/dim blue]")
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
        console.print(performance_text)

    except Exception as e:
        console.print(f"[bold red]Error running {filepath} > {e}[/bold red]")
        return

```

## ./src/pt.py

```python
import jinja2
import re

from instruct.llm_engine.model import Model
import logging

logging.basicConfig(level=logging.ERROR)


class PT:
    """
    The PT class represents a Prompt Template.
    See the Prompt Template (PT) documentation for more details.

    Attributes:
        filepath (str): The filepath of the PT file.
        shebangs (list): A list of shebangs found in the PT file.
        template (jinja2.Template): The Jinja2 template object representing the PT file.
        models (list): Returns a list of model names extracted from the shebangs.
        tags (list): Returns a list of tags extracted from the template.
        template_values (list): Returns a list of jinja2 values extracted from the template.
        prompt (str): Returns the rendered prompt using the provided keyword arguments.

    Methods:
        _parse_file(): Parses the PT file and extracts shebangs and template.
        _perform_templating(**kwargs): Performs templating using the provided keyword arguments.
    """

    def __init__(self, filepath, forced_model=None, **kwargs):
        self.filepath = filepath

        try:
            from instruct.llm_engine.providers.model_loader import ModelLoader
            self.available_models, _ = ModelLoader().providers
        except Exception as e:
            logging.debug(
                f"{self.filepath} > available_models loading: {e}")
            self.available_models = None

        if forced_model is not None and self.available_models is not None:
            print(forced_model)
            for provider in self.available_models:
                if provider['model_name'] == forced_model:
                    self.forced_model: Model = provider['provider']
                    logging.info(f"Forced model: {forced_model}")
                    break
            if self.forced_model is None:
                logging.info(f"Forced model not found: {forced_model}")
        else:
            self.forced_model = None

        # store the other arguments for later use
        self.kwargs = kwargs
        self.shebangs = []
        self.template = None
        self.raw_template = None
        self._parse_file()

        from instruct.llm_engine.providers.model_loader import ModelLoader
        self.available_models = ModelLoader().providers
        self.models = [d['model_name'] for d in self.shebangs]
        

    @property
    def tags(self):
        """
        Extracts tags from the template.
        Tags are in the format: <tag_name>

        Returns:
            list: A list of tags extracted from the template.
        """
        return re.findall(r'(<[^>]*>)', self.raw_template)

    @property
    def template_values(self):
        """
        Extracts jinja2 values from the template.
        Jinja2 values are in the format: {{ value }}

        Returns:
            list: A list of jinja2 values extracted from the template.
        """
        return list(set(re.findall(r'{{([^}]*)}}', self.raw_template)))

    @property
    def prompt(self):
        """
        Returns the rendered prompt using the provided keyword arguments.

        Args:
            **kwargs: Keyword arguments to be used for templating.

        Returns:
            str: The rendered prompt.
        """

        if self.forced_model is not None:
            logging.info(
                f"Prompt template resolved with forced_model: {self.forced_model.name}")
            return self._perform_templating(**self.kwargs, model=self.forced_model)
        elif self.matching_model is not None:
            return self._perform_templating(**self.kwargs, model=self.matching_model.name)
        else:
            return self._perform_templating(**self.kwargs)

    @property
    def matching_model(self) -> Model:
        # return the first available model matching with the shebangs
        try:
            selected_model = None
            # logging.info(f"available models: {self.available_models}")
            for model in self.models:
                for provider in self.available_models:
                    # logging.info(f"Checking provider: {provider['model_name']}")
                    if provider['model_name'] == model:
                        selected_model = provider['provider']
                        break

                if selected_model is not None:
                    break

            return selected_model
        except Exception as e:
            logging.error(f"Error finding matching model: {e}")
            return None

    def _parse_file(self):
        """
        Parses the PT file and extracts shebangs and template.
        """
        try:
            with open(self.filepath, 'r') as file:
                lines = file.readlines()
                i = 0
                # find all the shebangs and get their values
                while lines[i].startswith("#!"):
                    shebang = lines[i].strip()
                    match = re.search(r'#!\s*([^/]*)/?([^/]*)?', shebang)
                    if match is not None:
                        model_name, version = match.groups()
                        self.shebangs.append({
                            'model_name': model_name,
                            'version': version if version else 'latest'
                        })
                    else:
                        raise ValueError(
                            f"Invalid shebang: {shebang}\nFormat: #! model_name(/version)")
                    i += 1
                # find the first non empty line after shebangs
                while not lines[i].strip():
                    i += 1
                # remove all the empty lines at the end of the file
                while not lines[-1].strip():
                    lines.pop()

                self.raw_template = ''.join(lines[i:])
                self.template = jinja2.Template(self.raw_template)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {self.filepath}")
        except Exception as e:
            raise Exception(f"Error parsing file: {self.filepath} - {e}")

    def _perform_templating(self, **kwargs):
        """
        Performs templating using the provided keyword arguments.

        Args:
            **kwargs: Keyword arguments to be used for templating.

        Returns:
            str: The rendered template.
        """
        # if one of the args is of type PT, call its prompt method
        for k, v in kwargs.items():
            if isinstance(v, PT):
                kwargs[k] = v.prompt
                # also retrieve the models from the PT and choose the common model with the current PT
                self.models = list(set(self.models).intersection(v.models))

        try:
            return self.template.render(**kwargs)
        except Exception as e:
            logging.error(f"Error performing templating: {e}")
            logging.error(
                f"Check that you passed all the template values: {self.template_values}")
            return None

    def __str__(self):
        """
        Returns a string representation of the PT object.

        Returns:
            str: A string representation of the PT object.
        """
        return f"PT: {self.filepath}"

    def run(self, **kwargs):
        """
        Run the prompt to the appropriate model.

        Returns:
            str: The result of the Model call.
        """
        try:
            # for each model in the shebangs, in order, check if there is a provider for it
            # if there is, call it with the prompt

            if self.forced_model is not None:
                logging.info(
                    f"Running prompt with forced model: {self.forced_model.name}")
                return self.forced_model.invoke_from_pt(self, **kwargs)[0]

            elif self.matching_model is not None:
                logging.info(f"run with args: {kwargs}")
                return self.matching_model.invoke_from_pt(self, **kwargs)[0]
            else:
                raise Exception(f"""
{self} > No matching provider <> model found:
providers: {self.available_models}
PT's compatibility list: {self.models}
To fix the problem:
1. Check the providers in the models.conf file.
2. Check the PT file's shebangs for compatibility with the providers.""")

        except Exception as e:
            logging.error(f"Error running PT: {self} > {e}")
            return None

```

## ./src/sample.py

```python
from instruct.pt import PT
import logging
import datetime
import yaml

def write_output(filepath, output):
    with open(filepath, "w") as f:
        f.write(output)

def generate_sample_values(filepath, write_to_file=False, model=None):
    try:
        
        pt = PT(filepath)
        template_values = pt.template_values
        
        if len(template_values) == 0:
            return {}

        print(f"Generating sample values for {filepath}", f" with {model}" if model else "")
        sample_values_generator = PT("src/instructions/generate_sample_values.pt", template=pt.raw_template, values=pt.template_values, forced_model=model)
        sample_values = sample_values_generator.run(temperature=0, max_tokens=1000)
        
        # parse the output to only keep the content of the "<output>"
        
        if write_to_file:
            try:
                # check if write_to_file is a valid filepath
                if write_to_file == True:
                    now = datetime.datetime.now()
                    output_filename = f"sample-{filepath.split('/')[-1].split('.')[0]}-{now.strftime('%Y-%m-%d.%H:%M:%S')}.txt"
                else:
                    output_filename = write_to_file
                    try:
                        with open(output_filename, "w") as f:
                            f.write("test")
                            f.truncate(0)
                    except:
                        raise ValueError(f"Invalid filepath: {output_filename}")
                    
                write_output(output_filename, sample_values)
                print(f"Sample values written to {output_filename}")
            except Exception as e:
                logging.error(f"Error writing sample values > {e}")

        # parse the sample values in a yaml file
        try:
            sample_values = yaml.load(sample_values.strip(), Loader=yaml.FullLoader)
        except Exception as e:
            logging.error(f"Error parsing sample values > 👀 possible cause: malformed sample values")
            # write sample values to a file
            write_output(f"sample-error-{filepath.split('/')[-1].split('.')[0]}.yaml", sample_values)
            logging.error(f"See raw sample values generation in `sample-error-{filepath.split('/')[-1].split('.')[0]}.yaml`")
            return None

        return sample_values
    
    except Exception as e:
        logging.error(f"Error generating sample values > 👀 possible cause: model to generate sample values not available in `models.yaml`\n {e}")
        return


    


```

## ./src/llm_engine/model.py

```python
from abc import ABC, abstractmethod
import json
import logging
import os

logging.basicConfig(level=logging.ERROR)


class Model(ABC):
    """
    Abstract base class for Model implementations.
    """

    @abstractmethod
    def __init__(self, model_conf):
        """
        Initializes the model object.

        Args:
            model_conf (dict): The configuration for the model.
        """
        pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @abstractmethod
    def invoke(self, messages, temperature, max_tokens):
        """
        Perform a Model chat completion.

        Args:
            messages (list): List of messages.
            temperature (float): Temperature parameter for generating responses.
            max_tokens (int): Maximum number of tokens in the generated response.

        Returns:
            None
        """
        pass

    @abstractmethod
    def invoke_from_pt(self, pt, temperature, max_tokens):
        """
        Perform a Model chat completion using the provided PT.

        Args:
            pt (PT): The PT object.
            temperature (float): Temperature parameter for generating responses.
            max_tokens (int): Maximum number of tokens in the generated response.

        Returns:
            None
        """
        pass

    @abstractmethod
    def chatCompletion(self, *args, **kwargs):
        """
        Abstract method that should be implemented to handle chat completions. The parameters for each subclass that
        implements this method may vary, hence the use of *args and **kwargs to accept any number of arguments.
        """
        pass

```

## ./src/llm_engine/providers/openai_llm.py

```python
from openai import OpenAI, AzureOpenAI, RateLimitError
from instruct.llm_engine.model import Model
import tiktoken
import uuid

import logging
from typing import List


import os

from instruct.pt import PT


class OpenAILLM(Model):

    def __init__(self, llm_conf):
        """
        :param api_key: API key to call openAI
        :param api_base: Endpoint to call openAI
        :param api_version: Version of the API to user
        :param model: Model to use (deployment_id for azure)
        :param api_type: 'azure' or 'openai'
        """
        try:
            self._name = llm_conf["model_name"]
            api_key = llm_conf["api_key"]
            api_base = llm_conf["api_base"] if "api_base" in llm_conf else None
            api_version = llm_conf["api_version"] if "api_version" in llm_conf else None
            api_type = llm_conf["api_type"] if "api_type" in llm_conf else "openai"
            self.deployment = llm_conf["deployment_id"] if "deployment_id" in llm_conf else None

            # user_id for openAI moderation
            self.user_id = uuid.uuid4()

            self.client = AzureOpenAI(
                api_version=api_version,
                azure_endpoint=api_base,
                azure_deployment=self.deployment,
                api_key=api_key
            ) if api_type == 'azure' else OpenAI(api_key=api_key)

            self.client_backup = None

            Model.__init__(
                self, llm_conf)
        except Exception as e:
            raise Exception(f"🔴 Error initializing OpenAILLM __init__  : {e}")

    def _handle_chat_completion_response(self, completion, stream, stream_callback):
        try:
            if stream:
                complete_text = ""
                finish_reason = None
                for stream_chunk in completion:
                    choice = stream_chunk.choices[0]
                    partial_token = choice.delta
                    finish_reason = choice.finish_reason
                    if partial_token.content:
                        complete_text += partial_token.content
                        if stream_callback is not None:
                            try:
                                flag_to_stop_streaming = stream_callback(
                                    complete_text)
                                if flag_to_stop_streaming:
                                    return None
                            except Exception as e:
                                logging.error(
                                    f"🔴 Error in streamCallback: {e}")

                response = complete_text
            else:
                response = completion.choices[0].message.content
                finish_reason = completion.choices[0].finish_reason

            return response, finish_reason
        except Exception as e:
            raise Exception(f"_handle_chat_completion_stream : {e}")

    def chatCompletion(self, messages, user_uuid, temperature, max_tokens, frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None,
                       n_additional_calls_if_finish_reason_is_length=0, assistant_response="", n_calls=0, use_backup_client=False, **kwargs):
        """
        OpenAI chat completion
        :param messages: List of messages composing the conversation, each message is a dict with keys "role" and "content"
        :param user_uuid: Compulsory for openAI to track harmful content. If a user tries to pass the openAI moderation, we will receive an email with this id and we can go back to him to remove his access.
        :param temperature: The higher the temperature, the crazier the text
        :param max_tokens: The maximum number of tokens to generate
        :param frequency_penalty: The higher the penalty, the less likely the model is to repeat itself
        :param presence_penalty: The higher the penalty, the less likely the model is to generate a response that is similar to the prompt
        :param stream: If True, will stream the completion
        :param stream_callback: If stream is True, will call this function with the completion as parameter
        :param n_additional_calls_if_finish_reason_is_length: If the finish reason is "length", will relaunch the function, instructing the assistant to continue its response
        :param assistant_response: Assistant response to add to the completion
        :param n_calls: Number of calls to the function
        :return: List of n generated messages
        """
        openai_client = self.client_backup if use_backup_client else self.client

        # if "json_format" in kwargs and kwargs["json_format"]:
        # set response_format={"type": "json_object"} in kwargs
        if "json_format" in kwargs and kwargs["json_format"]:
            kwargs.pop("json_format")
            kwargs["response_format"] = {"type": "json_object"}

        completion = openai_client.chat.completions.create(
            messages=messages,
            model=self.name,
            temperature=temperature,
            max_tokens=max_tokens,
            user=user_uuid,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stream=stream,
            **kwargs
        )

        response, finish_reason = self._handle_chat_completion_response(
            completion, stream, stream_callback)

        if finish_reason == "length" and n_calls < n_additional_calls_if_finish_reason_is_length:
            # recall the function with assistant_message + user_message
            messages = messages + [{'role': 'assistant', 'content': response},
                                   {'role': 'user', 'content': 'Continue'}]
            return self.chatCompletion(messages, user_uuid, temperature, max_tokens,
                                       frequency_penalty=frequency_penalty, presence_penalty=presence_penalty,
                                       stream=stream, stream_callback=stream_callback,
                                       assistant_response=assistant_response + " " + response,
                                       n_additional_calls_if_finish_reason_is_length=n_additional_calls_if_finish_reason_is_length,
                                       n_calls=n_calls + 1, **kwargs)
        # [] is a legacy from the previous version that could return several completions. Need complete refacto to remove.
        return [assistant_response + " " + response]

    def invoke_from_pt(self, pt: PT, temperature, max_tokens, frequency_penalty=0, presence_penalty=0,
                        stream=False, stream_callback=None, **kwargs):
        try:


            if self.name not in pt.models:
                logging.warning(
                    f"{pt} does not contain model: {self.name} in its dashbangs")
            messages = [{"role": "user", "content": pt.prompt}]
            responses = self.recursive_invoke(messages, temperature, max_tokens,
                                              frequency_penalty=frequency_penalty, presence_penalty=presence_penalty,
                                              stream=stream, stream_callback=stream_callback,
                                              n_additional_calls_if_finish_reason_is_length=0, **kwargs)
            return responses
        except Exception as e:
            raise Exception(
                f"🔴 Error in OpenAILLM invoke: {e} - model: {self.name}"
            )

    def invoke(self, messages: List, temperature, max_tokens,
               frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None, **kwargs):
        return self.recursive_invoke(messages, temperature, max_tokens,
                                     frequency_penalty=frequency_penalty, presence_penalty=presence_penalty,
                                     stream=stream, stream_callback=stream_callback,
                                     n_additional_calls_if_finish_reason_is_length=0, **kwargs)

    def _call_completion_with_rate_limit_management(self, messages, temperature, max_tokens, frequency_penalty, presence_penalty,
                                                    stream, stream_callback,
                                                    n_additional_calls_if_finish_reason_is_length, **kwargs):
        try:
            try:
                return self.chatCompletion(messages, str(self.user_id), temperature, max_tokens, frequency_penalty, presence_penalty, stream=stream,
                                           stream_callback=stream_callback,
                                           n_additional_calls_if_finish_reason_is_length=n_additional_calls_if_finish_reason_is_length,
                                           **kwargs)
            except RateLimitError:
                # try to use backup engine
                if self.client_backup:
                    return self.chatCompletion(messages, str(self.user_id), temperature, max_tokens, frequency_penalty, presence_penalty,
                                               stream=stream,
                                               stream_callback=stream_callback,
                                               use_backup_client=True, **kwargs)
                else:
                    raise Exception(
                        "Rate limit exceeded and no backup engine available")
        except Exception as e:
            raise Exception(
                f"_call_completion_with_rate_limit_management : {e}")

    def recursive_invoke(self, messages, temperature, max_tokens, frequency_penalty=0, presence_penalty=0,
                         stream=False, stream_callback=None,
                         n_additional_calls_if_finish_reason_is_length=0, **kwargs):
        try:

            responses = self._call_completion_with_rate_limit_management(messages, temperature, max_tokens,
                                                                         frequency_penalty, presence_penalty,
                                                                         stream, stream_callback,
                                                                         n_additional_calls_if_finish_reason_is_length,
                                                                         **kwargs)
            return responses
        except Exception as e:
            raise Exception(
                f"🔴 Error in OpenAILLM recursive_invoke() > {e} - model: {self.name}")

```

## ./src/llm_engine/providers/groq_llm.py

```python


import os
from instruct.llm_engine.model import Model
from instruct.pt import PT

import logging

from groq import Groq

class GroqLLM(Model):

    def __init__(self, groq_conf):

        try:
            self._name = groq_conf["model_name"]
            self.model = groq_conf.get(
                "model") if groq_conf.get("model") else None

            if self.model is None:
                raise Exception(
                    f"🔴 model not set in models conf: {groq_conf}")

            self.client = Groq(api_key=groq_conf["api_key"])

        except Exception as e:
            raise Exception(
                f"🔴 Error initializing GroqLLM __init__  : {e}")

    def chatCompletion(self, messages, temperature, max_tokens, n_responses=1,
                       frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None, json_format=False):
        try:
            # ensure if stream is true, n_responses = 1
            if stream and n_responses != 1:
                n_responses = 1
                logging.warning("n_responses must be 1 if stream is True")

            if stream:
                stream_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    stream=True,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                complete_text = ""
                for chunk in stream_response:
                    partial_token = chunk.choices[0].delta.content
                    complete_text += partial_token if partial_token else ""
                    if stream_callback is not None:
                        try:
                            stream_callback(complete_text)
                        except Exception as e:
                            logging.error(
                                f"🔴 Error in streamCallback : {e}")
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                    )

                complete_text = response.choices[0].message.content
            # [content.text for content in stream_response.choices]
            return [complete_text]

        except Exception as e:
            logging.error(f"Error in GroqLLM chat: {e}")

    def invoke(self, messages, temperature, max_tokens, n_responses=1,
               frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None, json_format=False):
        try:

            responses = self.chatCompletion(messages, temperature, max_tokens, n_responses=n_responses,
                                            frequency_penalty=frequency_penalty, presence_penalty=presence_penalty, stream=stream, stream_callback=stream_callback, json_format=json_format)

            return responses
        except Exception as e:
            raise Exception(
                f"🔴 Error in GroqLLM: {e} - model: {self.model}")

    def invoke_from_pt(self, pt: PT, temperature, max_tokens, n_responses=1,
                        frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None, json_format=False):
        try:

            if self.model not in pt.models:
                logging.warning(
                    f"{pt} does not contain model: {self.model} in its dashbangs")

            messages = [{"role": "user", "content": pt.prompt}]
            responses = self.invoke(messages, temperature, max_tokens, n_responses=n_responses,
                                    frequency_penalty=frequency_penalty, presence_penalty=presence_penalty, stream=stream, stream_callback=stream_callback, json_format=json_format)
            return responses
        except Exception as e:
            raise Exception(
                f"🔴 Error in GroqLLM: > {e} - model: {self.model}")

```

## ./src/llm_engine/providers/model_loader.py

```python
import configparser

from instruct.llm_engine.model import Model
from instruct.llm_engine.providers.openai_llm import OpenAILLM
from instruct.llm_engine.providers.mistralai_llm import MistralAILLM
from instruct.llm_engine.providers.ollama_llm import OllamaLLM
from instruct.llm_engine.providers.openai_vision_llm import OpenAIVisionLLM
from instruct.llm_engine.providers.groq_llm import GroqLLM

import logging
import os
import yaml

logging.basicConfig(level=logging.ERROR)


class ModelLoader:
    llm_conf_filename = "models.yaml"
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ModelLoader, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.providers = self._get_providers()

    def _get_providers(self):
        """
        Returns the list of available LLM providers in the models.yaml file

        """
        try:
            llm_providers_list = []
            
            with open(ModelLoader.llm_conf_filename, 'r') as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
            
            providers = config

            for provider_name, conf in providers.items():
                for model_name in conf:
                    llm = self._build_provider(
                        provider_name, model_name, conf)
                    provider_conf = {
                        "model_name": model_name,
                        "provider_name": provider_name,
                        "provider": llm,
                        "config": conf
                    }
                    llm_providers_list.append(provider_conf)

            return llm_providers_list

        except Exception as e:
            logging.error(
                f"🔴: ERROR: {ModelLoader.__subclasses__()[0].__name__} >> {e}")
            return []

    def _build_provider(self, provider_name, model_name, conf):
        """
        Build a provider object from the provider name and model name.
        """
        try:
            model = None
            provider_conf = conf[model_name]

            
            if provider_name == "openai":
                conf = {
                    "api_key": provider_conf["openai_api_key"],
                    "api_type": provider_name,
                    "model_name": model_name
                }
                model = OpenAILLM(conf)

            elif provider_name == "azure":
                conf = {
                    "api_key": provider_conf["api_key"],
                    "api_base": provider_conf["endpoint"], # for OpenAI models
                    "endpoint": provider_conf["endpoint"], # for Mistral models
                    "api_type": provider_name,
                    "api_version": provider_conf["api_version"],
                    "deployment_id": provider_conf["deployment_id"],
                    "model_name": model_name
                }
                if model_name in ["gpt4-turbo", "gpt-4-turbo", "gpt4-32k", "gpt-4o"]:
                    model = OpenAILLM(conf)
                elif model_name == "gpt4-vision":
                    model = OpenAIVisionLLM(conf)
                elif model_name == "mistral-large":
                    model = MistralAILLM(conf)

            elif provider_name == "mistral":
                conf = {
                    "api_key": provider_conf["api_key"],
                    "api_model": model_name,
                    "model_name": model_name
                }
                model = MistralAILLM(conf)

            elif provider_name == "ollama":
                conf = {
                    "endpoint": provider_conf["ollama_endpoint"],
                    "model": model_name,
                    "model_name": model_name
                }
                model = OllamaLLM(conf)
            
            elif provider_name == "groq":
                conf = {
                    "api_key": provider_conf["api_key"],
                    "model": model_name,
                    "model_name": model_name
                }
                model = GroqLLM(conf)

            if provider_name not in ["openai", "azure", "mistral", "ollama", "groq"]:
                logging.warning(
                    f"🔴: ERROR: ModelLoader _build_provider() >> in config file {ModelLoader.llm_conf_filename} provider: ** {provider_name} ** has not been implemented")

            return model
        except Exception as e:
            logging.error(f"🔴: ERROR: ModelLoader _build_provider() >> {e}")
            return None



    def _get_providers_by_model(self, model):
        """
        Return a list of providers that support the given model.
        The providers are encoded in the sections of the config file as the following format <provider>/<model>
        """
        conf_file = os.path.join(os.path.dirname(
            __file__), ModelLoader.llm_conf_filename)
        config = configparser.ConfigParser()
        config.read(conf_file)
        providers = []
        for section in config.sections():
            provider, model_name = section.split('/')
            if model_name == model:
                providers.append(provider)
        return providers

    def _get_all_models(self):
        """
        Return a list of all models in the config file.
        """
        conf_file = os.path.join(os.path.dirname(
            __file__), ModelLoader.llm_conf_filename)
        config = configparser.ConfigParser()
        config.read(conf_file)
        models = []
        for section in config.sections():
            provider, model_name = section.split('/')
            models.append(model_name)
        return set(models)

```

## ./src/llm_engine/providers/openai_vision_llm.py

```python
from openai import OpenAI, AzureOpenAI, RateLimitError
from instruct.llm_engine.model import Model
from instruct.llm_engine.providers.openai_llm import OpenAILLM
import tiktoken
import logging
from typing import List

from instruct.pt import PT


class OpenAIVisionLLM(OpenAILLM):

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    def __init__(self, llm_conf):
        super().__init__(llm_conf)

    @staticmethod
    def get_image_message_url_prefix(image_name):
        try:
            extension = image_name.split(".")[-1].lower()
            # check if extension is allowed
            if extension not in OpenAIVisionLLM.ALLOWED_EXTENSIONS:
                raise Exception(f"Image extension not allowed: {extension}")
            return 'data:image/' + extension
        except Exception as e:
            raise Exception(f"_get_image_message_url_prefix :: {e}")

    def recursive_invoke(self, messages, user_id, temperature, max_tokens, frequency_penalty, presence_penalty,
                         stream=False, stream_callback=None, user_task_execution_pk=None, task_name_for_system=None,
                         n_additional_calls_if_finish_reason_is_length=0, **kwargs):
        try:

            responses = self._call_completion_with_rate_limit_management(messages, self.user_id, temperature, max_tokens,
                                                                         frequency_penalty, presence_penalty,
                                                                         stream, stream_callback,
                                                                         n_additional_calls_if_finish_reason_is_length,
                                                                         **kwargs)

            return responses
        except Exception as e:
            raise Exception(
                f"🔴 Error in OpenAI recursive_invoke() > - model: {self.name}")

```

## ./src/llm_engine/providers/mistralai_llm.py

```python
from mistralai.models.chat_completion import ChatMessage
from mistralai.client import MistralClient
import logging
import os
from instruct.llm_engine.model import Model
from instruct.pt import PT

logging.basicConfig(level=logging.ERROR)


class MistralAILLM(Model):

    def __init__(self, mistral_conf):

        try:
            self._name = mistral_conf["model_name"]
            api_key = mistral_conf["api_key"]
            self.model = mistral_conf["api_model"]

            endpoint = mistral_conf.get("endpoint") if mistral_conf.get(
                "endpoint") else None
            api_type = "azure" if mistral_conf.get(
                "endpoint") else "la_plateforme"

            self.client = MistralClient(
                api_key=api_key,
                endpoint=endpoint if api_type == 'azure' else "https://api.mistral.ai",
            )

        except Exception as e:
            raise Exception(
                f"🔴 Error initializing MistralAILLM __init__  : {e}")

    def chatCompletion(self, messages, temperature, max_tokens, n_responses=1,
                       frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None, json_format=False):
        try:
            # ensure if stream is true, n_responses = 1
            if stream and n_responses != 1:
                n_responses = 1
                logging.warning("n_responses must be 1 if stream is True")

            # Convert messages into Mistral ChatMessages
            if len(messages) == 1:
                messages = [ChatMessage(
                    role='user', content=messages[0]['content'])]
            else:
                messages = [ChatMessage(
                    role=message['role'], content=message['content']) for message in messages]

            if stream:
                stream_response = self.client.chat_stream(
                    model=self.model, messages=messages, temperature=temperature, max_tokens=max_tokens)

                complete_text = ""
                for chunk in stream_response:
                    partial_token = chunk.choices[0].delta.content
                    complete_text += partial_token if partial_token else ""
                    if stream_callback is not None:
                        try:
                            stream_callback(complete_text)
                        except Exception as e:
                            logging.error(
                                f"🔴 Error in streamCallback : {e}")
            else:
                response = self.client.chat(
                    model=self.model, messages=messages, temperature=temperature, max_tokens=max_tokens)

                complete_text = response.choices[0].message.content
            # [content.text for content in stream_response.choices]
            return [complete_text]

        except Exception as e:
            logging.error(f"💨❌: Error in MistralAILLM: {e}")

    def invoke(self, messages, temperature, max_tokens, n_responses=1,
               frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None, json_format=False):
        try:

            responses = self.chatCompletion(messages, temperature, max_tokens, n_responses=n_responses,
                                            frequency_penalty=frequency_penalty, presence_penalty=presence_penalty, stream=stream, stream_callback=stream_callback, json_format=json_format)

            return responses
        except Exception as e:
            raise Exception(
                f"🔴 Error in MistralAILLM.invoke: {e} - model: {self.model}")

    def invoke_from_pt(self, pt: PT, temperature, max_tokens, n_responses=1,
                        frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None, json_format=False):
        try:

            if self.model not in pt.models:
                logging.warning(
                    f"{pt} does not contain model: {self.model} in its dashbangs")
            messages = [{"role": "user", "content": pt.prompt}]
            responses = self.invoke(messages, temperature, max_tokens, n_responses=n_responses,
                                    frequency_penalty=frequency_penalty, presence_penalty=presence_penalty, stream=stream, stream_callback=stream_callback, json_format=json_format)
            return responses
        except Exception as e:
            raise Exception(
                f"Error in Mistral AI chat : {e}")

```

## ./src/llm_engine/providers/ollama_llm.py

```python


import os
from instruct.llm_engine.model import Model
from instruct.pt import PT


from ollama import Client


class OllamaLLM(Model):

    def __init__(self, ollama_conf):

        try:
            self._name = ollama_conf["model_name"]
            self.model = ollama_conf.get(
                "model") if ollama_conf.get("model") else None
            self.endpoint = ollama_conf.get("endpoint") if ollama_conf.get(
                "endpoint") else None

            if self.endpoint is None or self.model is None:
                raise Exception(
                    f"🔴 model and endpoint not set in models conf: {ollama_conf}")

            self.client = Client(host=ollama_conf["endpoint"])

        except Exception as e:
            raise Exception(
                f"🔴 Error initializing OllamaLLM __init__  : {e}")

    def chatCompletion(self, messages, temperature, max_tokens, n_responses=1,
                       frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None, json_format=False):
        try:
            # ensure if stream is true, n_responses = 1
            if stream and n_responses != 1:
                n_responses = 1
                logging.warning("n_responses must be 1 if stream is True")

            if stream:

                stream_response = self.client.chat(
                    model=self.model,
                    messages=messages,
                    stream=True,
                )

                complete_text = ""
                for chunk in stream_response:
                    partial_token = chunk['message']['content']
                    complete_text += partial_token if partial_token else ""
                    if stream_callback is not None:
                        try:
                            stream_callback(complete_text)
                        except Exception as e:
                            logging.error(
                                f"🔴 Error in streamCallback : {e}")
            else:
                response = self.client.chat(
                    model=self.model, messages=messages)

                complete_text = response['message']['content']
            # [content.text for content in stream_response.choices]
            return [complete_text]

        except Exception as e:
            logging.error(f"Error in OllamaLLM chat: {e}")

    def invoke(self, messages, temperature, max_tokens, n_responses=1,
               frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None, json_format=False):
        try:

            responses = self.chatCompletion(messages, temperature, max_tokens, n_responses=n_responses,
                                            frequency_penalty=frequency_penalty, presence_penalty=presence_penalty, stream=stream, stream_callback=stream_callback, json_format=json_format)

            return responses
        except Exception as e:
            raise Exception(
                f"🔴 Error in OllamaAILLM: {e} - model: {self.model}")

    def invoke_from_pt(self, pt: PT, temperature, max_tokens, n_responses=1,
                        frequency_penalty=0, presence_penalty=0, stream=False, stream_callback=None, json_format=False):
        try:

            if self.model not in pt.models:
                logging.warning(
                    f"{pt} does not contain model: {self.model} in its dashbangs")

            messages = [{"role": "user", "content": pt.prompt}]
            responses = self.invoke(messages, temperature, max_tokens, n_responses=n_responses,
                                    frequency_penalty=frequency_penalty, presence_penalty=presence_penalty, stream=stream, stream_callback=stream_callback, json_format=json_format)
            return responses
        except Exception as e:
            raise Exception(
                f"🔴 Error in OllamaAILLM: > {e} - model: {self.model}")

```

