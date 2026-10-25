from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

from times_table_grids.geometry import (
    SOLIDS,
    Point2,
    Solid,
    hidden_edges,
    project,
    solid_named,
)
from times_table_grids.solids_locales import Definition, SolidsLocale
from times_table_grids.worksheets import (
    AXIS_GRAY,
    BLACK,
    BOLD,
    CONTENT_TOP,
    MARGIN,
    REGULAR,
    TEXT_GRAY,
    draw_header,
)

HIDDEN_GRAY = 0.45
HATCH_GRAY = 0.7
HATCH_STEP = 2.2 * mm
COUNT_COLUMNS = 2
COUNT_ROWS = 3
FRONT_FACE, FRONT_TOP_LEFT, EDGE_ENDS = 0, 3, (1, 2)
PAGE_WIDTH = A4[0]


def fit_box(
    points: list[Point2], left: float, bottom: float, width: float, height: float
) -> list[Point2]:
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    span_x, span_y = max(xs) - min(xs), max(ys) - min(ys)
    scale = min(width / span_x, height / span_y)
    offset_x = left + (width - span_x * scale) / 2 - min(xs) * scale
    offset_y = bottom + (height - span_y * scale) / 2 - min(ys) * scale
    return [(offset_x + x * scale, offset_y + y * scale) for x, y in points]


def place(
    solid: Solid, left: float, bottom: float, width: float, height: float
) -> list[Point2]:
    return fit_box([project(v) for v in solid.vertices], left, bottom, width, height)


def draw_solid(
    canvas: Canvas, solid: Solid, points: list[Point2], width: float
) -> None:
    hidden = set(hidden_edges(solid))
    for first, second in solid.edges:
        is_hidden = (first, second) in hidden
        canvas.setStrokeGray(HIDDEN_GRAY if is_hidden else BLACK)
        canvas.setLineWidth(width * 0.7 if is_hidden else width)
        canvas.setDash(3, 2) if is_hidden else canvas.setDash()
        canvas.line(*points[first], *points[second])
    canvas.setDash()


