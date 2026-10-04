"""Create a shareable archive with a placeholder key, using an explicit file list."""

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = [
    "app.py",
    "index.html",
    "settings.json",
    "exercise.json",
    "README.md",
    "START_HERE.md",
    "CODEX_LAUNCH.md",
    "AGENTS.md",
    "skills/tutor.md",
    "skills/hint.md",
    ".gitignore",
    "Start Demo.cmd",
    "Start Demo.command",
    "start-demo.sh",
    "test_app.py",
    "package_demo.py",
]
PLACEHOLDER = "PASTE_YOUR_API_KEY_HERE\n"


def package(destination=None):
    output = (
        Path(destination)
        if destination
        else ROOT.parent / "deliverables" / "demo-tutor.zip"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in FILES:
            archive.write(ROOT / name, "demo-tutor/" + name)
        archive.writestr("demo-tutor/api-key.txt", PLACEHOLDER)
    print(str(output))
    return output


if __name__ == "__main__":
    package()
