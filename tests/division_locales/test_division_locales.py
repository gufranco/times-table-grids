from times_table_grids.division_locales import DIVISION_LOCALES


def test_every_division_locale_writes_to_its_own_file() -> None:
    # Arrange
    expected = ["divisao", "division"]

    # Act
    stems = [locale.file_stem for locale in DIVISION_LOCALES]

    # Assert
    assert stems == expected
