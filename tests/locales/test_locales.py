import pytest

from times_table_grids.locales import EN, LOCALES, PT_BR, Locale


@pytest.mark.parametrize(
    ("locale", "count", "expected"),
    [
        (PT_BR, 1, "1 linha"),
        (PT_BR, 7, "7 linhas"),
        (EN, 1, "1 row"),
        (EN, 10, "10 rows"),
    ],
)
def test_rows_label_picks_singular_or_plural(
    locale: Locale, count: int, expected: str
) -> None:
    # Arrange
    rows = count

    # Act
    label = locale.rows_label(rows)

    # Assert
    assert label == expected


@pytest.mark.parametrize(
    ("locale", "count", "expected"),
    [
        (PT_BR, 1, "1 coluna"),
        (PT_BR, 4, "4 colunas"),
        (EN, 1, "1 column"),
        (EN, 4, "4 columns"),
    ],
)
def test_columns_label_picks_singular_or_plural(
    locale: Locale, count: int, expected: str
) -> None:
    # Arrange
    columns = count

    # Act
    label = locale.columns_label(columns)

    # Assert
    assert label == expected


@pytest.mark.parametrize(
    ("locale", "expected"), [(PT_BR, "Tabuada do 7"), (EN, "7 Times Table")]
)
def test_title_for_names_the_table_in_each_language(
    locale: Locale, expected: str
) -> None:
    # Arrange
    table = 7

    # Act
    title = locale.title_for(table)

    # Assert
    assert title == expected


def test_every_locale_writes_to_its_own_file() -> None:
    # Arrange
    expected = ["tabuada", "times-table"]

    # Act
    stems = [locale.file_stem for locale in LOCALES]

    # Assert
    assert stems == expected
