from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import update_readme_eval_table as u


def test_render_layer3_table_has_all_skills_and_models():
    summary = {
        "by_skill_model_config": {
            "ping-app-integration": {
                "claude-sonnet-4-6": {
                    "with_skill":    {"pass_rate": 0.96, "tokens_mean": 22000, "duration_mean_s": 180},
                    "without_skill": {"pass_rate": 0.72, "tokens_mean": 31000, "duration_mean_s": 210},
                    "delta":         {"pass_rate": "+0.24", "tokens": "-9000", "duration_s": "-30.0"},
                }
            }
        },
        "aggregate_by_model": {"claude-sonnet-4-6": {"with_skill_pass": 0.93, "without_skill_pass": 0.69}},
    }
    out = u.render_layer3_section(summary, models=["claude-sonnet-4-6"])
    assert "ping-app-integration" in out
    assert "+0.24" in out
    assert "-9000" in out


def test_replace_between_markers(tmp_path):
    f = tmp_path / "README.md"
    f.write_text("Hello\n<!-- BEGIN: layer3-eval-table -->\nold\n<!-- END: layer3-eval-table -->\nBye\n")
    u.replace_between_markers(f, begin="<!-- BEGIN: layer3-eval-table -->",
                              end="<!-- END: layer3-eval-table -->", new_content="### Layer 3\nNEW BODY\n")
    text = f.read_text()
    assert "### Layer 3" in text
    assert "NEW BODY" in text
    assert "old" not in text


def test_replace_raises_when_markers_missing(tmp_path):
    f = tmp_path / "README.md"
    f.write_text("no markers here")
    try:
        u.replace_between_markers(f, begin="A", end="B", new_content="x")
    except ValueError:
        return
    raise AssertionError("expected ValueError")
