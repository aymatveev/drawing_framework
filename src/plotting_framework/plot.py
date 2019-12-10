from typing import Iterable, Tuple

def remove_linebreaks(s: str) -> str:
    return "".join(s.split("\n"))

def shift_data(data: Iterable[Tuple[float, float]], offset: Tuple[float, float]) -> Iterable[Tuple[float, float]]:
    return ((p[0] - offset[0], p[1] - offset[1]) for p in data)

def scale_data(data: Iterable[Tuple[float, float]], scale: Tuple[float, float]) -> Iterable[Tuple[float, float]]:
    return ((p[0] * scale[0], p[1] * scale[1]) for p in data)

def mark_point(point: Tuple[int, int]) -> str:
    return f"""<circle cx="{point[0]}" cy="{point[1]}" r="3"/>"""

def scatter(data: Iterable[Tuple[float, float]], bl: Tuple[float, float], tr: Tuple[float, float]) -> str:
    width = 640
    height = 480

    middle = ((bl[0] + tr[0]) / 2, (bl[1] + tr[1]) / 2)
    viewport_middle = (- width / 2, - height / 2)

    scale = (width / abs(bl[0] - tr[0]), height / abs(bl[1] - tr[1]))

    centered_data: Iterable[Tuple[float, float]] = shift_data(data, middle)
    scaled_data: Iterable[Tuple[float, float]] = scale_data(centered_data, scale)
    shifted_data: Iterable[Tuple[float, float]] = shift_data(scaled_data, viewport_middle)
    scaled_data_int: Iterable[Tuple[int, int]] = ((round(p[0]), round(p[1])) for p in shifted_data)
    flipped_y_data: Iterable[Tuple[int, int]] = ((p[0], height - p[1]) for p in scaled_data_int)

    result = remove_linebreaks(f"""
    <svg width="{width}" height="{height}">
        <line x1="0" y1="{height}" x2="{width}" y2="{height}" stroke="black" />
        <line x1="0" y1="0" x2="0" y2="{height}" stroke="black" />
        <text x="10" y="{height - 10}" class="small">{bl}</text>
        <text x="{width - 80}" y="{15}" class="small">{tr}</text>
        { "".join(mark_point(p) for p in flipped_y_data) }
    </svg>
    """)

    return result