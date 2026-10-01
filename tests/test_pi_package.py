"""Keep the documented Pi Git install loading exactly the LintLang skill.

Pi discovers a manifest-less Git package through its conventional resource
directories; a root package.json would also make the install run npm.
"""

from pathlib import Path

from lintlang import __version__

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/lintlang/SKILL.md"


def test_pi_package_exposes_only_the_lintlang_skill():
    assert not (ROOT / "package.json").exists()
    for resource_dir in ("extensions", "prompts", "themes"):
        assert not (ROOT / resource_dir).exists()
    assert sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "skills").rglob("SKILL.md")) == [
        "skills/lintlang/SKILL.md"
    ]
    frontmatter = SKILL.read_text(encoding="utf-8").split("---", 2)[1]
    assert "\nname: lintlang\n" in frontmatter
    assert "\ndescription: " in frontmatter


def test_pi_install_docs_track_the_release():
    guide = (ROOT / "docs/integrations.md").read_text(encoding="utf-8")
    assert f"pi install git:github.com/hermes-labs-ai/lintlang@v{__version__}" in guide
    assert f"uvx --from lintlang=={__version__}" in guide
    assert f"uvx --from lintlang=={__version__}" in SKILL.read_text(encoding="utf-8")
