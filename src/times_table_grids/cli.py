import sys
from collections.abc import Sequence
from pathlib import Path

from times_table_grids.division import build_division
from times_table_grids.division_locales import DIVISION_LOCALES
from times_table_grids.locales import LOCALES
from times_table_grids.solids import build_solids
from times_table_grids.solids_locales import SOLIDS_LOCALES
from times_table_grids.worksheets import build

DEFAULT_OUTPUT_DIR = Path("dist")


def write_all(output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    times = [(output_dir / f"{locale.file_stem}.pdf", locale) for locale in LOCALES]
    divisions = [
        (output_dir / f"{locale.file_stem}.pdf", locale) for locale in DIVISION_LOCALES
    ]
    for path, locale in times:
        build(path, locale)
    for path, division_locale in divisions:
        build_division(path, division_locale)
    solids = [
        (output_dir / f"{locale.file_stem}.pdf", locale) for locale in SOLIDS_LOCALES
    ]
    for path, solids_locale in solids:
        build_solids(path, solids_locale)
    return (
        [path for path, _ in times]
        + [path for path, _ in divisions]
        + [path for path, _ in solids]
    )


def main(argv: Sequence[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    output_dir = Path(args[0]) if args else DEFAULT_OUTPUT_DIR
    for path in write_all(output_dir):
        sys.stdout.write(f"{path.resolve()}\n")
    return 0
