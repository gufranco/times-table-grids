from dataclasses import dataclass

type Definition = tuple[str, str, str]


@dataclass(frozen=True, slots=True)
class SolidsLocale:
    file_stem: str
    document_title: str
    name_label: str
    lesson_title: str
    face: Definition
    edge: Definition
    vertex: Definition
    try_title: str
    try_steps: tuple[str, str, str]
    tips: tuple[str, str, str]
    count_title: str
    count_instruction: str
    count_labels: tuple[str, str, str]
    solid_names: dict[str, str]


SOLIDS_PT_BR = SolidsLocale(
    file_stem="solidos",
    document_title="Face, aresta e vértice",
    name_label="Nome:",
    lesson_title="Face, aresta e vértice",
    face=("Face", "É cada lado plano do sólido.", "Um dado tem 6 faces."),
    edge=(
        "Aresta",
        "É a linha onde duas faces se encontram.",
        "Passe o dedo: é a dobra.",
    ),
    vertex=(
        "Vértice",
        "É a ponta onde as arestas se encontram.",
        "Toque nele: é o cantinho.",
    ),
    try_title="Experimente no cubo",
    try_steps=(
        "1. Pinte de leve UMA face.",
        "2. Passe o lápis por cima de UMA aresta.",
        "3. Faça uma bolinha em UM vértice.",
    ),
    tips=(
        "As linhas tracejadas ficam escondidas atrás. Conte elas também!",
        "Marque cada vértice com um ponto enquanto conta, para não repetir.",
        "Pegue um dado ou uma caixa de leite e conte com as mãos.",
    ),
    count_title="Conte as faces, arestas e vértices",
    count_instruction="Escreva quantos cada sólido tem. Não esqueça das linhas tracejadas.",
    count_labels=("Faces", "Arestas", "Vértices"),
    solid_names={
        "cube": "Cubo",
        "box": "Bloco retangular",
        "triangular_prism": "Prisma triangular",
        "square_pyramid": "Pirâmide de base quadrada",
        "triangular_pyramid": "Pirâmide de base triangular",
        "hexagonal_prism": "Prisma hexagonal",
    },
)

SOLIDS_EN = SolidsLocale(
    file_stem="solids",
    document_title="Faces, edges and vertices",
    name_label="Name:",
    lesson_title="Faces, edges and vertices",
    face=("Face", "Each flat side of the solid.", "A die has 6 faces."),
    edge=("Edge", "The line where two faces meet.", "Run your finger along the fold."),
    vertex=("Vertex", "The point where edges meet.", "Touch it: it is the corner."),
    try_title="Try it on the cube",
    try_steps=(
        "1. Lightly shade ONE face.",
        "2. Trace over ONE edge with your pencil.",
        "3. Draw a circle on ONE vertex.",
    ),
    tips=(
        "Dashed lines are hidden at the back. Count them too!",
        "Put a dot on each vertex as you count, so you never count one twice.",
        "Grab a die or a milk carton and count with your hands.",
    ),
    count_title="Count the faces, edges and vertices",
    count_instruction="Write how many each solid has. Remember the dashed lines.",
    count_labels=("Faces", "Edges", "Vertices"),
    solid_names={
        "cube": "Cube",
        "box": "Rectangular prism",
        "triangular_prism": "Triangular prism",
        "square_pyramid": "Square pyramid",
        "triangular_pyramid": "Triangular pyramid",
        "hexagonal_prism": "Hexagonal prism",
    },
)

SOLIDS_LOCALES = (SOLIDS_PT_BR, SOLIDS_EN)
