from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent
REMI_DATA_PATH = ROOT / 'data' / 'remibrutinib_longitudinal_uas7.json'
BARZO_DATA_PATH = ROOT / 'data' / 'barzolvolimab_longitudinal_uas7.json'
RILZA_DATA_PATH = ROOT / 'data' / 'rilzabrutinib_longitudinal_uas7.json'
ASSETS_DIR = ROOT / 'wiki' / 'assets' / 'plots'

BLUE = '#1f5aa6'
GRAY = '#6f7f8f'
GREEN = '#2f8a68'
TEAL = '#3d88a8'
LIGHT_BLUE = '#dbe9f9'
LIGHT_GRAY = '#e8eef5'
INK = '#17212b'
MUTED = '#5c6b7a'
LINE = '#d8e1ec'
BG = '#ffffff'

BARZO_COLOR_MAP = {
    '75 mg Q4W': '#7aa6d8',
    '75 mg Q4W -> 150 mg Q4W / 300 mg Q8W': '#7aa6d8',
    '150 mg Q4W': BLUE,
    '300 mg Q8W': GREEN,
    'placebo': GRAY,
    'placebo -> 150 mg Q4W / 300 mg Q8W': GRAY,
}

RILZA_COLOR_MAP = {
    'placebo': GRAY,
    '400 mg/day': '#8db6e2',
    '800 mg/day': TEAL,
    '1200 mg/day': BLUE,
    '1200 mg/day vs placebo': BLUE,
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def xml_escape(text: object) -> str:
    return (
        str(text)
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
    )


def baseline_map(data: dict) -> dict[tuple[str, str], float]:
    out: dict[tuple[str, str], float] = {}
    for row in data.get('baseline', []):
        if row.get('metric') != 'UAS7':
            continue
        out[(row['trial'], row['arm'])] = row['value']
    return out


def remi_cfb_series(data: dict) -> dict[str, dict[str, list[tuple[int, float]]]]:
    series: dict[str, dict[str, list[tuple[int, float]]]] = {
        'REMIX-1': {'remibrutinib 25 mg BID': [], 'placebo': []},
        'REMIX-2': {'remibrutinib 25 mg BID': [], 'placebo': []},
    }
    for row in data.get('cfb_uas7', []):
        trial = row['trial']
        arm = row['arm']
        series.setdefault(trial, {}).setdefault(arm, []).append((int(row['week']), float(row['ls_mean'])))
    for trial in series:
        for arm in series[trial]:
            series[trial][arm] = sorted(series[trial][arm])
    return series


def remi_absolute_uas7_series(data: dict) -> dict[str, dict[str, list[tuple[int, float]]]]:
    base = baseline_map(data)
    series: dict[str, dict[str, list[tuple[int, float]]]] = {
        'REMIX-1': {'remibrutinib 25 mg BID': [], 'placebo': []},
        'REMIX-2': {'remibrutinib 25 mg BID': [], 'placebo': []},
    }
    for (trial, arm), baseline in base.items():
        series.setdefault(trial, {}).setdefault(arm, []).append((0, baseline))
    for row in data.get('cfb_uas7', []):
        trial = row['trial']
        arm = row['arm']
        baseline = base[(trial, arm)]
        value = baseline + float(row['ls_mean'])
        series.setdefault(trial, {}).setdefault(arm, []).append((int(row['week']), value))
    for trial in series:
        for arm in series[trial]:
            series[trial][arm] = sorted(series[trial][arm])
    return series


def remi_uas7_leq6_series(data: dict) -> dict[str, dict[str, list[tuple[int, float]]]]:
    series: dict[str, dict[str, list[tuple[int, float]]]] = {
        'REMIX-1': {'remibrutinib 25 mg BID': [], 'placebo': []},
        'REMIX-2': {'remibrutinib 25 mg BID': [], 'placebo': []},
    }
    for row in data.get('responder_uas7_leq6', []):
        trial = row['trial']
        arm = row['arm']
        series.setdefault(trial, {}).setdefault(arm, []).append((int(row['week']), float(row['value'])))
    for trial in series:
        for arm in series[trial]:
            series[trial][arm] = sorted(series[trial][arm])
    return series


def pooled_week52(data: dict) -> dict[str, float]:
    out: dict[str, float] = {}
    for row in data.get('band_shift_pooled', []):
        metric = row.get('metric')
        week = row.get('week')
        if week == 52 and metric in {'severe band (UAS7 28-42) %', 'complete response (UAS7=0) %'}:
            out[metric] = float(row['value'])
    return out


def barzo_landmark_series(data: dict, section: str) -> dict[str, list[tuple[int, float]]]:
    order = [
        '75 mg Q4W -> 150 mg Q4W / 300 mg Q8W',
        '150 mg Q4W',
        '300 mg Q8W',
        'placebo -> 150 mg Q4W / 300 mg Q8W',
    ]
    series: dict[str, list[tuple[int, float]]] = {arm: [] for arm in order}
    for row in data.get(section, []):
        arm = row['arm']
        series.setdefault(arm, []).append((int(row['week']), float(row['value'])))
    for arm in series:
        series[arm] = sorted(series[arm])
    return series


def barzo_week12_cfb_rows(data: dict) -> list[dict]:
    order = ['75 mg Q4W', '150 mg Q4W', '300 mg Q8W', 'placebo']
    row_by_arm = {row['arm']: row for row in data.get('cfb_uas7', []) if int(row.get('week', -1)) == 12}
    return [row_by_arm[arm] for arm in order if arm in row_by_arm]


def barzo_week76_complete_response(data: dict) -> float | None:
    for row in data.get('follow_up_landmarks', []):
        if row.get('metric') == 'UAS7=0 %' and int(row.get('week', -1)) == 76:
            return float(row['value'])
    return None


def rilza_cfb_series(data: dict) -> dict[str, list[tuple[int, float]]]:
    order = ['placebo', '400 mg/day', '800 mg/day', '1200 mg/day']
    series: dict[str, list[tuple[int, float]]] = {arm: [] for arm in order}
    for row in data.get('cfb_uas7', []):
        arm = row['arm']
        series.setdefault(arm, []).append((int(row['week']), float(row['ls_mean'])))
    for arm in series:
        series[arm] = sorted(series[arm])
    return series


def rilza_difference_series(data: dict) -> dict[str, list[tuple[int, float]]]:
    series = {'1200 mg/day vs placebo': []}
    for row in data.get('uas7_difference_vs_placebo_1200mg', []):
        series['1200 mg/day vs placebo'].append((int(row['week']), float(row['ls_mean_difference'])))
    series['1200 mg/day vs placebo'] = sorted(series['1200 mg/day vs placebo'])
    return series


def rilza_week12_response_rows(data: dict) -> list[dict]:
    metric_order = ['UAS7 <= 6', 'UAS7 = 0']
    arm_order = ['placebo', '1200 mg/day']
    rows = []
    for metric in metric_order:
        group = [row for row in data.get('week12_response', []) if row.get('metric') == metric]
        row_by_arm = {row['arm']: row for row in group}
        for arm in arm_order:
            if arm in row_by_arm:
                rows.append(row_by_arm[arm])
    return rows


def polyline(points: Iterable[tuple[float, float]], color: str) -> str:
    pts = ' '.join(f'{x:.1f},{y:.1f}' for x, y in points)
    return f"<polyline fill='none' stroke='{color}' stroke-width='3' points='{pts}' />"


def circles(points: Iterable[tuple[float, float]], color: str) -> str:
    return ''.join(
        f"<circle cx='{x:.1f}' cy='{y:.1f}' r='4.5' fill='{color}' stroke='#ffffff' stroke-width='2' />"
        for x, y in points
    )


def text(x: float, y: float, value: str, size: int = 14, weight: str = '400', fill: str = INK, anchor: str = 'start') -> str:
    return f"<text x='{x:.1f}' y='{y:.1f}' font-family='Inter, Arial, sans-serif' font-size='{size}' font-weight='{weight}' fill='{fill}' text-anchor='{anchor}'>{xml_escape(value)}</text>"


def line(x1: float, y1: float, x2: float, y2: float, stroke: str = LINE, width: int = 1, dash: str | None = None) -> str:
    dash_attr = f" stroke-dasharray='{dash}'" if dash else ''
    return f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' stroke='{stroke}' stroke-width='{width}'{dash_attr} />"


def rect(x: float, y: float, w: float, h: float, fill: str, stroke: str = 'none', radius: int = 0) -> str:
    return f"<rect x='{x:.1f}' y='{y:.1f}' width='{w:.1f}' height='{h:.1f}' rx='{radius}' fill='{fill}' stroke='{stroke}' />"


def build_two_panel_line_chart(
    title_str: str,
    subtitle: str,
    series_by_trial: dict[str, dict[str, list[tuple[int, float]]]],
    y_label: str,
    filename: str,
    y_min: float,
    y_max: float,
    week_ticks: list[int],
    note_lines: list[str] | None = None,
):
    width, height = 1160, 620
    panel_w, panel_h = 455, 320
    left1, left2, top = 90, 610, 135
    plot_bottom = top + panel_h

    def x_scale(week: int, left: int) -> float:
        return left + (week - min(week_ticks)) / (max(week_ticks) - min(week_ticks)) * panel_w

    def y_scale(value: float) -> float:
        return top + (y_max - value) / (y_max - y_min) * panel_h

    parts = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>",
        rect(0, 0, width, height, BG),
        text(44, 46, title_str, size=28, weight='700', fill=INK),
        text(44, 74, subtitle, size=15, fill=MUTED),
        rect(870, 32, 16, 16, BLUE, radius=3),
        text(894, 45, 'Remibrutinib 25 mg BID', size=14, fill=INK),
        rect(870, 58, 16, 16, GRAY, radius=3),
        text(894, 71, 'Placebo', size=14, fill=INK),
    ]

    trials = ['REMIX-1', 'REMIX-2']
    lefts = [left1, left2]
    for trial, left in zip(trials, lefts):
        parts.append(rect(left - 24, top - 34, panel_w + 48, panel_h + 70, '#fbfdff', stroke=LINE, radius=14))
        parts.append(text(left, top - 10, trial, size=18, weight='700', fill=INK))
        for y_val in range(int(y_min), int(y_max) + 1, 5):
            y = y_scale(y_val)
            parts.append(line(left, y, left + panel_w, y, stroke=LINE, width=1))
            parts.append(text(left - 10, y + 5, str(y_val), size=12, fill=MUTED, anchor='end'))
        parts.append(line(left, top, left, plot_bottom, stroke=MUTED, width=1))
        parts.append(line(left, plot_bottom, left + panel_w, plot_bottom, stroke=MUTED, width=1))
        for week in week_ticks:
            x = x_scale(week, left)
            parts.append(line(x, plot_bottom, x, plot_bottom + 6, stroke=MUTED, width=1))
            parts.append(text(x, plot_bottom + 24, str(week), size=12, fill=MUTED, anchor='middle'))

        remi_points = [(x_scale(w, left), y_scale(v)) for w, v in series_by_trial[trial]['remibrutinib 25 mg BID']]
        placebo_points = [(x_scale(w, left), y_scale(v)) for w, v in series_by_trial[trial]['placebo']]
        parts.append(polyline(remi_points, BLUE))
        parts.append(polyline(placebo_points, GRAY))
        parts.append(circles(remi_points, BLUE))
        parts.append(circles(placebo_points, GRAY))

    parts.append(text(28, top + panel_h / 2, y_label, size=14, fill=MUTED, anchor='middle'))
    parts.append(f"<g transform='rotate(-90 28 {top + panel_h / 2:.1f})'></g>")
    parts.append(text(left1 + panel_w / 2, plot_bottom + 52, 'Week', size=14, fill=MUTED, anchor='middle'))
    parts.append(text(left2 + panel_w / 2, plot_bottom + 52, 'Week', size=14, fill=MUTED, anchor='middle'))

    if note_lines:
        y = 510
        for note in note_lines:
            parts.append(text(44, y, note, size=13, fill=MUTED))
            y += 20

    parts.append('</svg>')
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / filename).write_text(''.join(parts))


