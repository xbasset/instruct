![instruct_logo](/assets/instruct_logo.png)

 # Instruct

Handcraft, Run, Evaluate Instructions for LLMs

`instruct` is a Python library designed for developers to craft rich instructions, execute them on various LLMs, and evaluate their robustness across different models.

## Table of Contents

- [Instruct](#instruct)
  - [Table of Contents](#table-of-contents)
  - [Why `instruct`](#why-instruct)
  - [Features](#features)
    - [1. Handcraft your instructions: VS Code developer worflow](#1-handcraft-your-instructions-vs-code-developer-worflow)
    - [2. Run \& Evaluate your instructions: Terminal UI](#2-run--evaluate-your-instructions-terminal-ui)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
  - [Usage](#usage)
    - [Creating Instructions](#creating-instructions)
    - [Use `.instruct` in your code](#use-instruct-in-your-code)
      - [Python code](#python-code)
      - [CLI](#cli)
    - [Evaluating Instructions](#evaluating-instructions)
  - [Configuration](#configuration)
  - [Examples](#examples)
  - [Contributing](#contributing)
    - [Developer commands](#developer-commands)
    - [TODO](#todo)
  - [License](#license)

## Why `instruct`

Large Language Models (LLMs) are **powerful statistical interpretation engines**.

Crafting effective prompts (instructions) for these models is crucial for obtaining accurate outputs. While advanced models like GPT-4o, Claude 3.5, Mistral large can handle poorly crafted instructions, smaller models (e.g., 7B or 12B parameters) struggle.

When you've got a brilliant idea that works great at scale on a giant model, you want to make it reliable and cost-effective. That's when you start thinking about using a smaller, maybe even local, model. But here's the catch: prompts are critical. A poorly crafted prompt can make a small model spit out garbage.

This is where `instruct` steps in. Instead of [hiding your prompts in a mess of code]((https://github.com/langchain-ai/langchain/blob/master/templates/hyde/hyde/prompts.py)), `instruct` lets you handcraft them in a dedicated workspace. 
- **Handcraft Instructions**: Move from unorganized strings to well-crafted `.instruct` files.
- **Evaluate on Multiple Models**: Test and refine instructions across various LLMs to find the best balance of accuracy, speed, and cost.

You can refine your instructions using techniques like few-shot examples, chain of thoughts, and tree of thoughts until they work even on smaller models. Treat your `.instruct` files as first-class citizens in your codebase, right next to your code.

 
## Features

### 1. Handcraft your instructions: VS Code developer worflow
- **Create Rich Instructions and run**: See the interpretation of your `.instruct` for quick iterations in no time with the [VS Code Extension](https://github.com/xbasset/vscode-instruct)

![Instruct VS Code Extension](/assets/instruct_demo_extension_0.1.gif)

### 2. Run & Evaluate your instructions: Terminal UI

Explore easily how different LLMs –local and API-based– with different configurations (temperature, max_tokens) behave to find the best (model,conf) combination that matches your requirements in terms of **accuracy**, **speed** and **cost**
- **CLI**: Execute instructions on different LLMs with easy configuration directly from your CLI

![CLI execution](/assets/instruct_demo_0.1.gif)


## Installation

To install `Instruct` Python package, use pip:

```bash
pip install instruct
```

For the VS Code extension, follow this guide:
https://github.com/xbasset/vscode-instruct

## Quick Start

Here's a quick example to get you started with Instruct:

1. **Create an Instruction File** (`quickstart.instruct`):

```plaintext
#! gpt-3.5-turbo
#! gpt-4

Hello, my name is {{ name }}!
```

2.1 **Run the Instruction from Python**:

```python
from instruct.instruct import Instruct

instruct = Instruct("quickstart.instruct", name="Alice")
result = instruct.run(temperature=0.7, max_tokens=50)
print(result)
```

2.2 **Run from CLI**
```shell
echo "name: Alice" > quickstart.input
instruct run quickstart.instruct --input quickstart.input
```


## Usage

### Creating Instructions

Instructions are written in `.instruct` files. These files typically contain:

- **Shebangs**: Indicate the models on which the instruction should run.
- **Context**: The purpose and objective of the instruction.
- **Examples**: Structured examples to help the model understand the expected output.
- **Data**: Variables used in the instruction, similar to function parameters.
- **Expected Format**: Description of the expected response format.

Example of an instruction file (`hello_world.instruct`):

```
#! gpt-4o
#! llama3.2

Your task is to say "Hello, World!" to {{ name }}! in a creative way. I mean... very creative way. Like the most creative way you can think of. 
You have NO limit to imagination.
Go!

```

### Use `.instruct` in your code

To run an instruction, use the `Instruct` class:

#### Python code
```python

from instruct import Instruct

instruction = Instruct("hello_world.instruct", name="Alice")
result = instruction.run(temperature=0.7, max_tokens=50)
print(result)

```

#### CLI
Basic
```shell
instruct run examples/hello_world.instruct
```

Advanced:
```shell
instruct run example/translate.instruct --temperature 2.0 --max_token 42 --input ~/input_translation.json --output ~/output.txt
```

Help:
```shell
instruct --help
```

### Evaluating Instructions

[FUTURE WORK] Run multiple evaluations for a statistical assessment of your `instruction` for a given task on multiple models and configurations.

## Configuration

Instruct needs to know where your models are. h/t to the [LiteLLM](https://github.com/BerriAI/litellm) team that does the job of staying up to date and serve them for us. Thanks guys.

There's a unique YAML configuration file (`models.yaml`) to manage model access:

```yaml

models:
  ollama/llama3.1:
      name: llama3.1
      base_url: "http://localhost:11434"
  ollama/gemma2:
      name: gemma2
      base_url: "http://localhost:11434"
  ollama/mistral-nemo:
      name: mistral-nemo
      base_url: "http://localhost:11434"


  openai/gpt-4o:
      name: gpt-4o
      api_key: <your-api-key>

  azure/prod-gpt4o:
      client: openai
      name: gpt-4o
      base_url: <your-endpoint>
      api_version: <your-api-version>
      api_key: <your-api-key>

  azure/mistral-large-latest:
      client: mistral
      name: mistral-large
      base_url: <your-endpoint>
      api_key: <your-api-key>
  
  groq/llama3-70b-8192:
      name: llama3-70b-8192
      api_key: <your-api-key>
```

Place this file in `~/.instruct/models.yaml`.
See `/models-example-exhaustive.yaml` file for more infos

## Examples

Explore the `examples` directory for various use cases:

> 🚧 Work in progress
> Explore the directory, you will find gems of instructions made by the greatests for inspiration.

## Contributing

We welcome contributions! Please open an issue and let's start the discussion


### Developer commands

```
python3 -m pip install --force-reinstall --quiet . && instruct run examples/instructions/hello_world.instruct --gui
```

### TODO
- CORE > add "import file content" in the .instruct syntax (see Jinja2 features?)
- FEAT > Display token count of output
- FEAT > Display prompt view with tokenizer colorization and input token count
- FIX > --model flag in run command
- DOC > Create a getting started and tutorial
- FEAT > Create a wizard for 1st run to initialize ~/.instruct/models.yaml from ENV variables and step by step guide
- create a README à la https://github.com/darold/pgbadger/blob/master/doc/pgBadger.pod
- FEAT > In GUI mode, save each calls in ./instruct/dataset pair query<>answer + instruct model used [optional feedback, use case] for further use

## License

Instruct is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

If you encounter any issues or have questions, feel free to open an issue or contact me. Happy LLM explorations!