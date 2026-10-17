"""Exercise real font lookup with isolated Linux fontconfig directories."""

import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
TIMES_FILES = (
    "Times New Roman.ttf", "Times New Roman Bold.ttf",
    "Times New Roman Italic.ttf", "Times New Roman Bold Italic.ttf",
)


@unittest.skipUnless(
    sys.platform.startswith("linux") and shutil.which("xelatex")
    and shutil.which("fc-match"), "XeLaTeX and Linux fontconfig required",
)
class FontFallbackTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="swufe-font-test-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        for name in ("setup.tex", "swufe-layout.tex", "config.json"):
            shutil.copy2(ROOT / name, self.project / name)
        self.system_fonts = self.project / "system-fonts"
        self.system_fonts.mkdir()
        config = self.project / "fontconfig.xml"
        config.write_text(
            '<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd">'
            f'<fontconfig><dir>{self.system_fonts}</dir>'
            f'<cachedir>{self.project / "cache"}</cachedir></fontconfig>'
        )
        self.env = dict(os.environ, FONTCONFIG_FILE=str(config))
        (self.project / "main.tex").write_text(r"""
\documentclass[type=master,openany,oneside,cjk-font=fandol,baselineskip=false]{sjtuthesis}
\input{setup}
\begin{document}
\typeout{SWUFEFONT-REG=\fontname\font}
{\bfseries\typeout{SWUFEFONT-BOLD=\fontname\font}Bold}
{\itshape\typeout{SWUFEFONT-ITALIC=\fontname\font}Italic}
{\bfseries\itshape\typeout{SWUFEFONT-BI=\fontname\font}Bold Italic}
{\swufexbslatin\typeout{SWUFEFONT-XBS=\fontname\font}1}
{\swufexiaobiaosong 中文章标题}
{\zhongsong 中文内封}
\end{document}
""")

    def build(self):
        result = subprocess.run(
            ["xelatex", "-no-pdf", "-halt-on-error", "-interaction=nonstopmode",
             "-file-line-error", "main.tex"],
            cwd=self.project, env=self.env, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, timeout=90,
        )
        log = (self.project / "main.log").read_text(errors="replace")
        self.assertEqual(result.returncode, 0, result.stdout[-6000:])
        for warning in ("Missing character", "LaTeX Font Warning", "not loadable"):
            self.assertNotIn(warning, log)
        self.assertTrue((self.project / "main.xdv").is_file())
        return dict(re.findall(r"SWUFEFONT-(\w+)=(.*)", log))

    def assert_termes(self, fonts):
        for label, face in (("REG", "regular"), ("BOLD", "bold"),
                            ("ITALIC", "italic"), ("BI", "bolditalic")):
            self.assertIn(f"texgyretermes-{face}.otf", fonts[label])

    def test_distribution_fonts_without_project_or_system_fonts(self):
        fonts = self.build()
        self.assert_termes(fonts)
        self.assertIn("FandolSong-Regular.otf", fonts["XBS"])

    def test_each_missing_times_face_falls_back_as_a_family(self):
        shutil.copytree(ROOT / "font", self.project / "font")
        for missing in TIMES_FILES:
            with self.subTest(missing=missing):
                target = self.project / "font" / missing
                target.unlink()
                try:
                    fonts = self.build()
                    self.assert_termes(fonts)
                    self.assertIn("font/FZXiaoBiaoSong.ttf", fonts["XBS"])
                finally:
                    shutil.copy2(ROOT / "font" / missing, target)

    def test_system_names_without_project_fonts(self):
        for source in (ROOT / "font").iterdir():
            shutil.copy2(source, self.system_fonts)
        fonts = self.build()
        for label in ("REG", "BOLD", "ITALIC", "BI"):
            self.assertIn("Times New Roman", fonts[label])
        self.assertIn("FZXiaoBiaoSong-B05S", fonts["XBS"])


if __name__ == "__main__":
    unittest.main()