def build_pooled_week52_callout(data: dict, filename: str):
    width, height = 760, 240
    points = pooled_week52(data)
    severe = points.get('severe band (UAS7 28-42) %')
    complete = points.get('complete response (UAS7=0) %')
    parts = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>",
        rect(0, 0, width, height, BG),
        rect(20, 20, width - 40, height - 40, '#fbfdff', stroke=LINE, radius=16),
        text(40, 52, 'REMIX pooled week 52 landmarks (explicit numeric values only)', size=24, weight='700'),
        text(40, 78, 'From the GUF/UCARE 2024 band-shift poster. These are pooled REMIX-1 + REMIX-2 values, not per-trial week 52 curves.', size=14, fill=MUTED),
    ]
    card_y = 110
    card_w = 300
    parts.append(rect(40, card_y, card_w, 84, LIGHT_BLUE, stroke=LINE, radius=14))
    parts.append(text(60, card_y + 30, 'Complete response (UAS7 = 0)', size=17, weight='700'))
    parts.append(text(60, card_y + 62, f'{complete:.1f}%', size=30, weight='700', fill=BLUE))
    parts.append(rect(380, card_y, card_w, 84, LIGHT_GRAY, stroke=LINE, radius=14))
    parts.append(text(400, card_y + 30, 'Still severe (UAS7 28 to 42)', size=17, weight='700'))
    parts.append(text(400, card_y + 62, f'{severe:.1f}%', size=30, weight='700', fill=GRAY))
    parts.append('</svg>')
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / filename).write_text(''.join(parts))


