class CalculateMathTool:
    name = "calculate"
    description = "Evaluates a simple Python mathematical expression. Example: '2 + 2' returns 4."

    @staticmethod
    def run(expression: str):
        try:
            # Only allow safe builtins
            return eval(expression, {"__builtins__": {}})
        except Exception as e:
            return f"Error: {e}"
