from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


def run() -> AppTest:
    return AppTest.from_file(str(ROOT / "app.py"), default_timeout=60).run()


def test_app_renders_question_and_views() -> None:
    app = run()
    assert not app.exception
    assert any("In regions where leading closed US models are restricted" in m.value for m in app.markdown)
    keys = {getattr(node, "key", None) for node in app}
    assert {"cost_capability", "ranked_options"} <= keys


def test_controls_and_empty_state() -> None:
    app = run()
    app.selectbox(key="route").set_value("Open weights (can be self-hosted)").run()
    app.checkbox(key="weight_method_opt1").check().run()
    app.selectbox(key="match_rule").set_value("same name only (safest)").run()
    assert not app.exception
    app.multiselect(key="developers").set_value([]).run()
    assert not app.exception
    assert any("No models match the selected filters" in i.value for i in app.info)


def test_small_selections_do_not_break_the_page():
    """Few models left (slider range, empty score lists) and stale session values must not raise."""
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"), default_timeout=60)
    app.session_state["window"] = "2025 to 2026 (158 models)"  # left over from an older version
    app.run()
    assert not app.exception
    app.selectbox(key="route").set_value("Open weights (can be self-hosted)")
    app.multiselect(key="developers").set_value(["Google DeepMind"]).run()
    assert not app.exception
    app.multiselect(key="developers").set_value([]).run()
    assert not app.exception
