from typing import Iterable, Tuple
#from . import plot
import plot
import importlib

def test_plot8():
    importlib.reload(plot)

    data: Iterable[Iterable[Iterable[Tuple[int, int]]]] = ((
        ("points", ((0, 0), (-10, -10))),
        ("points", ((10, 10), (-9, -9))),
        ("points", ((5, 5), (-6, 8))),
        ("vector", ((-2, -1), (15, 5)))
    ), (
        ("points", ((9, 0), (-10, -10))),
        ("points", ((19, 10), (-9, -9))),
        ("points", ((9, 5), (-6, 8))),
        ("vector", ((-2, -1), (15, 5)))
    ), (
        ("points", ((5, 0), (-10, -10))),
        ("points", ((15, 10), (-9, -9))),
        ("points", ((5, 5), (-6, 8))),
        ("vector", ((-2, -1), (15, 5)))
    ))

    result = plot.plot(data, (-20, -20), (20, 20), 3)
    print(result)

def test_plot7():
    importlib.reload(plot)

    data: Iterable[Iterable[Iterable[Tuple[int, int]]]] = ((
        ("points", ((0, 0), (-10, -10))),
        ("points", ((10, 10), (-9, -9))),
        ("points", ((5, 5), (-6, 8)))
    ), (
        ("points", ((9, 0), (-10, -10))),
        ("points", ((19, 10), (-9, -9))),
        ("points", ((9, 5), (-6, 8)))
    ), (
        ("points", ((5, 0), (-10, -10))),
        ("points", ((15, 10), (-9, -9))),
        ("points", ((5, 5), (-6, 8)))
    ))
    result = plot.plot(data, (-20, -20), (20, 20), 3)
    print(result)

def test_plot6():
    importlib.reload(plot)

    data: Iterable[Iterable[Iterable[Tuple[int, int]]]] = ((
        ((0, 0), (-10, -10)),
        ((10, 10), (-9, -9)),
        ((5, 5), (-6, 8))
    ),)
    result = plot.scatter_animate(data, (-20, -20), (20, 20), 3)
    print(result)

def test_plot5():
    importlib.reload(plot)

    data: Iterable[Iterable[Iterable[Tuple[int, int]]]] = ((
        ((0, 0), (-10, -10)),
        ((10, 10), (-9, -9)),
        ((5, 5), (-6, 8))
    ), (
        ((9, 0), (-10, -10)),
        ((19, 10), (-9, -9)),
        ((9, 5), (-6, 8))
    ), (
        ((5, 0), (-10, -10)),
        ((15, 10), (-9, -9)),
        ((5, 5), (-6, 8))
    ))
    result = plot.scatter_animate(data, (-20, -20), (20, 20), 3)
    print(result)

def test_plot4():
    importlib.reload(plot)

    data: Iterable[Iterable[Iterable[Tuple[int, int]]]] = ((
        ((0, 0), (1, 1)),
    ), (
        ((5, 5), (10, 10)),
    ), (
        ((10, 10), (19, 19)),
    ))
    result = plot.scatter_animate(data, (-20, -20), (20, 20), 3)
    print(result)

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