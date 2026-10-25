import random
from dataclasses import dataclass
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

from times_table_grids.division_locales import DivisionLocale
from times_table_grids.worksheets import (
    AXIS_SPACE,
    CONTENT_TOP,
    GRID_SIZE,
    GUIDE_CELL,
    MARGIN,
    REGULAR,
    TEXT_GRAY,
    Slot,
    draw_answer_box,
    draw_axis_numbers,
    draw_equation,
    draw_example_heading,
    draw_grid,
    draw_guide_frame,
    draw_guide_text,
    draw_header,
    draw_marks,
    exercise_slots,
)

DIVISORS = range(1, 11)
QUOTIENTS = range(1, 11)
DIVIDE = "÷"
EXAMPLE_DIVISOR, EXAMPLE_QUOTIENT, EXAMPLE_GRID = 3, 2, 5


@dataclass(frozen=True, slots=True)
class Division:
    divisor: int
    quotient: int

    @property
    def dividend(self) -> int:
        return self.divisor * self.quotient

    @property
    def equation(self) -> str:
        return f"{self.dividend} {DIVIDE} {self.divisor} ="


def divisions_for(divisor: int) -> list[Division]:
    quotients = random.Random(divisor).sample(list(QUOTIENTS), len(QUOTIENTS))
    return [Division(divisor, quotient) for quotient in quotients]


def draw_hint(
    canvas: Canvas,
    left: float,
    baseline: float,
    division: Division,
    locale: DivisionLocale,
) -> None:
    canvas.setFont(REGULAR, 7)
    canvas.setFillGray(TEXT_GRAY)
    canvas.drawString(left, baseline + 2.2 * mm, locale.total_label(division.dividend))
    canvas.drawString(left, baseline - 0.8 * mm, locale.per_row_label(division.divisor))


def draw_division(
    canvas: Canvas, slot: Slot, division: Division, locale: DivisionLocale
) -> None:
    baseline = slot.top - 6 * mm
    box_left = draw_equation(canvas, slot.left, baseline, division.equation)
    draw_answer_box(canvas, box_left, baseline, "")
    draw_hint(canvas, box_left + 15 * mm, baseline, division, locale)
    draw_axis_numbers(canvas, slot.grid_left, slot.grid_top, GRID_SIZE, slot.cell)
    draw_grid(canvas, slot.grid_left, slot.grid_top, GRID_SIZE, slot.cell)


def draw_guide_example(
    canvas: Canvas, left: float, top: float, locale: DivisionLocale
) -> None:
    example = Division(EXAMPLE_DIVISOR, EXAMPLE_QUOTIENT)
    draw_example_heading(
        canvas, left, top, locale.example_label, example.equation, example.quotient
    )
    grid_left, grid_top = left + AXIS_SPACE, top - 27 * mm
    draw_axis_numbers(canvas, grid_left, grid_top, EXAMPLE_GRID, GUIDE_CELL)
    draw_grid(canvas, grid_left, grid_top, EXAMPLE_GRID, GUIDE_CELL)
    draw_marks(canvas, grid_left, grid_top, example.quotient, example.divisor)


def draw_page(canvas: Canvas, divisor: int, locale: DivisionLocale) -> None:
    draw_header(canvas, locale.title_for(divisor), locale.name_label)
    example_left = draw_guide_frame(canvas)
    draw_guide_text(canvas, MARGIN + 4 * mm, CONTENT_TOP, locale)
    draw_guide_example(canvas, example_left, CONTENT_TOP, locale)
    for slot, division in zip(exercise_slots(), divisions_for(divisor), strict=True):
        draw_division(canvas, slot, division, locale)
    canvas.showPage()


def build_division(output: Path, locale: DivisionLocale) -> None:
    canvas = Canvas(str(output), pagesize=A4, invariant=True)
    canvas.setTitle(locale.document_title)
    for divisor in DIVISORS:
        draw_page(canvas, divisor, locale)
    canvas.save()
