from matplotlib import pyplot as plt
import os
import time

class PlottingTool2D:
    name = "plot_2d"
    description = "Generates a 2D plot from given x and y data. Accepts optional title, xlabel, ylabel, and filename. Example usage: run({'x': [1,2,3], 'y': [4,5,6], 'title': 'My Plot', 'filename': 'plot.png'})"

    @staticmethod
    def run(params: dict):
        x = params.get("x")
        y = params.get("y")
        title = params.get("title", "2D Plot")
        xlabel = params.get("xlabel", "X-axis")
        ylabel = params.get("ylabel", "Y-axis")
        # Ensure output/plot directory exists
        os.makedirs("output/plot", exist_ok=True)
        filename = params.get("filename", os.path.join("output/plot", f"plot2d_{int(time.time())}.png"))
        if not x or not y or len(x) != len(y):
            return "Error: x and y must be provided and have the same length."
        plt.figure()
        plt.plot(x, y, marker='o')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.savefig(filename)
        plt.close()
        return f"2D plot successfully saved as {filename}."

class PlottingTool3D:
    name = "plot_3d"
    description = "Generates a 3D plot from given x, y, and z data. Accepts optional title, xlabel, ylabel, zlabel, and filename. Example usage: run({'x': [1,2,3], 'y': [4,5,6], 'z': [7,8,9], 'title': 'My 3D Plot', 'filename': 'plot3d.png'})"

    @staticmethod
    def run(params: dict):
        x = params.get("x")
        y = params.get("y")
        z = params.get("z")
        title = params.get("title", "3D Plot")
        xlabel = params.get("xlabel", "X-axis")
        ylabel = params.get("ylabel", "Y-axis")
        zlabel = params.get("zlabel", "Z-axis")
        # Ensure output/plot directory exists
        os.makedirs("output/plot", exist_ok=True)
        filename = params.get("filename", os.path.join("output/plot", f"plot3d_{int(time.time())}.png"))
        if not x or not y or not z or len(x) != len(y) or len(y) != len(z):
            return "Error: x, y, and z must be provided and have the same length."
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(x, y, z, marker='o')
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)
        plt.savefig(filename)
        plt.close(fig)
        return f"3D plot successfully saved as {filename}."