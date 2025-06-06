# SS25 Mathematik KI-Agent

This project is a modular, extensible Python agent for solving mathematical tasks using the Google Gemini API and custom tools. It is designed for E-Learning assignments and presentations, supporting step-by-step reasoning, tool use, and easy integration with Jupyter notebooks.

## Features
- OOP-style agent with ReAct loop (Thought → Action → Observation → Answer)
- Modular tools system (currently: calculate)
- Gemini API integration (API key via `.env`)
- System prompt and assignment text externalized in `docs/`
- Pytest-based tests for agent and calculate tool
- Ready for notebook-based presentation

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
- **Direct tool usage:** See `testing.py` for examples of calling the calculate tool directly.
- **Agent usage:** Call the agent with a query; it will reason, use the calculate tool, and return an answer.
- **Notebook presentation:** Use or generate a Jupyter notebook for step-by-step results and visualizations.

## Tools
- `calculate`: Simple math expressions (Python syntax)

## System Prompt
See `docs/system_prompt.txt` for the current system prompt and available actions.

## Testing
- Agent and calculate tool are covered by pytest tests in `test/`.

## License
MIT License

## Authors
- Thomas Proksch

---
For questions or contributions, open an issue or pull request.
