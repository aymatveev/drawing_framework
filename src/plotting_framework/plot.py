from typing import Iterable, Tuple
import colors

def remove_linebreaks(s: str) -> str:
    return "".join(s.split("\n"))

def shift_data(data: Iterable[Tuple[float, float]], offset: Tuple[float, float]) -> Iterable[Tuple[float, float]]:
    return ((p[0] - offset[0], p[1] - offset[1]) for p in data)

def scale_data(data: Iterable[Tuple[float, float]], scale: Tuple[float, float]) -> Iterable[Tuple[float, float]]:
    return ((p[0] * scale[0], p[1] * scale[1]) for p in data)

def transform_to_screen_plane(
    data: Iterable[Tuple[float, float]],
    bl: Tuple[float, float],
    tr: Tuple[float, float],
    width: int = 640,
    height: int = 480) -> Iterable[Tuple[float, float]]:
    middle = ((bl[0] + tr[0]) / 2, (bl[1] + tr[1]) / 2)
    viewport_middle = (- width / 2, - height / 2)

    scale = (width / abs(bl[0] - tr[0]), height / abs(bl[1] - tr[1]))

    centered_data: Iterable[Tuple[float, float]] = shift_data(data, middle)
    scaled_data: Iterable[Tuple[float, float]] = scale_data(centered_data, scale)
    shifted_data: Iterable[Tuple[float, float]] = shift_data(scaled_data, viewport_middle)
    scaled_data_int: Iterable[Tuple[int, int]] = ((round(p[0]), round(p[1])) for p in shifted_data)
    flipped_y_data: Iterable[Tuple[int, int]] = ((p[0], height - p[1]) for p in scaled_data_int)

    return flipped_y_data

def svg_wrap(width: int, height: int, content: str) -> str:
    return f"""<svg width="{width}" height="{height}">{content}</svg>"""

def draw_axes(width: int, height: int, bl: Tuple[float, float], tr: Tuple[float, float]) -> str:
    return remove_linebreaks(f"""
        <line x1="0" y1="{height}" x2="{width}" y2="{height}" stroke="black" />
        <line x1="0" y1="0" x2="0" y2="{height}" stroke="black" />
        <text x="10" y="{height - 10}" class="small">{bl}</text>
        <text x="{width - 80}" y="{15}" class="small">{tr}</text>
    """)

def mark_point(point: Tuple[int, int], size: int = 3, color: str = "black") -> str:
    return f"""<circle cx="{point[0]}" cy="{point[1]}" r="{size}" style="fill: {color}"/>"""

def join_series_of_points(data: Iterable[Tuple[float, float]], point_size: int = 3, color: str = "black") -> str:
    return "".join(mark_point(p, point_size, color) for p in data)

def scatter(
    data: Iterable[Iterable[Tuple[float, float]]],
    bl: Tuple[float, float],
    tr: Tuple[float, float],
    point_size: int = 3,
    width: int = 640,
    height: int = 480) -> str:
    color_gen = colors.color_generator()
    transformed_data = tuple(transform_to_screen_plane(series, bl, tr, width, height) for series in data)
    return svg_wrap(width, height, remove_linebreaks(f"""
        {draw_axes(width, height, bl, tr)}
        {"".join(join_series_of_points(series, point_size, next(color_gen)) for series in transformed_data)}
    """))

def scatter_xy(
    data: Iterable[Tuple[float, float]],
    bl: Tuple[float, float],
    tr: Tuple[float, float],
    point_size: int = 3,
    width: int = 640,
    height: int = 480) -> str:
    return scatter((data,), bl, tr, point_size, width, height)
