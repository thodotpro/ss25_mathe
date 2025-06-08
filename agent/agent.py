import re
import os
from typing import Any
from dotenv import load_dotenv
from tools.tools import Tools
from tools.gemini_formatter import GeminiFormatter
from tools.ollama_adapter import OllamaClient
from tools.ollama_formatter import OllamaFormatter

load_dotenv()   # load api-key from .env file, comment this line if you want to use a hardcoded API key

# Set up model and parameters for Gemini
model  = "gemini-2.0-flash" # Model to use, can be changed as needed
max_tokens = 1024  # Maximum number of tokens for the response, can be adjusted
top_p = 0.95  # Top-p sampling for response generation, can be adjusted
top_k = 40  # Top-k sampling for response generation, can be adjusted

try:
    from google import genai
    client = genai.Client(
        api_key=os.environ.get("GOOGLE_API_KEY"),
    )
except ImportError:
    client = None

system_prompt_path = "docs/system_prompt.txt" # Path to the system prompt file
temperature = 0.1  # set model temperature

def system_prompt() -> str:
    """
    Returns the system prompt for the agent.
    This can be customized as needed.
    """
    with open(system_prompt_path, "r") as file:
        system_prompt = file.read().strip()
    return system_prompt

class Agent:
    def __init__(self, use_ollama=False, ollama_model="gemma3:4b", system=system_prompt()):
        self.use_ollama = use_ollama
        self.system = system
        self.tools = Tools.get_tools()
        self.messages = []
        if use_ollama:
            self.client = OllamaClient(model=ollama_model)
            self.formatter = OllamaFormatter
        else:
            self.client = client
            self.formatter = GeminiFormatter

    def __call__(self, query) -> Any:
        return self._agent_loop(query)

    def _execute(self, query: str) -> Any:
        if not query:
            raise ValueError("Query cannot be empty.")
        self.messages.append({"role": "user", "content": query})
        formatted_content = self.formatter.format_messages(self.messages, self.system)
        if self.use_ollama:
            response_text = self.client.generate(formatted_content, system=self.system)
            self.messages.append({"role": "assistant", "content": response_text})
            return response_text
        else:
            response = self.client.models.generate_content(
                model=model,
                contents=formatted_content,
                max_output_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
            )
            self.messages.append({"role": "assistant", "content": response.text})
            return response.text

    def _agent_loop(self, query: str, max_steps: int = 10) -> str:
        if not query:
            raise ValueError("Query cannot be empty.")
        self.messages = []
        self.messages.append({"role": "user", "content": query})
        tools_used = set()
        steps = 0
        last_text = None
        real_plot_filename = None
        while steps < max_steps:
            formatted_content = self.formatter.format_messages(
                self.messages, self.system, include_system_prompt=(steps == 0)
            )
            if self.use_ollama:
                text = self.client.generate(formatted_content, system=self.system).strip()
            else:
                response = self.client.models.generate_content(
                    model=model,
                    contents=formatted_content,
                )
                text = response.text.strip() if response.text else ""
            self.messages.append({"role": "assistant", "content": text})
            # Print only the LLM's reasoning and answers
            for line in text.splitlines():
                if not line.strip().startswith("You are ToolAgentLab") and not line.strip().startswith("Your available actions are:") and not line.strip().startswith("Reference: This agent is inspired") and not line.strip().startswith("Example session:") and not line.strip().startswith("Question:"):
                    print(line)
            if "Answer:" in text and real_plot_filename:
                # Replace any output/plot/plot_2d.png or similar with the real filename
                import re as _re
                text = _re.sub(r'output/plot/plot_2d(\.png)?', real_plot_filename, text)
                print(f"[AGENT] Final answer filename replaced: {real_plot_filename}")
                print(f"Tools used: {', '.join(tools_used) if tools_used else 'None'}")
                return text
            if last_text == text:
                print("[DEBUG] Repeated response detected, breaking loop.")
                break
            last_text = text
            action_match = re.search(r"Action:\s*(\w+):\s*(.*)", text)
            if action_match:
                action_name = action_match.group(1).strip()
                action_arg = action_match.group(2).strip()
                tool = self.tools.get(action_name)
                if tool:
                    if action_name == "plot_2d":
                        import numpy as np
                        import os
                        import time
                        match = re.match(r"(.+) for x in range\((.+)\)", action_arg)
                        if match:
                            func_str = match.group(1).strip()
                            range_args = [int(v) for v in match.group(2).split(",")]
                            x = list(range(*range_args))
                            allowed_names = {k: getattr(np, k) for k in dir(np) if not k.startswith("_")}
                            y = [eval(func_str, {"__builtins__": {}}, dict(allowed_names, x=xi)) for xi in x]
                            filename = os.path.join("output/plot", f"plot2d_{int(time.time())}.png")
                            params = {"x": x, "y": y, "filename": filename}
                            observation = tool.run(params)
                            if os.path.exists(filename):
                                print(f"[TOOL] plot_2d generated: {observation}\n[TOOL] Plot file: {filename}")
                                real_plot_filename = filename
                            else:
                                print(f"[TOOL] plot_2d attempted but file not found: {filename}")
                        else:
                            observation = "Error: Could not parse plot_2d input."
                    elif action_name in ["symbolic_math", "numeric_math", "plot_3d"]:
                        match = re.match(r"(integrate|differentiate|diff)\((.*)\)", action_arg)
                        if match:
                            op = match.group(1)
                            rest = match.group(2)
                            parts = [p.strip() for p in rest.split(',')]
                            expr = parts[0]
                            variables = [v for v in parts[1:]]
                            params = {"operation": op, "expression": expr, "variables": variables}
                            observation = tool.run(params)
                        else:
                            observation = tool.run({"expression": action_arg})
                    else:
                        observation = tool.run(action_arg)
                    tools_used.add(action_name)
                else:
                    observation = f"Error: Unknown tool '{action_name}'"
                self.messages.append({"role": "user", "content": f"Observation: {observation}"})
            else:
                break
            steps += 1
        print(f"Tools used: {', '.join(tools_used) if tools_used else 'None'}")
        return text


def main():
    agent = Agent(use_ollama=True, ollama_model="gemma3:4b")
    query = "What is the value of the derivative of x**2 + y**2 with respect to x at x=2, y=3?"
    result = agent(query)
    print(f"Query: {query}\n")
    print(result)

if __name__ == "__main__":
    main()