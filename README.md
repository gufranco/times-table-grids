# times-table-grids

Printable worksheets for an 8-year-old: the 1 to 10 times tables, division by 1 to 10, and faces, edges and vertices of solids. Each times table and each divisor gets one A4 page. Every exercise comes with an empty 10x10 grid. To solve `3 × 4`, the child marks an X in 3 rows of 4 squares, counts the marks, and writes the answer.

Every grid is the same size on purpose. A grid sized to the answer would give the answer away; a fixed 10x10 grid makes the child find the rectangle.

Two languages ship from the same layout:

| File | Topic | Language |
|---|---|---|
| `tabuada.pdf` | Times tables | Brazilian Portuguese |
| `times-table.pdf` | Times tables | English |
| `divisao.pdf` | Division | Brazilian Portuguese |
| `division.pdf` | Division | English |
| `solidos.pdf` | Faces, edges and vertices | Brazilian Portuguese |
| `solids.pdf` | Faces, edges and vertices | English |

## What is on a page

- A "How to do it" box with four steps and a worked `2 × 3 = 6` example.
- Ten exercises, `N × 1` through `N × 10`, each with an answer box and a small hint naming the rows and columns.
- Row and column numbers from 1 to 10 along each grid, and a darker line every 5 squares for counting in fives.

## Division

Division runs the grid backwards. To solve `12 ÷ 3`, the child marks 3 X in each row, row by row, until 12 X are marked, then counts the rows. The exercises on each page come in a fixed shuffled order, so the answers never read 1, 2, 3 down the page.

## Faces, edges and vertices

Two pages. The first names a face, an edge and a vertex on a labelled cube, then asks the child to shade, trace and circle each one on a blank cube. The second shows six solids, from a cube to a hexagonal prism, with boxes to write how many faces, edges and vertices each has. Hidden edges are dashed and are worked out from each solid's 3D shape.

## Download

Get every PDF from the latest release: <https://github.com/gufranco/times-table-grids/releases/latest>.

## Printing

Print at 100% scale, "Actual size" in most print dialogs. "Fit to page" shrinks the 4.8 mm squares. The pages are made for black and white: lines are thin and gray and nothing is filled, so a page uses little toner.

## Building locally

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv run times-table-grids          # writes every PDF into dist/
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

Releases are automatic. After CI passes on `main`, semantic-release reads the conventional commit messages, bumps the version, tags it, publishes a GitHub release, and the workflow attaches every PDF to it. A `feat:` commit makes a minor release and a `fix:` commit a patch release.

## License

[MIT](LICENSE).
