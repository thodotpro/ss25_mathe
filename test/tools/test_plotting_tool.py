import os
import pytest
from tools.plotting_tool import PlottingTool2D, PlottingTool3D


def test_plotting_tool_2d(tmp_path):
    params = {
        "x": [1, 2, 3],
        "y": [4, 5, 6],
        "title": "Test 2D Plot",
        "xlabel": "X",
        "ylabel": "Y",
        "filename": str(tmp_path / "test_plot2d.png")
    }
    result = PlottingTool2D.run(params)
    assert "2D plot saved as" in result
    assert os.path.exists(params["filename"])
    assert os.path.getsize(params["filename"]) > 0


def test_plotting_tool_2d_error():
    params = {"x": [1, 2], "y": [3]}  # mismatched lengths
    result = PlottingTool2D.run(params)
    assert "Error" in result


def test_plotting_tool_3d(tmp_path):
    params = {
        "x": [1, 2, 3],
        "y": [4, 5, 6],
        "z": [7, 8, 9],
        "title": "Test 3D Plot",
        "xlabel": "X",
        "ylabel": "Y",
        "zlabel": "Z",
        "filename": str(tmp_path / "test_plot3d.png")
    }
    result = PlottingTool3D.run(params)
    assert "3D plot saved as" in result
    assert os.path.exists(params["filename"])
    assert os.path.getsize(params["filename"]) > 0


def test_plotting_tool_3d_error():
    params = {"x": [1, 2], "y": [3, 4], "z": [5]}  # mismatched lengths
    result = PlottingTool3D.run(params)
    assert "Error" in result
