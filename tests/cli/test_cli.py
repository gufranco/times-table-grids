from pathlib import Path

from times_table_grids.cli import main


def test_main_writes_every_worksheet_into_the_given_directory(tmp_path: Path) -> None:
    # Arrange
    expected = [
        "divisao.pdf",
        "division.pdf",
        "solidos.pdf",
        "solids.pdf",
        "tabuada.pdf",
        "times-table.pdf",
    ]

    # Act
    exit_code = main([str(tmp_path)])

    # Assert
    assert exit_code == 0
    assert sorted(path.name for path in tmp_path.iterdir()) == expected
