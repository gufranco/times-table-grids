import math
from dataclasses import dataclass

type Point3 = tuple[float, float, float]
type Point2 = tuple[float, float]
type Edge = tuple[int, int]

DEPTH_X = 0.5 * math.cos(math.radians(40))
DEPTH_Y = 0.5 * math.sin(math.radians(40))
VIEW = (DEPTH_X, DEPTH_Y, -1.0)


@dataclass(frozen=True, slots=True)
class Solid:
    key: str
    vertices: tuple[Point3, ...]
    faces: tuple[tuple[int, ...], ...]

    @property
    def edges(self) -> tuple[Edge, ...]:
        pairs = {
            ordered(face[index], face[(index + 1) % len(face)])
            for face in self.faces
            for index in range(len(face))
        }
        return tuple(sorted(pairs))


def ordered(first: int, second: int) -> Edge:
    return (first, second) if first < second else (second, first)


def project(point: Point3) -> Point2:
    x, y, z = point
    return (x + z * DEPTH_X, y + z * DEPTH_Y)


def mean(points: list[Point3]) -> Point3:
    count = len(points)
    return (
        sum(p[0] for p in points) / count,
        sum(p[1] for p in points) / count,
        sum(p[2] for p in points) / count,
    )


def newell_normal(points: list[Point3]) -> Point3:
    pairs = list(zip(points, points[1:] + points[:1], strict=True))
    return (
        sum((a[1] - b[1]) * (a[2] + b[2]) for a, b in pairs),
        sum((a[2] - b[2]) * (a[0] + b[0]) for a, b in pairs),
        sum((a[0] - b[0]) * (a[1] + b[1]) for a, b in pairs),
    )


def dot(first: Point3, second: Point3) -> float:
    return sum(a * b for a, b in zip(first, second, strict=True))


def outward_normal(solid: Solid, face: tuple[int, ...]) -> Point3:
    points = [solid.vertices[index] for index in face]
    normal = newell_normal(points)
    center, face_center = mean(list(solid.vertices)), mean(points)
    outward = tuple(f - c for f, c in zip(face_center, center, strict=True))
    sign = 1.0 if dot(normal, outward) >= 0 else -1.0
    return (normal[0] * sign, normal[1] * sign, normal[2] * sign)


def visible_faces(solid: Solid) -> tuple[int, ...]:
    return tuple(
        index
        for index, face in enumerate(solid.faces)
        if dot(outward_normal(solid, face), VIEW) > 1e-9
    )


def hidden_edges(solid: Solid) -> tuple[Edge, ...]:
    shown = visible_faces(solid)
    visible = {
        ordered(solid.faces[i][k], solid.faces[i][(k + 1) % len(solid.faces[i])])
        for i in shown
        for k in range(len(solid.faces[i]))
    }
    return tuple(edge for edge in solid.edges if edge not in visible)


def prism(key: str, outline: tuple[Point2, ...], depth: float) -> Solid:
    count = len(outline)
    front = tuple((x, y, 0.0) for x, y in outline)
    back = tuple((x, y, depth) for x, y in outline)
    sides = tuple(
        (index, (index + 1) % count, count + (index + 1) % count, count + index)
        for index in range(count)
    )
    caps = (tuple(range(count)), tuple(range(count, 2 * count)))
    return Solid(key=key, vertices=front + back, faces=caps + sides)


def pyramid(key: str, base: tuple[Point3, ...], apex: Point3) -> Solid:
    count = len(base)
    sides = tuple((index, (index + 1) % count, count) for index in range(count))
    return Solid(key=key, vertices=(*base, apex), faces=(tuple(range(count)), *sides))


def hexagon(radius: float) -> tuple[Point2, ...]:
    return tuple(
        (
            radius * math.cos(math.radians(60 * k)),
            radius * math.sin(math.radians(60 * k)),
        )
        for k in range(6)
    )


SOLIDS = (
    prism("cube", ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)), 1.0),
    prism("box", ((0.0, 0.0), (1.7, 0.0), (1.7, 0.8), (0.0, 0.8)), 0.9),
    prism("triangular_prism", ((0.0, 0.0), (1.0, 0.0), (0.5, 0.85)), 1.4),
    pyramid(
        "square_pyramid",
        ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 0.0, 1.0), (0.0, 0.0, 1.0)),
        (0.5, 1.2, 0.5),
    ),
    pyramid(
        "triangular_pyramid",
        ((0.0, 0.0, 0.0), (1.2, 0.0, 0.0), (0.6, 0.0, 1.0)),
        (0.55, 1.1, 0.35),
    ),
    prism("hexagonal_prism", hexagon(0.6), 1.2),
)


def solid_named(key: str) -> Solid:
    matches = [solid for solid in SOLIDS if solid.key == key]
    if not matches:
        raise KeyError(f"no solid named {key!r}")
    return matches[0]