def hatch_face(canvas: Canvas, outline: list[Point2]) -> None:
    xs, ys = [p[0] for p in outline], [p[1] for p in outline]
    canvas.saveState()
    path = canvas.beginPath()
    path.moveTo(*outline[0])
    for point in outline[1:]:
        path.lineTo(*point)
    path.close()
    canvas.clipPath(path, stroke=0, fill=0)
    canvas.setStrokeGray(HATCH_GRAY)
    canvas.setLineWidth(0.5)
    span = (max(xs) - min(xs)) + (max(ys) - min(ys))
    for step in range(int(span // HATCH_STEP) + 1):
        start = min(xs) + step * HATCH_STEP
        canvas.line(start, min(ys), start - (max(ys) - min(ys)), max(ys))
    canvas.restoreState()


def callout(canvas: Canvas, target: Point2, label_at: Point2, text: str) -> None:
    canvas.setStrokeGray(AXIS_GRAY)
    canvas.setLineWidth(0.6)
    canvas.line(*target, *label_at)
    canvas.setFillGray(BLACK)
    canvas.setFont(BOLD, 12)
    canvas.drawString(label_at[0] + 1 * mm, label_at[1] - 1.5 * mm, text)


def draw_labeled_cube(
    canvas: Canvas, left: float, bottom: float, locale: SolidsLocale
) -> None:
    cube = solid_named("cube")
    points = place(cube, left, bottom, 62 * mm, 62 * mm)
    hatch_face(canvas, [points[i] for i in cube.faces[FRONT_FACE]])
    draw_solid(canvas, cube, points, 1.4)
    canvas.setStrokeGray(BLACK)
    canvas.setLineWidth(3.2)
    canvas.line(*points[EDGE_ENDS[0]], *points[EDGE_ENDS[1]])
    canvas.setFillGray(BLACK)
    vertex = points[FRONT_TOP_LEFT]
    canvas.circle(*vertex, 1.8 * mm, stroke=0, fill=1)
    face_center = (points[0][0] + 10 * mm, points[0][1] + 10 * mm)
    callout(canvas, face_center, (left - 4 * mm, bottom - 6 * mm), locale.face[0])
    edge_mid = ((points[1][0] + points[2][0]) / 2, (points[1][1] + points[2][1]) / 2)
    callout(
        canvas, edge_mid, (edge_mid[0] + 22 * mm, edge_mid[1] - 18 * mm), locale.edge[0]
    )
    callout(
        canvas, vertex, (vertex[0] - 10 * mm, vertex[1] + 12 * mm), locale.vertex[0]
    )


def draw_definition(
    canvas: Canvas, left: float, top: float, definition: Definition
) -> None:
    term, meaning, example = definition
    canvas.setFillGray(BLACK)
    canvas.setFont(BOLD, 15)
    canvas.drawString(left, top, term)
    canvas.setFont(REGULAR, 10.5)
    canvas.drawString(left, top - 6 * mm, meaning)
    canvas.setFillGray(TEXT_GRAY)
    canvas.drawString(left, top - 11 * mm, example)


def draw_lines(
    canvas: Canvas, left: float, top: float, lines: tuple[str, ...], gap: float
) -> None:
    for index, line in enumerate(lines):
        canvas.drawString(left, top - index * gap, line)


def draw_try_it(canvas: Canvas, top: float, locale: SolidsLocale) -> None:
    canvas.setFillGray(BLACK)
    canvas.setFont(BOLD, 14)
    canvas.drawString(MARGIN, top, locale.try_title)
    cube = solid_named("cube")
    draw_solid(
        canvas, cube, place(cube, MARGIN + 6 * mm, top - 62 * mm, 50 * mm, 50 * mm), 1.2
    )
    canvas.setFont(REGULAR, 12)
    draw_lines(canvas, MARGIN + 80 * mm, top - 22 * mm, locale.try_steps, 10 * mm)


def draw_tips(canvas: Canvas, top: float, locale: SolidsLocale) -> None:
    width = PAGE_WIDTH - 2 * MARGIN
    canvas.setStrokeGray(AXIS_GRAY)
    canvas.setLineWidth(0.7)
    canvas.setDash(3, 2)
    canvas.roundRect(MARGIN, top - 30 * mm, width, 30 * mm, 3 * mm)
    canvas.setDash()
    canvas.setFillGray(BLACK)
    canvas.setFont(REGULAR, 10.5)
    draw_lines(canvas, MARGIN + 5 * mm, top - 9 * mm, locale.tips, 7.5 * mm)


def draw_lesson_page(canvas: Canvas, locale: SolidsLocale) -> None:
    draw_header(canvas, locale.lesson_title, locale.name_label)
    draw_labeled_cube(canvas, MARGIN + 12 * mm, CONTENT_TOP - 82 * mm, locale)
    definitions = (locale.face, locale.edge, locale.vertex)
    for index, definition in enumerate(definitions):
        draw_definition(
            canvas, MARGIN + 105 * mm, CONTENT_TOP - (12 + index * 25) * mm, definition
        )
    draw_try_it(canvas, CONTENT_TOP - 112 * mm, locale)
    draw_tips(canvas, CONTENT_TOP - 190 * mm, locale)
    canvas.showPage()


def draw_count_boxes(
    canvas: Canvas, left: float, top: float, labels: tuple[str, ...]
) -> None:
    canvas.setStrokeGray(BLACK)
    canvas.setLineWidth(0.8)
    for index, label in enumerate(labels):
        baseline = top - index * 13 * mm
        canvas.setFillGray(BLACK)
        canvas.setFont(REGULAR, 11)
        canvas.drawString(left, baseline, label)
        canvas.roundRect(left + 20 * mm, baseline - 3 * mm, 14 * mm, 9 * mm, 1.5 * mm)


def draw_count_slot(
    canvas: Canvas, solid: Solid, left: float, top: float, locale: SolidsLocale
) -> None:
    canvas.setFillGray(BLACK)
    canvas.setFont(BOLD, 12)
    canvas.drawString(left, top, locale.solid_names[solid.key])
    points = place(solid, left + 2 * mm, top - 52 * mm, 42 * mm, 42 * mm)
    draw_solid(canvas, solid, points, 1.2)
    draw_count_boxes(canvas, left + 50 * mm, top - 16 * mm, locale.count_labels)


def draw_count_page(canvas: Canvas, locale: SolidsLocale) -> None:
    draw_header(canvas, locale.count_title, locale.name_label)
    canvas.setFillGray(TEXT_GRAY)
    canvas.setFont(REGULAR, 10.5)
    canvas.drawString(MARGIN, CONTENT_TOP - 2 * mm, locale.count_instruction)
    column_width = (PAGE_WIDTH - 2 * MARGIN) / COUNT_COLUMNS
    for index, solid in enumerate(SOLIDS):
        row, col = divmod(index, COUNT_COLUMNS)
        left = MARGIN + col * column_width
        draw_count_slot(canvas, solid, left, CONTENT_TOP - (14 + row * 82) * mm, locale)
    canvas.showPage()


def build_solids(output: Path, locale: SolidsLocale) -> None:
    canvas = Canvas(str(output), pagesize=A4, invariant=True)
    canvas.setTitle(locale.document_title)
    draw_lesson_page(canvas, locale)
    draw_count_page(canvas, locale)
    canvas.save()
