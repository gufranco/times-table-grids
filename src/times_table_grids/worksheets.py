from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

from times_table_grids.locales import Locale

TABLES = range(1, 11)
FACTORS = range(1, 11)
GRID_SIZE = 10
GROUP_SIZE = 5
SLOT_COLUMNS = 3
SLOT_ROWS = 4
GUIDE_SLOTS = 2
MARGIN = 12 * mm
HEADER_HEIGHT = 14 * mm
LABEL_HEIGHT = 9 * mm
AXIS_SPACE = 4 * mm
CELL = 4.8 * mm
GUIDE_CELL = 4 * mm
BLACK = 0.0
TEXT_GRAY = 0.35
AXIS_GRAY = 0.5
BOLD = "Helvetica-Bold"
REGULAR = "Helvetica"
TITLE_SIZE = 22
TIMES = "×"
CONTENT_TOP = A4[1] - MARGIN - HEADER_HEIGHT
SLOT_WIDTH = (A4[0] - 2 * MARGIN) / SLOT_COLUMNS
SLOT_HEIGHT = (CONTENT_TOP - MARGIN) / SLOT_ROWS
EXAMPLE_ROWS, EXAMPLE_COLS, EXAMPLE_GRID = 2, 3, 5


class GuideText(Protocol):
    @property
    def guide_title(self) -> str: ...
    @property
    def guide_steps(self) -> tuple[str, str, str, str]: ...
    @property
    def guide_tip(self) -> str: ...
    @property
    def example_label(self) -> str: ...


@dataclass(frozen=True, slots=True)
class Exercise:
    table: int
    factor: int


@dataclass(frozen=True, slots=True)
class LineStyle:
    width: float
    gray: float


@dataclass(frozen=True, slots=True)
class Slot:
    left: float
    top: float
    grid_left: float
    grid_top: float
    cell: float


THIN_LINE = LineStyle(width=0.5, gray=0.6)
GROUP_LINE = LineStyle(width=1.2, gray=0.25)


def exercises_for(table: int) -> list[Exercise]:
    return [Exercise(table, factor) for factor in FACTORS]


def slot_at(index: int) -> Slot:
    row, col = divmod(index, SLOT_COLUMNS)
    left = MARGIN + col * SLOT_WIDTH
    top = CONTENT_TOP - row * SLOT_HEIGHT
    grid_left = left + AXIS_SPACE
    grid_top = top - LABEL_HEIGHT - AXIS_SPACE
    return Slot(left=left, top=top, grid_left=grid_left, grid_top=grid_top, cell=CELL)


def exercise_slots() -> list[Slot]:
    return [slot_at(index) for index in range(GUIDE_SLOTS, SLOT_COLUMNS * SLOT_ROWS)]


def grid_line_styles(size: int) -> tuple[LineStyle, ...]:
    return tuple(
        GROUP_LINE if index % GROUP_SIZE == 0 or index == size else THIN_LINE
        for index in range(size + 1)
    )


def draw_grid(canvas: Canvas, left: float, top: float, size: int, cell: float) -> None:
    side = size * cell
    for index, style in enumerate(grid_line_styles(size)):
        canvas.setLineWidth(style.width)
        canvas.setStrokeGray(style.gray)
        canvas.line(left, top - index * cell, left + side, top - index * cell)
        canvas.line(left + index * cell, top, left + index * cell, top - side)


def draw_axis_numbers(
    canvas: Canvas, left: float, top: float, size: int, cell: float
) -> None:
    canvas.setFont(REGULAR, 6)
    canvas.setFillGray(AXIS_GRAY)
    for number in range(1, size + 1):
        center = (number - 0.5) * cell
        canvas.drawCentredString(left + center, top + 1.2 * mm, str(number))
        canvas.drawRightString(left - 1 * mm, top - center - 2, str(number))


def draw_marks(canvas: Canvas, left: float, top: float, rows: int, cols: int) -> None:
    pad = GUIDE_CELL * 0.22
    canvas.setStrokeGray(BLACK)
    canvas.setLineWidth(0.8)
    for row in range(rows):
        for col in range(cols):
            x0, y0 = left + col * GUIDE_CELL + pad, top - row * GUIDE_CELL - pad
            x1, y1 = x0 + GUIDE_CELL - 2 * pad, y0 - GUIDE_CELL + 2 * pad
            canvas.line(x0, y0, x1, y1)
            canvas.line(x0, y1, x1, y0)


def draw_answer_box(canvas: Canvas, left: float, baseline: float, answer: str) -> None:
    canvas.setStrokeGray(BLACK)
    canvas.setLineWidth(0.8)
    canvas.roundRect(left, baseline - 2.5 * mm, 13 * mm, 8 * mm, 1.5 * mm)
    canvas.setFillGray(BLACK)
    canvas.drawCentredString(left + 6.5 * mm, baseline, answer)


def times_equation(rows: int, cols: int) -> str:
    return f"{rows} {TIMES} {cols} ="


def draw_equation(canvas: Canvas, left: float, baseline: float, equation: str) -> float:
    canvas.setFont(BOLD, 14)
    canvas.setFillGray(BLACK)
    canvas.drawString(left, baseline, equation)
    return left + canvas.stringWidth(equation, BOLD, 14) + 1.5 * mm


