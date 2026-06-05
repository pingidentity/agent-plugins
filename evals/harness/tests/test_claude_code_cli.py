import json
from evals.harness.runners.claude_code_cli import (
    parse_stream_json, RunOutcome, build_argv,
)


def test_parse_stream_json_extracts_tokens_and_text():
    """stream-json emits one JSON object per line. The runner needs to
    handle 'system' init, 'assistant' messages with usage, and 'result'."""
    lines = [
        json.dumps({"type": "system", "subtype": "init", "model": "claude-sonnet-4-6"}),
        json.dumps({
            "type": "assistant",
            "message": {
                "content": [{"type": "text", "text": "Working on it."}],
                "usage": {"input_tokens": 1000, "output_tokens": 50}
            }
        }),
        json.dumps({
            "type": "assistant",
            "message": {
                "content": [{"type": "text", "text": "Done. Final answer."}],
                "usage": {"input_tokens": 100, "output_tokens": 30}
            }
        }),
        json.dumps({
            "type": "result",
            "subtype": "success",
            "is_error": False,
            "duration_ms": 12345,
            "num_turns": 3,
            "usage": {"input_tokens": 1100, "output_tokens": 80}
        }),
    ]
    outcome = parse_stream_json(lines)
    assert outcome.tokens_input == 1100
    assert outcome.tokens_output == 80
    assert outcome.tokens_total == 1180
    assert outcome.duration_ms == 12345
    assert outcome.turn_count == 3
    assert outcome.final_message == "Done. Final answer."
    assert outcome.error is None


def test_parse_stream_json_handles_error_result():
    lines = [
        json.dumps({"type": "system", "subtype": "init"}),
        json.dumps({"type": "result", "subtype": "error_max_turns",
                    "is_error": True, "duration_ms": 9999,
                    "num_turns": 30, "usage": {"input_tokens": 5000, "output_tokens": 200}}),
    ]
    outcome = parse_stream_json(lines)
    assert outcome.error == "error_max_turns"
    assert outcome.tokens_total == 5200
    assert outcome.duration_ms == 9999


def test_parse_stream_json_tolerates_blank_and_garbage_lines():
    """Robustness: streams sometimes contain blank lines or partial chunks."""
    lines = [
        "",
        "not json at all",
        json.dumps({"type": "result", "subtype": "success",
                    "is_error": False, "duration_ms": 1, "num_turns": 1,
                    "usage": {"input_tokens": 10, "output_tokens": 5}}),
    ]
    outcome = parse_stream_json(lines)
    assert outcome.tokens_total == 15


def test_build_argv_with_skill_uses_plugin_dir(tmp_path):
    plugin = tmp_path / "plugins" / "ping-identity"
    plugin.mkdir(parents=True)
    argv = build_argv(
        prompt="hi",
        model="claude-sonnet-4-6",
        config="with_skill",
        plugin_dir=plugin,
        max_turns=30,
    )
    assert "claude" in argv[0]
    assert "-p" in argv
    assert "hi" in argv
    assert "--plugin-dir" in argv
    assert str(plugin) in argv
    assert "--bare" not in argv
    assert "--model" in argv
    assert "claude-sonnet-4-6" in argv


def test_build_argv_without_skill_uses_bare(tmp_path):
    argv = build_argv(
        prompt="hi",
        model="claude-sonnet-4-6",
        config="without_skill",
        plugin_dir=tmp_path,
        max_turns=30,
    )
    assert "--bare" in argv
    assert "--plugin-dir" not in argv