def build_multi_series_landmark_chart(
    title_str: str,
    subtitle: str,
    series_by_arm: dict[str, list[tuple[int, float]]],
    filename: str,
    y_label: str,
    y_min: float,
    y_max: float,
    week_ticks: list[int],
    color_map: dict[str, str],
    legend_order: list[str],
    note_lines: list[str] | None = None,
):
    width, height = 1040, 620
    left, top = 100, 150
    plot_w, plot_h = 820, 310
    plot_bottom = top + plot_h

    def x_scale(week: int) -> float:
        return left + (week - min(week_ticks)) / (max(week_ticks) - min(week_ticks)) * plot_w

    def y_scale(value: float) -> float:
        return top + (y_max - value) / (y_max - y_min) * plot_h

    parts = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>",
        rect(0, 0, width, height, BG),
        text(44, 46, title_str, size=28, weight='700', fill=INK),
        text(44, 74, subtitle, size=15, fill=MUTED),
        rect(left - 24, top - 34, plot_w + 48, plot_h + 78, '#fbfdff', stroke=LINE, radius=14),
    ]

    legend_x, legend_y = 640, 102
    for idx, arm in enumerate(legend_order):
        y = legend_y + idx * 24
        parts.append(rect(legend_x, y - 12, 16, 16, color_map[arm], radius=3))
        parts.append(text(legend_x + 24, y + 1, arm, size=13, fill=INK))

    for y_val in range(int(y_min), int(y_max) + 1, 10):
        y = y_scale(y_val)
        parts.append(line(left, y, left + plot_w, y, stroke=LINE, width=1))
        parts.append(text(left - 10, y + 5, str(y_val), size=12, fill=MUTED, anchor='end'))
    parts.append(line(left, top, left, plot_bottom, stroke=MUTED, width=1))
    parts.append(line(left, plot_bottom, left + plot_w, plot_bottom, stroke=MUTED, width=1))
    for week in week_ticks:
        x = x_scale(week)
        parts.append(line(x, plot_bottom, x, plot_bottom + 6, stroke=MUTED, width=1))
        parts.append(text(x, plot_bottom + 24, str(week), size=12, fill=MUTED, anchor='middle'))

    for arm in legend_order:
        points = [(x_scale(w), y_scale(v)) for w, v in series_by_arm.get(arm, [])]
        if not points:
            continue
        color = color_map[arm]
        parts.append(polyline(points, color))
        parts.append(circles(points, color))

    parts.append(text(30, top + plot_h / 2, y_label, size=14, fill=MUTED, anchor='middle'))
    parts.append(f"<g transform='rotate(-90 30 {top + plot_h / 2:.1f})'></g>")
    parts.append(text(left + plot_w / 2, plot_bottom + 52, 'Week', size=14, fill=MUTED, anchor='middle'))

    if note_lines:
        y = 520
        for note in note_lines:
            parts.append(text(44, y, note, size=13, fill=MUTED))
            y += 20

    parts.append('</svg>')
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / filename).write_text(''.join(parts))


