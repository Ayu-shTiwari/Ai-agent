# AI-Agent: Assistant that lives in your terminal

An intelligent, command-line based AI agent that leverages a Large Language Model (LLM) with function-calling capabilities to interact with the local file system. The agent can understand natural language prompts to perform operations like listing files, reading content, writing to files, and executing Python scripts within a secure, sandboxed directory.

## ✨ Features

-   **Natural Language Interface**: Interact with your files using plain English.
-   **File System Operations**:
    -   List files and directories.
    -   Read content from any file.
    -   Write or overwrite content to any file.
    -   Run python files
-   **Code Execution**: Run Python scripts and see their output directly.
-   **Secure & Sandboxed**: All operations are restricted to a designated working directory (`calculator` in this example) to prevent unintended changes to your system.
-   **Extensible**: Easily add new tools and capabilities in the `functions` directory.

## 📂 Project Structure

The project is organized to separate concerns, making it easy to manage and extend.

```
AI-AGENT/
├── .venv/                  # Virtual environment
├── calculator/             # The sandboxed working directory for the agent
│   ├── pkg/
│   │   ├── calculator.py
│   │   └── render.py
│   ├── main.py
│   └── tests.py
├── functions/              # Core agent capabilities (tools)
│   ├── get_file_content.py
│   ├── get_files_info.py
│   ├── run_python_file.py
│   ├── tools_schema.py     # Schemas defining the tools for the LLM
│   └── write_file.py
├── .env                    # Environment variables (API Keys, etc.)
├── .gitignore
├── agent_instructions.py   # System prompt/instructions for the AI agent
├── config.py               # Project configuration
├── main.py                 # Main entry point for the agent application
├── pyproject.toml          # Project metadata and dependencies (for uv/pip)
├── README.md               # You are here!
└── uv.lock                 # Dependency lock file for reproducible builds
```

## 🚀 Getting Started

Follow these instructions to get the AI agent running on your local machine.

### Prerequisites

-   Python 3.10+
-   [uv](https://github.com/astral-sh/uv) (a fast Python package installer, can be installed via `pip install uv`)
-   Git

### Installation

1.  **Clone the repository:**
    ```sh
    git clone <your-repository-url>
    cd AI-AGENT
    ```

2.  **Create a virtual environment and install dependencies:**
    The project is configured to use `uv`. This command creates a virtual environment and installs all packages from `pyproject.toml`.
    ```sh
    uv sync
    ```

3.  **Set up your environment variables:**
    Create a file named `.env` in the root of the project by copying the example file.
    ```sh
    cp .env.example .env
    ```
    Now, open the `.env` file and add your Google Gemini API key:
    ```ini
    # .env
    LLM_API_KEY="YOUR_API_KEY_HERE"
    ```

## Usage

You can run the agent from the command line. The main entry point is `main.py`. You pass your request as a string argument.

### General Syntax

```sh
uv run main.py "<your prompt in natural language>"
```

### Examples

1.  **List all files in the `calculator` directory:**
    ```sh
    uv run main.py "what files are in the current directory?"
    ```

2.  **Read the contents of `calculator/main.py`:**
    ```sh
    uv run main.py "can you show me the code inside calculator/main.py"
    ```

3.  **Create a new file and write to it:**
    ```sh
    uv run main.py "create a file named 'hello.txt' with the content 'Hello World'"
    ```

4.  **Execute the main calculator script:**
    ```sh
    uv run main.py "run the main.py file in the calculator directory"
    ```

5.  **Use the `--verbose` flag for more details:**
    To see token counts and other metadata from the LLM response, add the `--verbose` flag.
    ```sh
    uv run main.py "list files" --verbose
    ```

## ⚙️ How It Works

The agent follows a simple yet powerful workflow:

1.  **Input**: The user provides a natural language prompt via the command line.
2.  **System Prompt**: The `agent_instructions.py` file provides the LLM with its role, capabilities, and constraints.
3.  **Tool Definitions**: The schemas in `tools_schema.py` describe the available Python functions (`get_files_info`, `write_file`, etc.) to the LLM in a structured format.
4.  **LLM Planning**: The LLM receives the user prompt, system instructions, and tool definitions. It then formulates a plan, deciding which function(s) to call with what arguments to fulfill the request.
5.  **Function Execution**: The application parses the LLM's plan and executes the corresponding Python functions locally.
6.  **Output**: The result of the function call (e.g., file content, a success message) is displayed to the user.

## 🧪 Testing

To run the suite of tests for the project, use the following command:

```sh
uv run python -m unittest discover
```
