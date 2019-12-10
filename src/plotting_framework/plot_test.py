from typing import Iterable, Tuple
import plot
import importlib

def test_plot1():
    importlib.reload(plotter)

    data: Iterable[Tuple[int, int]] = ((0, 0), (10, 10))
    print(f"Data: {data}")
    result = plotter.scatter(data, (-20, -20), (20, 20))
    print(result)

def test_plot2():
    importlib.reload(plotter)

    data: Iterable[Tuple[int, int]] = ((0, 0), (-10, -10))
    result = plotter.scatter(data, (-20, -20), (20, 20))
    print(result)