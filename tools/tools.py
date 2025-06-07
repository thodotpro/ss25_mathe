from tools.calculate_math_tool import CalculateMathTool
from tools.plotting_tool import PlottingTool2D, PlottingTool3D
from tools.symbolic_math_tool import SymbolicMathTool
from tools.numeric_math_tool import NumericMathTool


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
Tools.register_tool(PlottingTool2D)
Tools.register_tool(PlottingTool3D)
Tools.register_tool(SymbolicMathTool)
Tools.register_tool(NumericMathTool)

