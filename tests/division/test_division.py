import re
from pathlib import Path

import pytest

from times_table_grids.division import (
    Division,
    build_division,
    divisions_for,
)
from times_table_grids.division_locales import (
    DIVISION_EN,
    DIVISION_LOCALES,
    DIVISION_PT_BR,
    DivisionLocale,
)

PAGE_OBJECT = re.compile(rb"/Type /Page\b(?!s)")


@pytest.mark.parametrize("divisor", range(1, 11))
def test_divisions_for_covers_every_quotient_from_one_to_ten(divisor: int) -> None:
    # Arrange
    expected = list(range(1, 11))

    # Act
    divisions = divisions_for(divisor)

    # Assert
    assert sorted(division.quotient for division in divisions) == expected
    assert all(division.divisor == divisor for division in divisions)
    assert all(
        division.dividend == division.divisor * division.quotient
        for division in divisions
    )


@pytest.mark.parametrize("divisor", range(2, 11))
def test_divisions_for_does_not_list_answers_in_counting_order(divisor: int) -> None:
    # Arrange
    counting_order = list(range(1, 11))

    # Act
    divisions = divisions_for(divisor)

    # Assert
    assert [division.quotient for division in divisions] != counting_order


def test_divisions_for_returns_the_same_order_every_time() -> None:
    # Arrange
    first = divisions_for(7)

    # Act
    second = divisions_for(7)

    # Assert
    assert first == second


def test_division_exercise_reads_dividend_then_divisor() -> None:
    # Arrange
    division = Division(divisor=3, quotient=4)

    # Act
    equation = division.equation

    # Assert
    assert equation == "12 ÷ 3 ="


@pytest.mark.parametrize(
    ("locale", "expected"),
    [
        (DIVISION_PT_BR, ("12 X no total", "3 em cada linha")),
        (DIVISION_EN, ("12 marks in all", "3 in each row")),
    ],
)
def test_hint_names_the_total_and_the_row_size(
    locale: DivisionLocale, expected: tuple[str, str]
) -> None:
    # Arrange
    division = Division(divisor=3, quotient=4)

    # Act
    hint = (
        locale.total_label(division.dividend),
        locale.per_row_label(division.divisor),
    )

    # Assert
    assert hint == expected


@pytest.mark.parametrize(
    ("locale", "expected"),
    [(DIVISION_PT_BR, "Divisão por 7"), (DIVISION_EN, "Dividing by 7")],
)
def test_division_title_names_the_divisor(
    locale: DivisionLocale, expected: str
) -> None:
    # Arrange
    divisor = 7

    # Act
    title = locale.title_for(divisor)

    # Assert
    assert title == expected


@pytest.mark.parametrize("locale", DIVISION_LOCALES)
def test_build_division_writes_one_page_per_divisor(
    tmp_path: Path, locale: DivisionLocale
) -> None:
    # Arrange
    output = tmp_path / f"{locale.file_stem}.pdf"

    # Act
    build_division(output, locale)

    # Assert
    assert output.read_bytes().startswith(b"%PDF")
    assert len(PAGE_OBJECT.findall(output.read_bytes())) == 10