def build_barzo_week12_cfb_bar_chart(data: dict, filename: str):
    rows = barzo_week12_cfb_rows(data)
    width, height = 940, 520
    left, top = 100, 130
    plot_w, plot_h = 740, 250
    plot_bottom = top + plot_h
    bar_w = 110
    min_val, max_val = -30.0, 0.0

    def y_scale(value: float) -> float:
        return top + (max_val - value) / (max_val - min_val) * plot_h

    parts = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>",
        rect(0, 0, width, height, BG),
        text(44, 46, 'Barzolvolimab week 12 UAS7 primary-endpoint snapshot', size=28, weight='700', fill=INK),
        text(44, 74, 'Explicit LS mean change-from-baseline values from the AAAAI 2025 CSU poster for the four core randomized arms.', size=15, fill=MUTED),
        rect(left - 24, top - 34, plot_w + 48, plot_h + 90, '#fbfdff', stroke=LINE, radius=14),
    ]

    for y_val in range(-30, 1, 5):
        y = y_scale(float(y_val))
        parts.append(line(left, y, left + plot_w, y, stroke=LINE, width=1))
        parts.append(text(left - 10, y + 5, str(y_val), size=12, fill=MUTED, anchor='end'))
    parts.append(line(left, top, left, plot_bottom, stroke=MUTED, width=1))
    parts.append(line(left, y_scale(0.0), left + plot_w, y_scale(0.0), stroke=MUTED, width=1))

    gap = (plot_w - len(rows) * bar_w) / (len(rows) + 1)
    zero_y = y_scale(0.0)
    for idx, row in enumerate(rows):
        x = left + gap + idx * (bar_w + gap)
        value = float(row['ls_mean'])
        value_y = y_scale(max(value, min_val))
        bar_y = min(zero_y, value_y)
        h = abs(value_y - zero_y)
        fill = BARZO_COLOR_MAP.get(row['arm'], TEAL)
        parts.append(rect(x, bar_y, bar_w, h, fill, stroke=fill, radius=6))
        parts.append(text(x + bar_w / 2, value_y + 18, f'{value:.2f}', size=14, weight='700', fill=fill, anchor='middle'))
        parts.append(text(x + bar_w / 2, plot_bottom + 30, row['arm'], size=12, fill=INK, anchor='middle'))

    parts.append(text(30, top + plot_h / 2, 'LS mean UAS7 CFB', size=14, fill=MUTED, anchor='middle'))
    parts.append(f"<g transform='rotate(-90 30 {top + plot_h / 2:.1f})'></g>")
    parts.append(text(44, 450, 'The week-12 values are a clean randomized-arm comparison. Later week-52 landmarks shift to post-week-16 transition groups.', size=13, fill=MUTED))
    parts.append('</svg>')
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / filename).write_text(''.join(parts))


