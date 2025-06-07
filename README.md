# toolagentlab

This project is a modular, extensible Python agent for solving mathematical tasks using the Google Gemini API and a flexible, registry-based tools system.

> **System prompt and agent loop inspired by the Python ReAct pattern from [Simon Willison's blog](https://til.simonwillison.net/llms/python-react-pattern).**

## Features
- OOP-style agent with ReAct loop (Thought → Action → Observation → Answer)
- Modular, extensible tools system (registry pattern)
- Gemini API integration (API key via `.env`)
- System prompt and assignment text externalized in `docs/`
- Pytest-based tests for agent and all tools
- Ready for notebook-based or script-based presentation
- Plots saved in `output/plot/` with unique filenames

## Available Tools
- `calculate`: Simple Python math expressions (supports math functions and safe built-ins like sum, min, max, abs, round, range)
- `numeric_math`: Numeric math with NumPy (trigonometric, exponential, logarithmic, etc.)
- `symbolic_math`: Symbolic math (integration, differentiation, multi-variable) with SymPy
- `plot_2d`: 2D plotting for functions of one variable (plots saved in `output/plot/`)
- `plot_3d`: 3D surface plotting for functions of two variables (plots saved in `output/plot/`)

## Setup
1. **Clone the repository**
2. **Install dependencies** (from project root):
   ```bash
   pip install -e .
   # or, if using uv:
   uv pip install -r pyproject.toml
   ```
3. **Create a `.env` file** in the project root with your Google API key:
   ```
   GOOGLE_API_KEY=your-key-here
   ```
4. **Run tests**:
   ```bash
   pytest -v
   ```
5. **Try the agent**:
   ```bash
   python testing.py
   # or run as a module:
   python -m agent.agent
   ```

## Usage
- **Direct tool usage:** See `testing.py` for examples of calling tools directly.
- **Agent usage:** Call the agent with a query; it will reason step by step, use the most appropriate tool(s), and return an answer.

## System Prompt
See `docs/system_prompt.txt` for the current system prompt, available actions, and usage examples.

## Testing
- All tools and agent logic are covered by pytest tests in `test/`.

## License
MIT License

## Authors
- Thomas Proksch

---
For questions or contributions, open an issue or pull request.
