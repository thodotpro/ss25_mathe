from tools.calculate_math_tool import CalculateMathTool


class Tools:
    _registry = {}

    @classmethod
    def register_tool(cls, tool):
        cls._registry[tool.name] = tool

    @classmethod
    def get_tools(cls):
        return cls._registry


# Register the calculate tool
Tools.register_tool(CalculateMathTool)