def build_barzo_week76_callout(data: dict, filename: str):
    value = barzo_week76_complete_response(data)
    if value is None:
        return
    width, height = 760, 240
    parts = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>",
        rect(0, 0, width, height, BG),
        rect(20, 20, width - 40, height - 40, '#fbfdff', stroke=LINE, radius=16),
        text(40, 52, 'Barzolvolimab post-treatment follow-up landmark', size=24, weight='700'),
        text(40, 78, 'The current cached sponsor summary gives a high-level week-76 complete-response landmark, but not a clean regimen-resolved denominator table.', size=14, fill=MUTED),
        rect(40, 110, 300, 84, LIGHT_BLUE, stroke=LINE, radius=14),
        text(60, 140, 'Week 76 complete response (UAS7 = 0)', size=17, weight='700'),
        text(60, 172, f'Up to {value:.1f}%', size=30, weight='700', fill=BLUE),
        rect(380, 110, 300, 84, LIGHT_GRAY, stroke=LINE, radius=14),
        text(400, 140, 'Interpretation status', size=17, weight='700'),
        text(400, 172, 'Sponsor summary only', size=24, weight='700', fill=GRAY),
        '</svg>',
    ]
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / filename).write_text(''.join(parts))


def build_rilza_week12_response_chart(data: dict, filename: str):
    rows = rilza_week12_response_rows(data)
    width, height = 980, 560
    left, top = 120, 140
    plot_w, plot_h = 720, 260
    plot_bottom = top + plot_h
    bar_w = 120
    group_gap = 120
    arm_gap = 24
    max_val = 40.0

    def y_scale(value: float) -> float:
        return top + (max_val - value) / max_val * plot_h

    parts = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>",
        rect(0, 0, width, height, BG),
        text(44, 46, 'Rilzabrutinib week 12 response snapshot', size=28, weight='700', fill=INK),
        text(44, 74, 'Explicit week-12 responder landmarks from PMCID PMC12019677 Table 2, comparing placebo with rilzabrutinib 1200 mg/day in the primary analysis population.', size=15, fill=MUTED),
        rect(left - 24, top - 34, plot_w + 48, plot_h + 110, '#fbfdff', stroke=LINE, radius=14),
        rect(720, 112, 16, 16, GRAY, radius=3),
        text(744, 125, 'Placebo', size=14, fill=INK),
        rect(720, 138, 16, 16, BLUE, radius=3),
        text(744, 151, 'Rilzabrutinib 1200 mg/day', size=14, fill=INK),
    ]

    for y_val in range(0, 41, 10):
        y = y_scale(float(y_val))
        parts.append(line(left, y, left + plot_w, y, stroke=LINE, width=1))
        parts.append(text(left - 10, y + 5, str(y_val), size=12, fill=MUTED, anchor='end'))
    parts.append(line(left, top, left, plot_bottom, stroke=MUTED, width=1))
    parts.append(line(left, plot_bottom, left + plot_w, plot_bottom, stroke=MUTED, width=1))

    groups = ['UAS7 <= 6', 'UAS7 = 0']
    row_map = {(row['metric'], row['arm']): row for row in rows}
    start_x = left + 90
    for idx, metric in enumerate(groups):
        group_left = start_x + idx * (2 * bar_w + arm_gap + group_gap)
        for arm_idx, arm in enumerate(['placebo', '1200 mg/day']):
            row = row_map[(metric, arm)]
            x = group_left + arm_idx * (bar_w + arm_gap)
            value = float(row['value'])
            y = y_scale(value)
            fill = RILZA_COLOR_MAP[arm]
            parts.append(rect(x, y, bar_w, plot_bottom - y, fill, stroke=fill, radius=6))
            parts.append(text(x + bar_w / 2, y - 10, f'{value:.1f}%', size=14, weight='700', fill=fill, anchor='middle'))
            label = 'Placebo' if arm == 'placebo' else '1200 mg/day'
            parts.append(text(x + bar_w / 2, plot_bottom + 24, label, size=12, fill=INK, anchor='middle'))
        parts.append(text(group_left + bar_w + arm_gap / 2, plot_bottom + 54, metric, size=14, weight='700', fill=INK, anchor='middle'))

    parts.append(text(32, top + plot_h / 2, 'Patients (%)', size=14, fill=MUTED, anchor='middle'))
    parts.append(f"<g transform='rotate(-90 32 {top + plot_h / 2:.1f})'></g>")
    parts.append(text(44, 470, 'UAS7 <= 6 separates clearly at week 12; complete-response separation is numerically favorable but less definitive in this phase 2 dataset.', size=13, fill=MUTED))
    parts.append('</svg>')
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / filename).write_text(''.join(parts))


