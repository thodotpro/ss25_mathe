import pytest
from tools.symbolic_math_tool import SymbolicMathTool

@pytest.mark.parametrize("params,expected", [
    # Single variable integration
    ({"expression": "x**2", "operation": "integrate", "variables": ["x"]}, "x**3/3"),
    # Single variable differentiation
    ({"expression": "x**2", "operation": "differentiate", "variables": ["x"]}, "2*x"),
    # Multi-variable integration (x then y)
    ({"expression": "x*y", "operation": "integrate", "variables": ["x", "y"]}, "x**2*y**2/4"),
    # Multi-variable differentiation (x then y)
    ({"expression": "x**2*y**2", "operation": "differentiate", "variables": ["x", "y"]}, "4*x*y"),
    # Default variable (should use x)
    ({"expression": "x", "operation": "integrate"}, "x**2/2"),
    # Error: No expression
    ({"operation": "integrate", "variables": ["x"]}, "Error: No expression provided."),
    # Error: Unsupported operation
    ({"expression": "x", "operation": "foo", "variables": ["x"]}, "Error: Unsupported operation."),
])
def test_symbolic_math_tool(params, expected):
    result = SymbolicMathTool.run(params)
    assert expected in result