def draw_hint(
    canvas: Canvas, left: float, baseline: float, exercise: Exercise, locale: Locale
) -> None:
    canvas.setFont(REGULAR, 7)
    canvas.setFillGray(TEXT_GRAY)
    canvas.drawString(left, baseline + 2.2 * mm, locale.rows_label(exercise.table))
    canvas.drawString(left, baseline - 0.8 * mm, locale.columns_label(exercise.factor))


def draw_exercise(
    canvas: Canvas, slot: Slot, exercise: Exercise, locale: Locale
) -> None:
    baseline = slot.top - 6 * mm
    equation = times_equation(exercise.table, exercise.factor)
    box_left = draw_equation(canvas, slot.left, baseline, equation)
    draw_answer_box(canvas, box_left, baseline, "")
    draw_hint(canvas, box_left + 15 * mm, baseline, exercise, locale)
    draw_axis_numbers(canvas, slot.grid_left, slot.grid_top, GRID_SIZE, slot.cell)
    draw_grid(canvas, slot.grid_left, slot.grid_top, GRID_SIZE, slot.cell)


def draw_guide_text(canvas: Canvas, left: float, top: float, locale: GuideText) -> None:
    canvas.setFillGray(BLACK)
    canvas.setFont(BOLD, 13)
    canvas.drawString(left, top - 9 * mm, locale.guide_title)
    canvas.setFont(REGULAR, 9.5)
    for index, step in enumerate(locale.guide_steps):
        canvas.drawString(left, top - (17 + index * 7) * mm, step)
    canvas.setFont(REGULAR, 8.5)
    canvas.setFillGray(TEXT_GRAY)
    canvas.drawString(left, top - 47 * mm, locale.guide_tip)


def draw_example_heading(
    canvas: Canvas, left: float, top: float, label: str, equation: str, answer: int
) -> None:
    canvas.setFont(BOLD, 10)
    canvas.setFillGray(BLACK)
    canvas.drawString(left, top - 9 * mm, label)
    baseline = top - 17 * mm
    box_left = draw_equation(canvas, left, baseline, equation)
    draw_answer_box(canvas, box_left, baseline, str(answer))


def draw_guide_example(canvas: Canvas, left: float, top: float, locale: Locale) -> None:
    equation = times_equation(EXAMPLE_ROWS, EXAMPLE_COLS)
    answer = EXAMPLE_ROWS * EXAMPLE_COLS
    draw_example_heading(canvas, left, top, locale.example_label, equation, answer)
    grid_left, grid_top = left + AXIS_SPACE, top - 27 * mm
    draw_axis_numbers(canvas, grid_left, grid_top, EXAMPLE_GRID, GUIDE_CELL)
    draw_grid(canvas, grid_left, grid_top, EXAMPLE_GRID, GUIDE_CELL)
    draw_marks(canvas, grid_left, grid_top, EXAMPLE_ROWS, EXAMPLE_COLS)


def draw_guide_frame(canvas: Canvas) -> float:
    width = GUIDE_SLOTS * SLOT_WIDTH - 4 * mm
    height = SLOT_HEIGHT - 6 * mm
    canvas.setStrokeGray(AXIS_GRAY)
    canvas.setLineWidth(0.7)
    canvas.setDash(3, 2)
    canvas.roundRect(MARGIN, CONTENT_TOP - height, width, height, 3 * mm)
    canvas.setDash()
    return MARGIN + width - 40 * mm


def draw_guide(canvas: Canvas, locale: Locale) -> None:
    example_left = draw_guide_frame(canvas)
    draw_guide_text(canvas, MARGIN + 4 * mm, CONTENT_TOP, locale)
    draw_guide_example(canvas, example_left, CONTENT_TOP, locale)


def draw_header(canvas: Canvas, title: str, name_label: str) -> None:
    baseline = A4[1] - MARGIN - 8 * mm
    name_line = f"{name_label} ______________________"
    room = A4[0] - 2 * MARGIN - canvas.stringWidth(name_line, REGULAR, 11) - 6 * mm
    size = min(
        TITLE_SIZE, TITLE_SIZE * room / canvas.stringWidth(title, BOLD, TITLE_SIZE)
    )
    canvas.setFillGray(BLACK)
    canvas.setFont(BOLD, size)
    canvas.drawString(MARGIN, baseline, title)
    canvas.setFont(REGULAR, 11)
    canvas.drawRightString(A4[0] - MARGIN, baseline, name_line)


def draw_page(canvas: Canvas, table: int, locale: Locale) -> None:
    draw_header(canvas, locale.title_for(table), locale.name_label)
    draw_guide(canvas, locale)
    for slot, exercise in zip(exercise_slots(), exercises_for(table), strict=True):
        draw_exercise(canvas, slot, exercise, locale)
    canvas.showPage()


def build(output: Path, locale: Locale) -> None:
    canvas = Canvas(str(output), pagesize=A4, invariant=True)
    canvas.setTitle(locale.document_title)
    for table in TABLES:
        draw_page(canvas, table, locale)
    canvas.save()
