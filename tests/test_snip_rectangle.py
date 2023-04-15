from hypothesis import given, strategies as st
from app.snip_tools import SnipRectangle


@given(
    x1=st.integers(min_value=-100, max_value=100),
    y1=st.integers(min_value=-100, max_value=100),
    x2=st.integers(min_value=-100, max_value=100),
    y2=st.integers(min_value=-100, max_value=100),
)
def test_SnipRectangle_init_and_bounds(x1, y1, x2, y2) -> None:
    rect = SnipRectangle(x1, y1, x2, y2)
    expected_init_points = {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
    assert rect.__dict__ == expected_init_points

    sorted_x1, sorted_x2 = sorted([x1, x2])
    sorted_y1, sorted_y2 = sorted([y1, y2])
    expected_bounds = (
        sorted_x1,
        sorted_y1,
        sorted_x2 - sorted_x1,
        sorted_y2 - sorted_y1,
    )
    assert rect.bounds == expected_bounds
