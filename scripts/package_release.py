"""Create user-facing template ZIPs from tracked project files."""

import argparse
from pathlib import Path
import re
import subprocess
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
PROJECT = "SWUFE-Thesis"
ROOT_FILES = {
    ".gitignore", ".latexmkrc", "Compile.bat", "LICENSE", "Makefile", "README.md",
    "config.json", "main.tex", "refs.bib", "setup.tex", "swufe-layout.tex",
}
FONT_FILES = {
    "STZHONGS.TTF", "FZXiaoBiaoSong.ttf", "Times New Roman.ttf",
    "Times New Roman Bold.ttf", "Times New Roman Italic.ttf",
    "Times New Roman Bold Italic.ttf",
}
DIRECTORIES = {"contents", "figures", "font", "img", "docs"}


def package_release(root, version, output_dir):
    tracked = subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=root
    ).decode("utf-8").split("\0")
    names = sorted(name for name in tracked if name and (
        name in ROOT_FILES or Path(name).parts[0] in DIRECTORIES
    ))
    required = ROOT_FILES | {f"font/{name}" for name in FONT_FILES}
    missing = required - set(names)
    missing.update(name for name in names if not (root / name).is_file())
    if missing:
        raise ValueError("Missing release inputs: " + ", ".join(sorted(missing)))
    for directory in ("contents", "figures", "img", "docs"):
        if not any(name.startswith(directory + "/") for name in names):
            raise ValueError(f"Missing release directory: {directory}")

    # Tags may contain slashes or characters unsuitable for Windows filenames.
    version = re.sub(r"[^\w.-]+", "-", version).strip(".-")
    if not version:
        raise ValueError("Tag must contain a letter, digit or underscore")
    output_dir.mkdir(parents=True, exist_ok=True)
    archives = []
    for variant in ("with-font", "without-font"):
        archive = output_dir / f"{PROJECT}-{version}-{variant}.zip"
        with ZipFile(archive, "w", compression=ZIP_DEFLATED) as package:
            for name in names:
                if variant == "without-font" and name.startswith("font/"):
                    continue
                # Keep main.tex at the ZIP root for direct Overleaf uploads.
                package.write(root / name, arcname=name)
        archives.append(archive)
    return archives


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="Release tag, e.g. v1.0.0")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "build" / "release")
    args = parser.parse_args()
    for archive in package_release(ROOT, args.version, args.output_dir):
        print(archive)


if __name__ == "__main__":
    main()
