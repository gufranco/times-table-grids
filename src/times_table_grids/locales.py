from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Locale:
    file_stem: str
    document_title: str
    page_title: str
    name_label: str
    guide_title: str
    guide_steps: tuple[str, str, str, str]
    guide_tip: str
    example_label: str
    row_words: tuple[str, str]
    column_words: tuple[str, str]

    def title_for(self, table: int) -> str:
        return self.page_title.format(table=table)

    def rows_label(self, count: int) -> str:
        return counted(count, self.row_words)

    def columns_label(self, count: int) -> str:
        return counted(count, self.column_words)


def counted(count: int, words: tuple[str, str]) -> str:
    singular, plural = words
    return f"{count} {singular if count == 1 else plural}"


PT_BR = Locale(
    file_stem="tabuada",
    document_title="Tabuada do 1 ao 10",
    page_title="Tabuada do {table}",
    name_label="Nome:",
    guide_title="Como fazer",
    guide_steps=(
        "1. 1º número: quantas LINHAS (para baixo)",
        "2. 2º número: quantas COLUNAS (para o lado)",
        "3. Marque um X em cada quadradinho",
        "4. Conte os X e escreva o resultado",
    ),
    guide_tip="Dica: as linhas escuras ajudam a contar de 5 em 5.",
    example_label="Exemplo",
    row_words=("linha", "linhas"),
    column_words=("coluna", "colunas"),
)

EN = Locale(
    file_stem="times-table",
    document_title="Times Tables 1 to 10",
    page_title="{table} Times Table",
    name_label="Name:",
    guide_title="How to do it",
    guide_steps=(
        "1. 1st number: how many ROWS (down)",
        "2. 2nd number: how many COLUMNS (across)",
        "3. Mark an X in each little square",
        "4. Count the X marks and write the answer",
    ),
    guide_tip="Tip: the dark lines help you count by 5s.",
    example_label="Example",
    row_words=("row", "rows"),
    column_words=("column", "columns"),
)

LOCALES = (PT_BR, EN)
