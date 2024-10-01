import jinja2
import re

from instruct.llm_engine.model import Model
import logging
from typing import List

from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text

logging.basicConfig(level=logging.ERROR)

console = Console()


class Instruct:
    """
    The Instruct class is in charge of all the operations of the `instruct` principles.
    See the Instruct(`.instruct`) documentation for more details.

    Attributes:
        filepath (str): The filepath of the Instruct file.
        shebangs (list): A list of shebangs found in the Instruct file.
        template (jinja2.Template): The Jinja2 template object representing the Instruct file.
        models (list): Returns a list of model names extracted from the shebangs.
        tags (list): Returns a list of tags extracted from the template.
        template_values (list): Returns a list of jinja2 values extracted from the template.
        prompt (str): Returns the rendered prompt using the provided keyword arguments.

    Methods:
        _parse_file(): Parses the Instruct file and extracts shebangs and template.
        _perform_templating(**kwargs): Performs templating using the provided keyword arguments.
    """

    def __init__(self, filepath:str, forced_model=None, **kwargs):
        self.filepath = filepath

        try:
            from instruct.llm_engine.providers.model_loader import ModelLoader

            self.available_models : List[Model]= ModelLoader().models
            # console.print(f"[dim]available models: {self.available_models}[/dim]")
        except Exception as e:
            self.available_models = None
            raise Exception(f"Error loading available models: {e}")
        try:
            if forced_model is not None and self.available_models is not None:
                console.print(f"forced model: {forced_model}")
                for model in self.available_models:
                    if model.name == forced_model:
                        self.forced_model: Model = model
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

            self.available_models = ModelLoader().models
            # console.print(f"[dim]available models: {self.available_models}[/dim]")
            self.models = [d["model"] for d in self.shebangs]
        except Exception as e:
            raise Exception(f"Error initializing Instruct: {e}")

    @property
    def tags(self):
        """
        Extracts tags from the template.
        Tags are in the format: <tag_name>

        Returns:
            list: A list of tags extracted from the template.
        """
        return re.findall(r"(<[^>]*>)", self.raw_template)

    @property
    def template_values(self):
        """
        Extracts jinja2 values from the template.
        Jinja2 values are in the format: {{ value }}

        Returns:
            list: A list of jinja2 values extracted from the template.
        """
        return list(set(re.findall(r"{{([^}]*)}}", self.raw_template)))

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
                f"Prompt template resolved with forced_model: {self.forced_model.name}"
            )
            return self._perform_templating(**self.kwargs, model=self.forced_model)
        elif self.matching_model is not None:
            return self._perform_templating(
                **self.kwargs, model=self.matching_model.name
            )
        else:
            return self._perform_templating(**self.kwargs)

    @property
    def matching_model(self) -> Model:
        # return the first available model in the config file matching with the shebangs
        try:
            selected_model = None
            for model in self.models:
                for available_model in self.available_models:
                    if available_model.name == model:
                        selected_model = available_model
                        break

                if selected_model is not None:
                    break
            return selected_model
        except Exception as e:
            logging.error(f"Error finding matching model: {e}")
            return None

    def _parse_file(self):
        """
        Parses the Instruct file and extracts shebangs and template.
        """
        try:
            with open(self.filepath, "r") as file:
                lines = file.readlines()
                i = 0
                # find all the shebangs and get their values
                while lines[i].startswith("#!"):
                    shebang = lines[i].strip()
                    match = re.search(r"#!\s*([^/]*)/?([^/]*)?", shebang)
                    if match is not None:
                        model, version = match.groups()
                        self.shebangs.append(
                            {
                                "model": model,
                                "version": version if version else "latest",
                            }
                        )
                    else:
                        raise ValueError(
                            f"Invalid shebang: {shebang}\nFormat: #! model(/version)"
                        )
                    i += 1
                # find the first non empty line after shebangs
                while not lines[i].strip():
                    i += 1
                # remove all the empty lines at the end of the file
                while not lines[-1].strip():
                    lines.pop()

                self.raw_template = "".join(lines[i:])
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
        # if one of the args is of type Instruct, call its prompt method
        for k, v in kwargs.items():
            if isinstance(v, Instruct):
                kwargs[k] = v.prompt
                # also retrieve the models from the Instruct and choose the common model with the current Instruct
                self.models = list(set(self.models).intersection(v.models))

        try:
            return self.template.render(**kwargs)
        except Exception as e:
            logging.error(f"Error performing templating: {e}")
            logging.error(
                f"Check that you passed all the template values: {self.template_values}"
            )
            return None

    def __str__(self):
        """
        Returns a string representation of the Instruct object.

        Returns:
            str: A string representation of the Instruct object.
        """
        return f"Instruct: {self.filepath}"

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
                    f"Running prompt with forced model: {self.forced_model.name}"
                )
                return self.forced_model.interpret(self, **kwargs)[0]

            elif self.matching_model is not None:
                logging.info(f"run with args: {kwargs}")
                return self.matching_model.interpret(self, **kwargs)[0]
            else:
                raise Exception(
                    f"""
{self} > No matching provider <> model found:
providers: {self.available_models}
Instruct's compatibility list: {self.models}
To fix the problem:
1. Check the providers in the ~/.instruct/models.yaml file.
2. Check the Instruct file's shebangs for compatibility with the providers."""
                )

        except Exception as e:
            logging.error(f"Error running Instruct: {self} > {e}")
            return None
