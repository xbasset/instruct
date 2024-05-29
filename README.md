 # Instruct

`instruct` is a Python library designed to create, run, and evaluate instructions for Large Language Models (LLMs). It allows developers to craft rich instructions, execute them on various LLMs, and evaluate their robustness across different models.

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
  - [License](#license)

## Features

- **Create Instructions**: Write developer instructions to leverage the full potential of LLMs. Soon: VS Code Extension
- **Run Instructions**: Execute instructions on different LLMs with simple configuration, or directly from CLI
- **[SOON] Evaluate Instructions**: Perform statistical evaluations to ensure the robustness of instructions across multiple models.

## Installation

To install Instruct, use pip:

```bash
pip install instruct
```

## Quick Start

Here's a quick example to get you started with Instruct:

1. **Create an Instruction File** (`hello_world.pt`):

    ```plaintext
    #! gpt-3.5-turbo
    #! gpt-4

    Hello, {{ name }}!
    ```

2. **Run the Instruction**:

    ```python
    from instruct.pt import PT

    pt = PT("hello_world.pt", name="Alice")
    result = pt.run(temperature=0.7, max_tokens=50)
    print(result)
    ```

## Usage

### Creating Instructions

Instructions are written in `.pt` – for Prompt Template – files. These files contain:

- **Shebangs**: Indicate the models on which the instruction should run.
- **Context**: The purpose and objective of the instruction.
- **Examples**: Structured examples to help the model understand the expected output.
- **Data**: Variables used in the instruction, similar to function parameters.
- **Expected Format**: Description of the expected response format.

Example of an instruction file (`hello_world.pt`):

```shell
#! gpt-3.5-turbo
#! gpt-4
Your task is to say "Hello, World!" to {{ name }}! in a creative way. I mean... very creative way. Like the most creative way you can think of. 
You have NO limit to imagination.
Go!

```

### Running Instructions

To run an instruction, use the `PT` class:

#### Python code
```python
from instruct.pt import PT

pt = PT("hello_world.pt", name="Alice")
result = pt.run(temperature=0.7, max_tokens=50)
print(result)
```

#### CLI
Basic
```shell
instruct run examples/hello_world.pt
```

Advanced:
```shell
instruct run example/translate.pt --temperature 2.0 --max_token 42 --input ~/input_translation.json --output ~/output.txt
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

Place this file in `~/.pt/models.yaml`.

## Examples

Explore the `examples` directory for various use cases:

- **Meeting Recap**: `examples/meeting_recap.py`
- **Translations**: `examples/translations.py`
- **Rephrase**: `examples/rephrase.py`
- **Hello World**: `examples/course_material/run_hello_world.py`

## Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) for details on how to get started.

## License

Instruct is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

For more detailed documentation, visit our [GitHub repository](https://github.com/xbasset/instruct). If you encounter any issues or have questions, feel free to open an issue or contact the maintainers. Happy coding!