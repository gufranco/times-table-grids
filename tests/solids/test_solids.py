import re
from pathlib import Path

import pytest

from times_table_grids.solids import build_solids, fit_box
from times_table_grids.solids_locales import SOLIDS_LOCALES, SolidsLocale

PAGE_OBJECT = re.compile(rb"/Type /Page\b(?!s)")


@pytest.mark.parametrize("locale", SOLIDS_LOCALES, ids=lambda locale: locale.file_stem)
def test_build_solids_writes_a_lesson_page_and_a_counting_page(
    tmp_path: Path, locale: SolidsLocale
) -> None:
    # Arrange
    output = tmp_path / f"{locale.file_stem}.pdf"

    # Act
    build_solids(output, locale)

    # Assert
    assert output.read_bytes().startswith(b"%PDF")
    assert len(PAGE_OBJECT.findall(output.read_bytes())) == 2


def test_fit_box_scales_a_drawing_into_the_box_and_keeps_its_shape() -> None:
    # Arrange
    points = [(0.0, 0.0), (2.0, 1.0)]

    # Act
    placed = fit_box(points, left=10.0, bottom=20.0, width=100.0, height=100.0)

    # Assert
    assert placed == [(10.0, 45.0), (110.0, 95.0)]
