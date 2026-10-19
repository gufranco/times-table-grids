import re
from pathlib import Path

import pytest

from times_table_grids.locales import EN, LOCALES, PT_BR, Locale
from times_table_grids.worksheets import (
    GRID_SIZE,
    MARGIN,
    Exercise,
    LineStyle,
    build,
    exercise_slots,
    exercises_for,
    grid_line_styles,
    main,
)

PAGE_OBJECT = re.compile(rb"/Type /Page\b(?!s)")
A4_WIDTH = 595.2755905511812


def page_count(pdf: Path) -> int:
    return len(PAGE_OBJECT.findall(pdf.read_bytes()))


@pytest.mark.parametrize("table", range(1, 11))
def test_exercises_for_lists_the_table_times_one_to_ten_in_order(table: int) -> None:
    # Arrange
    expected = [Exercise(table, factor) for factor in range(1, 11)]

    # Act
    exercises = exercises_for(table)

    # Assert
    assert exercises == expected


def test_every_exercise_grid_fits_inside_the_page_margins() -> None:
    # Arrange
    right_limit, bottom_limit = A4_WIDTH - MARGIN, MARGIN

    # Act
    slots = exercise_slots()

    # Assert
    assert len(slots) == 10
    assert all(slot.grid_top - GRID_SIZE * slot.cell >= bottom_limit for slot in slots)
    assert all(slot.grid_left + GRID_SIZE * slot.cell <= right_limit for slot in slots)


def test_grid_uses_light_gray_lines_and_darker_lines_every_five_cells() -> None:
    # Arrange
    thin = LineStyle(width=0.5, gray=0.6)
    group = LineStyle(width=1.2, gray=0.25)

    # Act
    styles = grid_line_styles(10)

    # Assert
    assert styles == (
        group,
        thin,
        thin,
        thin,
        thin,
        group,
        thin,
        thin,
        thin,
        thin,
        group,
    )


@pytest.mark.parametrize("locale", [PT_BR, EN])
def test_build_writes_one_page_per_table(tmp_path: Path, locale: Locale) -> None:
    # Arrange
    output = tmp_path / f"{locale.file_stem}.pdf"

    # Act
    build(output, locale)

    # Assert
    assert output.read_bytes().startswith(b"%PDF")
    assert page_count(output) == 10


def test_main_writes_one_pdf_per_locale_into_the_given_directory(
    tmp_path: Path,
) -> None:
    # Arrange
    expected = sorted(f"{locale.file_stem}.pdf" for locale in LOCALES)

    # Act
    exit_code = main([str(tmp_path)])

    # Assert
    assert exit_code == 0
    assert sorted(path.name for path in tmp_path.iterdir()) == expected
