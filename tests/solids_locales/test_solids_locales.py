import pytest

from times_table_grids.geometry import SOLIDS
from times_table_grids.solids_locales import SOLIDS_LOCALES, SolidsLocale


def test_every_solids_locale_writes_to_its_own_file() -> None:
    # Arrange
    expected = ["solidos", "solids"]

    # Act
    stems = [locale.file_stem for locale in SOLIDS_LOCALES]

    # Assert
    assert stems == expected


@pytest.mark.parametrize("locale", SOLIDS_LOCALES, ids=lambda locale: locale.file_stem)
def test_every_solid_has_a_name_in_each_language(locale: SolidsLocale) -> None:
    # Arrange
    keys = {solid.key for solid in SOLIDS}

    # Act
    named = set(locale.solid_names)

    # Assert
    assert named == keys
