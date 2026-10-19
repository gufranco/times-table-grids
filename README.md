# times-table-grids

Printable worksheets for the 1 to 10 times tables, one A4 page per table. Every exercise comes with an empty 10x10 grid. To solve `3 × 4`, the child marks an X in 3 rows of 4 squares, counts the marks, and writes the answer.

Every grid is the same size on purpose. A grid sized to the answer would give the answer away; a fixed 10x10 grid makes the child find the rectangle.

Two languages ship from the same layout:

| File | Language |
|---|---|
| `tabuada.pdf` | Brazilian Portuguese |
| `times-table.pdf` | English |

## What is on a page

- A "How to do it" box with four steps and a worked `2 × 3 = 6` example.
- Ten exercises, `N × 1` through `N × 10`, each with an answer box and a small hint naming the rows and columns.
- Row and column numbers from 1 to 10 along each grid, and a darker line every 5 squares for counting in fives.

The pages print in black and white. Grid lines are light gray and nothing is filled, so a page uses little toner.

## Download

Get both PDFs from the latest release: <https://github.com/gufranco/times-table-grids/releases/latest>.

## Printing

Print at 100% scale, "Actual size" in most print dialogs. "Fit to page" shrinks the 4.8 mm squares.

## Building locally

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv run times-table-grids          # writes dist/tabuada.pdf and dist/times-table.pdf
uv run times-table-grids out/     # writes into out/ instead
```

## Development

```bash
uv run ruff format --check .
uv run ruff check .
uv run pytest --cov=times_table_grids --cov-branch --cov-fail-under=95
```

To add a language, add a `Locale` to `src/times_table_grids/locales.py` and append it to `LOCALES`.

## Releases

Pushing a tag that starts with `v` runs the release workflow, which runs the checks, builds both PDFs, and attaches them to a GitHub release for that tag:

```bash
git tag v1.0.0
git push origin v1.0.0
```
