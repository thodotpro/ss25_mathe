import re
import os
from typing import Any
from dotenv import load_dotenv
from tools.tools import Tools
from google import genai
from tools.gemini_formatter import GeminiFormatter

load_dotenv()   # load api-key from .env file, comment this line if you want to use a hardcoded API key

# Set up model and parameters
model  = "gemini-2.0-flash" # Model to use, can be changed as needed
max_tokens = 1024  # Maximum number of tokens for the response, can be adjusted
top_p = 0.95  # Top-p sampling for response generation, can be adjusted
top_k = 40  # Top-k sampling for response generation, can be adjusted

client = genai.Client(
    api_key=os.environ.get("GOOGLE_API_KEY"),
)  

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
    def __init__(self, client=client, system=system_prompt()) -> None:
        self.client = client
        self.system = system
        self.formatter = GeminiFormatter    # adapter for google gemini
        self.messages = []
        self.tools = Tools.get_tools()
        
        
    def __call__(self, query) -> Any:
        return self._agent_loop(query)

    def _execute(self, query: str) -> Any:
        if not query:
            raise ValueError("Query cannot be empty.")

        self.messages.append({"role": "user", "content": query})

        formatted_content = self.formatter.format_messages(self.messages, self.system)

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

    def _agent_loop(self, query: str) -> str:
        """
        Runs the Thought → Action → Observation → ... → Answer loop until an Answer is produced.
        """
        if not query:
            raise ValueError("Query cannot be empty.")
        self.messages = []
        self.messages.append({"role": "user", "content": query})
        tools_used = set()
        while True:
            formatted_content = self.formatter.format_messages(self.messages, self.system)
            response = self.client.models.generate_content(
                model=model,
                contents=formatted_content,
            )
            text = response.text.strip() if response.text else ""
            self.messages.append({"role": "assistant", "content": text})
            print(text)  # Print each step for transparency
            # Check for final answer
            if text.lower().startswith("answer:"):
                print(f"Tools used: {', '.join(tools_used) if tools_used else 'None'}")
                return text
            # Parse Action
            action_match = re.search(r"Action:\s*(\w+):\s*(.*)", text)
            if action_match:
                action_name = action_match.group(1).strip()
                action_arg = action_match.group(2).strip()
                tool = self.tools.get(action_name)
                if tool:
                    # Special handling for tools that expect a dict
                    if action_name == "plot_2d":
                        import numpy as np
                        match = re.match(r"(.+) for x in range\((.+)\)", action_arg)
                        if match:
                            func_str = match.group(1).strip()
                            range_args = [int(v) for v in match.group(2).split(",")]
                            x = list(range(*range_args))
                            allowed_names = {k: getattr(np, k) for k in dir(np) if not k.startswith("_")}
                            y = [eval(func_str, {"__builtins__": {}}, dict(allowed_names, x=xi)) for xi in x]
                            params = {"x": x, "y": y}
                            observation = tool.run(params)
                        else:
                            observation = "Error: Could not parse plot_2d input."
                    elif action_name in ["symbolic_math", "numeric_math", "plot_3d"]:
                        # Minimal parser for symbolic_math: e.g. "integrate(x*y**2, x, y)"
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
                            # Fallback: pass as expression only
                            observation = tool.run({"expression": action_arg})
                    else:
                        observation = tool.run(action_arg)
                    tools_used.add(action_name)
                else:
                    observation = f"Error: Unknown tool '{action_name}'"
                self.messages.append({"role": "user", "content": f"Observation: {observation}"})
            else:
                # If no action, break to avoid infinite loop
                break
        print(f"Tools used: {', '.join(tools_used) if tools_used else 'None'}")
        return text
    

def main():
    agent = Agent()
    query = "What is the capital of France?"
    result = agent(query)
    print(f"Query: {query}\n")
    print(result)


if __name__ == "__main__":
    main()