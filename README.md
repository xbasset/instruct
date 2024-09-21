![instruct_logo](/assets/instruct_logo.png)

 # Instruct

Create, run, and evaluate elaborated instructions for Foundational Models like Large Language Models (LLMs).

`instruct` is a Python library designed for developers to craft rich instructions, execute them on various LLMs, and evaluate their robustness across different models.

## Table of Contents

- [Instruct](#instruct)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
  - [Usage](#usage)
    - [Creating Instructions](#creating-instructions)
    - [Running Instructions](#running-instructions)
      - [Python code](#python-code)
      - [CLI](#cli)
    - [Evaluating Instructions](#evaluating-instructions)
  - [Configuration](#configuration)
  - [Examples](#examples)
  - [Contributing](#contributing)
    - [Developer commands](#developer-commands)
    - [TODO](#todo)
  - [License](#license)

## Features

- **Create Rich Instructions**: Write developer-grade instructions to leverage the full potential of LLMs in the [VS Code Extension](https://github.com/xbasset/vscode-instruct)
![Instruct VS Code Extension](/assets/vscode-instruct.png)

- **Run Instructions**: Execute instructions on different LLMs with simple configuration from Python and directly your from CLI

![alt text](/assets/instruct-cli.png)

- **[SOON] Evaluate Instructions**: Perform statistical evaluations to ensure the robustness of instructions across multiple models.

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
#! gpt-3.5-turbo
#! gpt-4
Your task is to say "Hello, World!" to {{ name }}! in a creative way. I mean... very creative way. Like the most creative way you can think of. 
You have NO limit to imagination.
Go!

```

### Running Instructions

To run an instruction, use the `Instruct` class:

#### Python code
```python
from instruct.instruct import Instruct

pt = Instruct("hello_world.instruct", name="Alice")
result = instruct.run(temperature=0.7, max_tokens=50)
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

[FUTURE WORK] Run multiple evaluations for a statistical assessment of your `instruction` for a given task.

## Configuration

Instruct uses a YAML configuration file (`models.yaml`) to manage model access:

```yaml
openai:
  gpt-3.5-turbo:
    openai_api_key: "your_openai_api_key"
azure:
  gpt-4:
    api_key: "your_azure_api_key"
    endpoint: "your_azure_endpoint"
    api_version: "your_azure_api_version"
    deployment_id: "your_azure_deployment_id"
```

Place this file in `~/.instruct/models.yaml`.

## Examples

Explore the `examples` directory for various use cases:

- **Meeting Recap**: `examples/meeting_recap.py`
- **Translations**: `examples/translations.py`
- **Rephrase**: `examples/rephrase.py`
- **Hello World**: `examples/course_material/run_hello_world.py`

## Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) for details on how to get started.

### Developer commands

```
python3 -m pip install --force-reinstall --quiet . && instruct run examples/instructions/hello_world.instruct --no-interactivity
```

### TODO
- GUI > add copy to clipboard
- GUI > lauch GUI without waiting
- GUI > stream tokens in result view
- CORE > check replacing LLMs call with datasette.llm


## License

Instruct is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

For more detailed documentation, visit our [GitHub repository](https://github.com/xbasset/instruct). If you encounter any issues or have questions, feel free to open an issue or contact the maintainers. Happy coding!