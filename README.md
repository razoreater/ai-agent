# ai-agent

A command-line AI agent powered by Google Gemini that can autonomously use tools to complete tasks — including reading files, running Python scripts, and performing calculations.

## Features

- Conversational agentic loop with up to 20 iterations
- Tool/function calling via the Gemini API
- Built-in tools: file reading, file info, Python execution, and a calculator
- Verbose mode for token usage and step-by-step output
- Configurable system prompt

## Requirements

- Python 3.x (see `.python-version`)
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)
- [`uv`](https://github.com/astral-sh/uv) (recommended) or `pip`

## Installation

```bash
git clone https://github.com/razoreater/ai-agent.git
cd ai-agent
```

Install dependencies with `uv`:

```bash
uv sync
```

## Configuration

Create a `.env` file in the project root with your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

## Usage

```bash
python main.py "your prompt here"
```

Enable verbose output to see token usage and function call details:

```bash
python main.py "your prompt here" --verbose
```

### Examples

```bash
python main.py "What files are in the calculator directory?"
python main.py "Run the calculator script and add 42 and 58" --verbose
python main.py "Read config.py and summarize what it does"
```

## Project Structure

```
ai-agent/
├── main.py              # Entry point and agent loop
├── prompts.py           # System prompt definition
├── config.py            # Configuration settings
├── functions/           # Tool implementations
│   └── call_function.py # Function dispatch and available tools
├── calculator/          # Example calculator module
├── test_*.py            # Unit tests for each tool
└── pyproject.toml       # Project metadata and dependencies
```

## How It Works

1. Your prompt is sent to Gemini 2.5 Flash with a set of available tools.
2. The model decides whether to call a tool or respond directly.
3. If a tool is called, the result is fed back into the conversation.
4. This loop repeats until the model gives a final text response (or 20 iterations are reached).

## License

[WTFPL](LICENSE) — Do What The F*** You Want To Public License
