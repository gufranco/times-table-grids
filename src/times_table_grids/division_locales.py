from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DivisionLocale:
    file_stem: str
    document_title: str
    page_title: str
    name_label: str
    guide_title: str
    guide_steps: tuple[str, str, str, str]
    guide_tip: str
    example_label: str
    total_hint: str
    per_row_hint: str

    def title_for(self, divisor: int) -> str:
        return self.page_title.format(divisor=divisor)

    def total_label(self, dividend: int) -> str:
        return self.total_hint.format(count=dividend)

    def per_row_label(self, divisor: int) -> str:
        return self.per_row_hint.format(count=divisor)


DIVISION_PT_BR = DivisionLocale(
    file_stem="divisao",
    document_title="Divisão por 1 até 10",
    page_title="Divisão por {divisor}",
    name_label="Nome:",
    guide_title="Como fazer",
    guide_steps=(
        "1. 1º número: quantos X marcar no total",
        "2. 2º número: quantos X em cada linha",
        "3. Preencha linha por linha até o total",
        "4. Conte as LINHAS: esse é o resultado",
    ),
    guide_tip="Dica: o resultado é quantas linhas você usou.",
    example_label="Exemplo",
    total_hint="{count} X no total",
    per_row_hint="{count} em cada linha",
)

DIVISION_EN = DivisionLocale(
    file_stem="division",
    document_title="Dividing by 1 to 10",
    page_title="Dividing by {divisor}",
    name_label="Name:",
    guide_title="How to do it",
    guide_steps=(
        "1. 1st number: how many X marks in all",
        "2. 2nd number: how many X in each row",
        "3. Fill row by row until you reach it",
        "4. Count the ROWS: that is the answer",
    ),
    guide_tip="Tip: the answer is how many rows you used.",
    example_label="Example",
    total_hint="{count} marks in all",
    per_row_hint="{count} in each row",
)

DIVISION_LOCALES = (DIVISION_PT_BR, DIVISION_EN)