def main():
    remi_data = load_json(REMI_DATA_PATH)
    absolute_series = remi_absolute_uas7_series(remi_data)
    responder_series = remi_uas7_leq6_series(remi_data)

    build_two_panel_line_chart(
        title_str='Remibrutinib longitudinal UAS7, first pass',
        subtitle='Derived mean UAS7 = explicit baseline UAS7 plus explicit sponsor-portal change-from-baseline values. REMIX-1 and REMIX-2 shown separately.',
        series_by_trial=absolute_series,
        y_label='Derived mean UAS7',
        filename='remibrutinib-uas7-absolute-first-pass.svg',
        y_min=0,
        y_max=32,
        week_ticks=[0, 1, 2, 4, 12, 24],
        note_lines=[
            'Explicit numeric anchors are available through week 24. Week 52 mean UAS7 is not yet plotted because the current local extraction only gives graphical, not tabulated, values.',
            'Source backbone: ACAAI 2024 early symptom improvement poster plus baseline values from the same sponsor-hosted extraction.',
        ],
    )

    build_two_panel_line_chart(
        title_str='Remibrutinib UAS7 ≤ 6 response over time, first pass',
        subtitle='Explicit numeric responder rates extracted from the EADV 2024 52-week oral presentation. REMIX-1 and REMIX-2 shown separately.',
        series_by_trial=responder_series,
        y_label='Patients with UAS7 ≤ 6 (%)',
        filename='remibrutinib-uas7-leq6-first-pass.svg',
        y_min=0,
        y_max=60,
        week_ticks=[1, 2, 12, 24],
        note_lines=[
            'Week 52 UAS7 ≤ 6 per-trial numeric values are not yet tabulated in the current local extraction, so the plot stops at week 24.',
            'A pooled week 52 callout is provided separately where explicit values exist.',
        ],
    )

    build_pooled_week52_callout(remi_data, 'remibrutinib-week52-pooled-landmarks.svg')

    barzo_data = load_json(BARZO_DATA_PATH)
    barzo_uas7_leq6 = barzo_landmark_series(barzo_data, 'responder_uas7_leq6')
    barzo_uas7_zero = barzo_landmark_series(barzo_data, 'complete_response_uas7_0')
    legend_order = [
        '75 mg Q4W -> 150 mg Q4W / 300 mg Q8W',
        '150 mg Q4W',
        '300 mg Q8W',
        'placebo -> 150 mg Q4W / 300 mg Q8W',
    ]

    build_multi_series_landmark_chart(
        title_str='Barzolvolimab UAS7 ≤ 6 landmarks, first pass',
        subtitle='Explicit week-12 and week-52 values from the EADV 2024 congress presentation. These are landmark response rates, not a fully tabulated weekly curve.',
        series_by_arm=barzo_uas7_leq6,
        filename='barzolvolimab-uas7-leq6-landmarks.svg',
        y_label='Patients with UAS7 ≤ 6 (%)',
        y_min=0,
        y_max=80,
        week_ticks=[12, 52],
        color_map=BARZO_COLOR_MAP,
        legend_order=legend_order,
        note_lines=[
            'The week-52 values reflect post-week-16 transition groups for the prior 75 mg and placebo arms.',
            'The full over-time UAS7 curve is still graph-only in the current local extraction.',
        ],
    )

    build_multi_series_landmark_chart(
        title_str='Barzolvolimab complete response (UAS7 = 0), first pass',
        subtitle='Explicit week-12 and week-52 complete-response values from the manuscript-backed phase 2 sponsor/manuscript layer.',
        series_by_arm=barzo_uas7_zero,
        filename='barzolvolimab-uas7-complete-response-landmarks.svg',
        y_label='Patients with UAS7 = 0 (%)',
        y_min=0,
        y_max=80,
        week_ticks=[12, 52],
        color_map=BARZO_COLOR_MAP,
        legend_order=legend_order,
        note_lines=[
            'Week-12 complete-response values are also consistent with the phase 2 manuscript abstract.',
            'Week-76 follow-up is shown separately because the current sponsor summary is not regimen-resolved.',
        ],
    )

    build_barzo_week12_cfb_bar_chart(barzo_data, 'barzolvolimab-week12-uas7-cfb.svg')
    build_barzo_week76_callout(barzo_data, 'barzolvolimab-week76-complete-response-callout.svg')

    rilza_data = load_json(RILZA_DATA_PATH)
    rilza_cfb = rilza_cfb_series(rilza_data)
    rilza_diff = rilza_difference_series(rilza_data)

    build_multi_series_landmark_chart(
        title_str='Rilzabrutinib UAS7 change from baseline landmarks, first pass',
        subtitle='Explicit randomized-arm week-4 and week-12 LS mean change-from-baseline values from PMCID PMC12019677 Table 2.',
        series_by_arm=rilza_cfb,
        filename='rilzabrutinib-uas7-cfb-landmarks.svg',
        y_label='LS mean UAS7 CFB',
        y_min=-20,
        y_max=0,
        week_ticks=[4, 12],
        color_map=RILZA_COLOR_MAP,
        legend_order=['placebo', '400 mg/day', '800 mg/day', '1200 mg/day'],
        note_lines=[
            'This is a landmark plot, not a weekly curve. The current local numeric layer gives clean arm-resolved UAS7 CFB at weeks 4 and 12 only.',
            'Week-1 onset is shown separately as an explicit 1200 mg/day versus placebo difference landmark because full per-arm week-1 means are not safely tabulated locally.',
        ],
    )

    build_multi_series_landmark_chart(
        title_str='Rilzabrutinib high-dose early-onset UAS7 difference, first pass',
        subtitle='Explicit LS mean difference versus placebo for rilzabrutinib 1200 mg/day from PMCID PMC12019677, covering weeks 1, 4, and 12.',
        series_by_arm=rilza_diff,
        filename='rilzabrutinib-uas7-difference-vs-placebo.svg',
        y_label='LS mean difference in UAS7 CFB',
        y_min=-15,
        y_max=0,
        week_ticks=[1, 4, 12],
        color_map=RILZA_COLOR_MAP,
        legend_order=['1200 mg/day vs placebo'],
        note_lines=[
            'The most defensible early-onset rilzabrutinib numeric path in the current cache is the high-dose versus placebo contrast, not a four-arm week-by-week mean curve.',
        ],
    )

    build_rilza_week12_response_chart(rilza_data, 'rilzabrutinib-week12-response.svg')
    print('Built remibrutinib, barzolvolimab, and rilzabrutinib longitudinal UAS7 SVG plots')


if __name__ == '__main__':
    main()
