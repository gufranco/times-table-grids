import pytest

from times_table_grids.geometry import (
    SOLIDS,
    Solid,
    hidden_edges,
    solid_named,
    visible_faces,
)

KNOWN_COUNTS = {
    "cube": (6, 12, 8),
    "box": (6, 12, 8),
    "triangular_prism": (5, 9, 6),
    "square_pyramid": (5, 8, 5),
    "triangular_pyramid": (4, 6, 4),
    "hexagonal_prism": (8, 18, 12),
}


@pytest.mark.parametrize("solid", SOLIDS, ids=lambda solid: solid.key)
def test_solid_has_the_textbook_face_edge_and_vertex_counts(solid: Solid) -> None:
    # Arrange
    expected = KNOWN_COUNTS[solid.key]

    # Act
    counts = (len(solid.faces), len(solid.edges), len(solid.vertices))

    # Assert
    assert counts == expected


def test_cube_shows_its_front_top_and_right_faces() -> None:
    # Arrange
    cube = solid_named("cube")

    # Act
    faces = visible_faces(cube)

    # Assert
    assert len(faces) == 3


def test_cube_hides_the_three_edges_meeting_at_the_back_bottom_left_corner() -> None:
    # Arrange
    cube = solid_named("cube")
    corner = cube.vertices.index((0.0, 0.0, 1.0))

    # Act
    hidden = hidden_edges(cube)

    # Assert
    assert len(hidden) == 3
    assert all(corner in edge for edge in hidden)


@pytest.mark.parametrize("solid", SOLIDS, ids=lambda solid: solid.key)
def test_every_solid_shows_at_least_one_face_and_hides_at_least_one_edge(
    solid: Solid,
) -> None:
    # Arrange
    edge_count = len(solid.edges)

    # Act
    hidden = hidden_edges(solid)

    # Assert
    assert visible_faces(solid)
    assert 0 < len(hidden) < edge_count


def test_solid_named_rejects_an_unknown_key() -> None:
    # Arrange
    key = "sphere"

    # Act
    act = lambda: solid_named(key)

    # Assert
    with pytest.raises(KeyError, match="sphere"):
        act()
