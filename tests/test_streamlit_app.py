import json
import re
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "streamlit_app.py")


def run_app():
    at = AppTest.from_file(APP, default_timeout=60)
    return at.run()


def chart_spec(at):
    for name in ("arrow_vega_lite_chart", "vega_lite_chart"):
        els = at.get(name)
        if els:
            return json.loads(els[0].proto.spec)
    raise AssertionError("no vega-lite chart rendered")


def test_color_picker_default_in_sidebar():
    at = run_app()

    assert at.exception == []
    assert len(at.color_picker) == 1
    assert len(at.sidebar.color_picker) == 1
    assert at.sidebar.color_picker[0].value == "#0068c9"


def test_chart_uses_default_color():
    at = run_app()

    assert chart_spec(at)["mark"]["color"] == "#0068c9"


def test_chart_uses_selected_color():
    at = run_app()
    at = at.sidebar.color_picker[0].set_value("#ff0000").run()

    assert at.exception == []
    assert chart_spec(at)["mark"]["color"] == "#ff0000"


def test_sliders_unchanged():
    at = run_app()

    assert len(at.slider) == 2
    assert at.sidebar.slider == []

    points, turns = at.slider[0], at.slider[1]

    assert points.label == "Number of points in spiral"
    assert points.min == 1
    assert points.max == 5000
    assert points.value == 2000

    assert turns.label == "Number of turns in spiral"
    assert turns.min == 1
    assert turns.max == 100
    assert turns.value == 9


def test_chart_data_rows():
    at = run_app()

    assert at.exception == []

    for name in ("arrow_vega_lite_chart", "vega_lite_chart"):
        els = at.get(name)
        if els:
            element = els[0]
            break
    else:  # pragma: no cover - no chart element at all
        raise AssertionError("no vega-lite chart rendered")

    data = getattr(element, "value", None)
    if data is not None and hasattr(data, "__len__"):
        assert len(data) == at.slider[0].value


def test_no_hardcoded_mark_color():
    source = Path(APP).read_text()

    assert re.search(r"mark_circle\([^)]*#0068c9", source) is None
    assert re.search(r"color_picker\([^)]*#0068c9", source) is not None
