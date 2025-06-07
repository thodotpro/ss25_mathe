import pytest
import numpy as np
from tools.numeric_math_tool import NumericMathTool

@pytest.mark.parametrize("expression,expected", [
    ("1 + 2", "3"),
    ("np.sin(0)", "0.0"),
    ("sin(0)", "0.0"),
    ("np.cos(np.pi)", "-1.0"),
    ("cos(np.pi)", "-1.0"),
    ("2 * 3 + 4", "10"),
    ("np.sqrt(16)", "4.0"),
    ("sqrt(16)", "4.0"),
    ("np.log(1)", "0.0"),
    ("log(1)", "0.0"),
    ("np.exp(2)", str(np.exp(2))),
    ("exp(2)", str(np.exp(2))),
    ("1 / 0", "Error: Could not evaluate expression."),
    ("open('file')", "Error: Could not evaluate expression."),
])
def test_numeric_math_tool(expression, expected):
    result = NumericMathTool.run(expression)
    assert expected in result
