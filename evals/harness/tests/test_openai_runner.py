from pathlib import Path
from evals.harness.runners.openai_runner import (
    extract_code_blocks_to_workdir, build_system_prompt,
)


def test_extract_kotlin_block_writes_file(tmp_path):
    body = """Sure, here you go:

```kotlin AuthScreen.kt
package x
fun screen() {}
```

Done."""
    written = extract_code_blocks_to_workdir(body, tmp_path)
    assert written == [tmp_path / "AuthScreen.kt"]
    assert (tmp_path / "AuthScreen.kt").read_text().startswith("package x")


def test_extract_multiple_blocks_with_path_hints(tmp_path):
    body = """First file:

```kotlin file=app/AuthScreen.kt
content one
```

Second:

```kotlin app/Vm.kt
content two
```
"""
    written = extract_code_blocks_to_workdir(body, tmp_path)
    assert (tmp_path / "app" / "AuthScreen.kt").read_text() == "content one\n"
    assert (tmp_path / "app" / "Vm.kt").read_text() == "content two\n"


def test_extract_block_without_filename_falls_back_to_indexed(tmp_path):
    body = """```kotlin
no filename here
```"""
    written = extract_code_blocks_to_workdir(body, tmp_path)
    assert len(written) == 1
    assert written[0].suffix == ".kt"
    assert "no filename here" in written[0].read_text()


def test_build_system_prompt_with_skill(tmp_path, monkeypatch):
    fake_skill = tmp_path / "ping-app-integration"
    fake_skill.mkdir()
    (fake_skill / "SKILL.md").write_text("---\nname: ping-app-integration\n---\nbody body body")
    prompt = build_system_prompt("with_skill", "ping-app-integration", skills_root=tmp_path)
    assert "body body body" in prompt


def test_build_system_prompt_without_skill_is_empty(tmp_path):
    prompt = build_system_prompt("without_skill", "ping-app-integration", skills_root=tmp_path)
    assert prompt == ""
