import pytest
from tools.calculate_math_tool import CalculateMathTool

def test_calculate_simple():
    assert CalculateMathTool.run("2 + 2") == 4
    assert CalculateMathTool.run("4 * 7 / 3") == pytest.approx(9.3333333333)
    assert CalculateMathTool.run("10 - 3**2") == 1

def test_calculate_error():
    result = CalculateMathTool.run("1 / 0")
    assert isinstance(result, str)
    assert "Error" in result
