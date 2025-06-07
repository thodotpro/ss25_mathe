import math

class CalculateMathTool:
    name = "calculate"
    description = "Evaluates a simple Python mathematical expression. Example: '2 + 2' returns 4. Supports math functions and safe built-ins like sum, min, max, abs, round, and range."

    @staticmethod
    def run(expression: str):
        try:
            allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
            allowed_names.update({
                "sum": sum,
                "min": min,
                "max": max,
                "abs": abs,
                "round": round,
                "range": range
            })
            return str(eval(expression, {"__builtins__": {}}, allowed_names))
        except Exception as e:
            return f"Error: {e}"
