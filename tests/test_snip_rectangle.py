from pytest import fixture
from app.snip_tools import SnipRectangle


def test_SnipRectangle(rectangle: SnipRectangle) -> None:
    rect = rectangle()
    expected_init_points = {"x1": 0, "y1": 0, "x2": 0, "y2": 0}
    assert rect.__dict__ == expected_init_points

    rect = rectangle(-1, -2, -3, -4)
    expected_init_points = {"x1": -1, "y1": -2, "x2": -3, "y2": -4}
    assert rect.__dict__ == expected_init_points

    rect = rectangle(1, 2, 3, 4)
    expected_init_points = {"x1": 1, "y1": 2, "x2": 3, "y2": 4}
    assert rect.__dict__ == expected_init_points


def test_SnipRectangle_bounds(rectangle: SnipRectangle) -> None:
    rect1 = rectangle()
    expected_init_bounds = (0, 0, 0, 0)
    assert rect1.bounds == expected_init_bounds

    rect2 = rectangle(1, 2, 3, 4)
    expected_bounds = (1, 2, 2, 2)
    assert rect2.bounds == expected_bounds

    rect3 = rectangle(-100, -2, -30, -10)
    expected_bounds = (-100, -10, 70, 8)
    assert rect3.bounds == expected_bounds

    rect4 = rectangle(50, 32, -123, -10)
    expected_bounds = (-123, -10, 173, 42)
    assert rect4.bounds == expected_bounds
