import numpy as np

class NumericMathTool:
    name = "numeric_math"
    description = (
        "Performs numerical mathematics operations using NumPy. "
        "Example: 'sin(0)' returns 0.0. Supports basic operations like addition, "
        "subtraction, multiplication, division, and trigonometric functions."
    )

    @staticmethod
    def run(expression: str):
        try:
            # Only allow safe builtins and NumPy functions
            allowed_names = {k: getattr(np, k) for k in dir(np) if not k.startswith("_")}
            allowed_names["np"] = np
            # Evaluate the expression safely
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return str(result)
        except Exception as e:
            return f"Error: Could not evaluate expression. {e}"

