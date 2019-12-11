from typing import Iterable, Tuple
#from . import plot
import plot
import importlib

def test_plot3():
    importlib.reload(plot)

    data: Iterable[Iterable[Tuple[int, int]]] = (
        ((0, 0), (-10, -10)),
        ((10, 10), (-9, -9)),
        ((5, 5), (-6, 8))
    )
    result = plot.scatter(data, (-20, -20), (20, 20))
    print(result)

def test_plot2():
    importlib.reload(plot)

    data: Iterable[Tuple[int, int]] = ((0, 0), (-10, -10))
    result = plot.scatter_xy(data, (-20, -20), (20, 20))
    print(result)

def test_plot1():
    importlib.reload(plot)

    data: Iterable[Tuple[int, int]] = ((0, 0), (10, 10))
    print(f"Data: {data}")
    result = plot.scatter_xy(data, (-20, -20), (20, 20))
    print(result)