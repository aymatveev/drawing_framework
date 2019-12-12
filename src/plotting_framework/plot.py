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

    return tuple(flipped_y_data)

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

def join_serieses_of_points(data: Iterable[Iterable[Tuple[float, float]]], color_gen: Iterable[str], point_size: int = 3) -> str:
    return "".join(join_series_of_points(series, point_size, next(color_gen)) for series in data)

def draw_internal(
    desc: str,
    data: Iterable[Tuple[float, float]],
    bl: Tuple[float, float],
    tr: Tuple[float, float],
    point_size: int = 3,
    color: str = "black") -> str:
    if desc == "points":
        return join_series_of_points(data, point_size, color)
    if desc == "vector":
        p1, p2 = tuple(data)[:2]
        return f"""<line x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}" stroke="{color}"/>"""
    
    if len(data) != 2:
        return ""
    p1, p2 = tuple(data)[:2]
    k = (p2[1] - p1[1]) / (p2[0] - p1[0])
    b = p1[1] - k * p1[0]
    left = (bl[0], k * bl[0] + b)
    right = (tr[0], k * tr[0] + b)

    return f"""<line x1="{left[0]}" y1="{left[1]}" x2="{right[0]}" y2="{right[1]}" style="fill: {color}"/>"""


def draw(
    data: Iterable[Tuple[str, Iterable[Tuple[float, float]]]],
    color_gen: Iterable[str],
    bl: Tuple[float, float],
    tr: Tuple[float, float],
    point_size: int = 3) -> str:
    return "".join(draw_internal(desc, series, bl, tr, point_size, next(color_gen)) for (desc, series) in data)

def get_animation_frame(content: str, duration: int, keytimes: Iterable[str], visible_keytime: int) -> str:
    values = tuple(("visible" if vidx == visible_keytime else "hidden") for vidx in range(len(keytimes))) + ("hidden",)
    return remove_linebreaks(f"""
        <g>
            {content}
            <animate attributeName="visibility" dur="{duration}s" repeatCount="indefinite" values="{";".join(values)}" keyTimes="{";".join(tuple(keytimes) + ("1",))}"/>
        </g>
    """)

def plot(
    data: Iterable[Iterable[Tuple[str, Iterable[Tuple[float, float]]]]],
    bl: Tuple[float, float],
    tr: Tuple[float, float],
    animation_duration: int = 10,
    point_size: int = 3,
    width: int = 640,
    height: int = 480) -> str:
    n_frames = len(data)
    keytimes = tuple(str(key / n_frames)[:5] for key in range(len(data)))
    transformed_data = tuple(tuple((desc, transform_to_screen_plane(series, bl, tr, width, height)) for (desc, series) in keyframe) for keyframe in data)
    transformed_data = tuple(tuple((desc, (series + (series[0],))) for (desc, series) in keyframe) for keyframe in transformed_data)
    return svg_wrap(width, height, remove_linebreaks(f"""
        {draw_axes(width, height, bl, tr)}
        {tuple(get_animation_frame(draw(keyframe, colors.color_generator(), bl, tr, point_size), animation_duration, keytimes, idx) for (idx, keyframe) in enumerate(transformed_data))}
    """))

def scatter_animate(
    data: Iterable[Iterable[Iterable[Tuple[float, float]]]],
    bl: Tuple[float, float],
    tr: Tuple[float, float],
    animation_duration: int = 10,
    point_size: int = 3,
    width: int = 640,
    height: int = 480) -> str:
    n_frames = len(data)
    keytimes = tuple(str(key / n_frames)[:5] for key in range(len(data)))
    transformed_data = tuple(tuple(transform_to_screen_plane(series, bl, tr, width, height) for series in keyframe) for keyframe in data)
    transformed_data = tuple((series + (series[0],) for series in keyframe) for keyframe in transformed_data)
    return svg_wrap(width, height, remove_linebreaks(f"""
        {draw_axes(width, height, bl, tr)}
        {tuple(get_animation_frame(join_serieses_of_points(keyframe, colors.color_generator(), point_size), animation_duration, keytimes, idx) for (idx, keyframe) in enumerate(transformed_data))}
    """))

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
