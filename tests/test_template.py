"""Compile isolated template copies and check SJTUTeX migration behavior.

Run with: python3 -m unittest discover -s tests -v
Requires XeLaTeX, latexmk and Poppler; uses no Python dependencies.
"""

import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
import unicodedata
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ("xelatex", "latexmk", "pdfinfo", "pdftotext", "pdftohtml")


@unittest.skipUnless(all(shutil.which(tool) for tool in TOOLS), "TeX/Poppler required")
class TemplateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="swufe-template-test-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        for name in ("main.tex", "setup.tex", "swufe-layout.tex", "config.json"):
            shutil.copy2(ROOT / name, self.project / name)
        for name in ("contents", "figures", "font", "img"):
            shutil.copytree(ROOT / name, self.project / name)
        self.config = json.loads((self.project / "config.json").read_text())
        self.config["info"].update({
            "title": {
                "zh": "版本适配验证论文", "en": "A test of SJTUTeX compatibility",
                "display_zh": "", "display_en": "",
            },
            "author": {"zh": "验证申请人", "en": "Test Author"},
            "supervisor": {"zh": "验证导师", "en": "Test Supervisor"},
            "student_id": "2099123456",
            "keywords": {"zh": "版本迁移；配置校验", "en": "version migration; metadata"},
        })

    def build(self, config=True, succeeds=True, thesis=True):
        if config:
            (self.project / "config.json").write_text(
                json.dumps(self.config, ensure_ascii=False, indent=2)
            )
        else:
            (self.project / "config.json").unlink()
        # No project rc file: also tests the documented Overleaf upload contents.
        result = subprocess.run(
            ["latexmk", "-norc", "-xelatex", "-quiet", "-halt-on-error",
             "-interaction=nonstopmode", "-file-line-error", "main.tex"],
            cwd=self.project, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, timeout=120,
        )
        log = (self.project / "main.log").read_text(errors="replace")
        if not succeeds:
            self.assertNotEqual(result.returncode, 0)
            return log
        self.assertEqual(result.returncode, 0, log[-6000:])
        version = re.search(r"Document Class: sjtuthesis \S+ v?(\d+\.\d+\.\d+)", log)
        self.assertIsNotNone(version)
        self.assertGreaterEqual(tuple(map(int, version[1].split("."))), (2, 3, 1))
        for warning in ("undefined citations", "undefined references", "Rerun to get",
                        "Rerun LaTeX", "Label(s) may have changed",
                        "Unknown key", "unknown key", "Overfull", "Missing character",
                        "Package fancyhdr Warning"):
            self.assertFalse(warning in log, warning)
        pdf = str(self.project / "main.pdf")
        self.info = subprocess.check_output(["pdfinfo", pdf], text=True)
        self.text = unicodedata.normalize("NFC", subprocess.check_output(
            ["pdftotext", "-layout", pdf, "-"], text=True
        ))
        self.compact = re.sub(r"\s", "", self.text)
        self.pages = self.text.split("\f")
        if not thesis:
            return log
        toc = (self.project / "main.toc").read_text()
        self.assertNotIn("Abstract", toc)
        self.assertNotIn("摘要", re.sub(r"\s", "", toc))
        self.assertIn("Key words:", self.text)
        self.assertIn("关键词：", self.text)

    def assert_review(self, cover_count):
        for identity in ("验证申请人", "验证导师", "2099123456"):
            self.assertNotIn(identity, self.compact + self.info)
        self.assertNotIn("原创性及知识产权声明", self.compact)
        self.assertNotIn("致谢的文字", self.compact)
        self.assertIsNone(re.search(r"^Author:[^\S\r\n]*\S", self.info, re.MULTILINE))
        self.assertEqual(self.compact.count("学位申请人:"), cover_count)
        self.assertIn("版本适配验证论文", self.compact)

    def test_json_final_and_title_fallback(self):
        self.build()
        for value in ("验证申请人", "验证导师", "2099123456", "版本迁移；配置校验"):
            self.assertIn(value, self.compact)
        self.assertIn("A test of SJTUTeX compatibility", self.text)
        self.assertIn("version migration; metadata", self.text)
        self.assertIn("原创性及知识产权声明", self.compact)
        self.assertIn("致谢的文字", self.compact)
        self.assertIn("Author:          验证申请人", self.info)
        self.assertIn("Subject:         西南财经大学学位论文", self.info)
        self.assertEqual(self.compact.count("学位申请人:"), 2)

    def test_json_review_with_cover(self):
        self.config["review"] = True
        self.build()
        self.assert_review(2)

    def test_json_review_without_cover(self):
        self.config.update(review=True, hide_coverone_in_review=True)
        self.build()
        self.assert_review(1)
        self.assertIn("分类号", self.pages[0])

    def test_display_title_and_metadata(self):
        self.config["info"]["title"].update(
            display_zh=r"封面标题第一行\\封面标题第二行",
            display_en=r"A custom first line\\a custom second line",
        )
        self.build()
        self.assertIn("封面标题第一行", self.pages[0])
        self.assertIn("封面标题第二行", self.pages[0])
        self.assertIn("A custom first line", self.pages[0])
        self.assertIn("a custom second line", self.pages[0])
        self.assertIn("Title:           版本适配验证论文", self.info)
        self.assertNotIn("封面标题第一行", self.info)

    def configure_setup(self):
        path = self.project / "setup.tex"
        source = path.read_text()
        source = source.replace("某\\quad{}某", "验证申请人").replace("某某教授", "验证导师")
        source = source.replace("0010900990", "2099123456")
        source = source.replace("西南财经大学学位论文 \\LaTeX{} 模板示例文档", "版本适配验证论文")
        source = source.replace("% date                 = {2026-03-01},",
                                "date                 = {2026-04-12},")
        source = source.replace("final-date           = {2026年3月}", "final-date           = {}")
        path.write_text(source)

    def test_setup_fallback_and_date(self):
        self.configure_setup()
        self.build(config=False)
        for value in ("验证申请人", "验证导师", "2099123456", "2026年4月12日"):
            self.assertIn(value, self.compact)
        self.assertIn("Author:          验证申请人", self.info)

    def test_setup_review(self):
        self.configure_setup()
        path = self.project / "setup.tex"
        path.write_text(path.read_text().replace(
            "review                  = false,", "review                  = true,"
        ))
        self.build(config=False)
        self.assert_review(2)

    def test_old_class_is_rejected(self):
        (self.project / "sjtuthesis.cls").write_text(
            r"\ProvidesClass{sjtuthesis}[2024/06/29 v2.1.3 test stub]" "\n"
            r"\LoadClass{article}" "\n"
        )
        self.assertIn("SJTUTeX 2.3.1 or newer is required", self.build(succeeds=False))

    LAYOUT_PROBE = r"""
\makeatletter
\newcommand{\swufelayoutprobe}{%
\typeout{SWUFE-WIDTH=\the\textwidth}%
\typeout{SWUFE-HEIGHT=\the\textheight}%
\typeout{SWUFE-HEADWIDTH=\the\headwidth}%
\typeout{SWUFE-LEFT=\the\dimexpr1in+\hoffset+\oddsidemargin\relax}%
\typeout{SWUFE-RIGHT=\the\dimexpr\paperwidth-1in-\hoffset-\oddsidemargin-\textwidth\relax}%
\typeout{SWUFE-TOP=\the\dimexpr1in+\voffset+\topmargin+\headheight+\headsep\relax}%
\typeout{SWUFE-BOTTOM=\the\dimexpr\paperheight-1in-\voffset-\topmargin-\headheight-\headsep-\textheight\relax}%
\typeout{SWUFE-HEADER=\the\dimexpr1in+\voffset+\topmargin\relax}%
\typeout{SWUFE-FOOTER=\the\dimexpr\paperheight-1in-\voffset-\topmargin-\headheight-\headsep-\textheight-\footskip\relax}%
\typeout{SWUFE-BASELINE=\the\baselineskip}%
\typeout{SWUFE-STRETCH=\baselinestretch}%
\typeout{SWUFE-FLOATGAP=\the\intextsep}%
}
\makeatother
"""

    def assert_layout(self, log):
        expected_cm = {
            "WIDTH": 14.1, "HEIGHT": 22.4, "HEADWIDTH": 14.1,
            "LEFT": 3.45, "RIGHT": 3.45,
            "TOP": 3.9, "BOTTOM": 3.4, "HEADER": 2.8, "FOOTER": 2.5,
            "BASELINE": 22.4 / 30, "FLOATGAP": 22.4 / 60,
        }
        for key, value in expected_cm.items():
            match = re.search(r"SWUFE-" + key + r"=([\d.]+)pt", log)
            self.assertIsNotNone(match, key)
            self.assertAlmostEqual(float(match[1]) / 72.27 * 2.54, value, places=4)
        self.assertIn("SWUFE-STRETCH=1.37", log)

    def test_geometry_restored_after_covers(self):
        path = self.project / "main.tex"
        source = path.read_text().replace(
            r"\begin{document}", self.LAYOUT_PROBE + r"\begin{document}"
        ).replace(r"\mainmatter", r"\mainmatter\swufelayoutprobe")
        path.write_text(source)
        self.build()
        self.assert_layout((self.project / "main.log").read_text())

    def test_print_grid_and_fonts(self):
        source = r"""\documentclass[type=master,openany,oneside,cjk-font=fandol,baselineskip=false]{sjtuthesis}
\input{setup}
""" + self.LAYOUT_PROBE + r"""
\begin{document}
\swufelayoutprobe
\noindent
""" + "测" * (33 * 65) + r"""
\par\clearpage
\chapter{一级标题测量}
\section{二级标题测量}
\subsection{三级标题测量}
正文测量
\begin{table}[h]
\caption{表题测量}
\centering\begin{tabular}{cc}表格内容 & 测量内容\\\end{tabular}
\swufetablenote{注：表注测量}
\end{table}
\begin{figure}[h]
\centering\rule{2cm}{1cm}
\caption{图题测量}
\end{figure}
\end{document}
"""
        (self.project / "main.tex").write_text(source)
        log = self.build(thesis=False)
        self.assert_layout(log)
        pdf = str(self.project / "main.pdf")
        xml = self.project / "layout.xml"
        subprocess.run(
            ["pdftohtml", "-xml", "-i", "-hidden", "-zoom", "1", pdf, str(xml)],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        root = ET.parse(xml).getroot()
        fonts = {font.attrib["id"]: font.attrib for font in root.iter("fontspec")}
        pages = root.findall("page")
        for page in pages[:2]:
            rows = [node for node in page.findall("text") if "测测测测" in "".join(node.itertext())]
            self.assertEqual(len(rows), 30)
            self.assertEqual({len("".join(row.itertext())) for row in rows}, {33})
            for node in page.findall("text"):
                if int(node.attrib["top"]) > 700 and "".join(node.itertext()).isdigit():
                    self.assertIn("FandolSong", fonts[node.attrib["font"]]["family"])
                    self.assertEqual(fonts[node.attrib["font"]]["size"], "9")
        expected = {
            "一级标题测量": ("FZXBSJW", "22"),
            "二级标题测量": ("FandolHei", "15"),
            "三级标题测量": ("FandolHei", "12"),
            "正文测量": ("FandolSong", "12"),
            "表题测量": ("FandolHei", "11"),
            "表格内容": ("FandolSong", "11"),
            "图题测量": ("FandolSong", "11"),
            "注：表注测量": ("FandolSong", "9"),
        }
        for label, (family, size) in expected.items():
            nodes = [node for node in root.iter("text") if label in "".join(node.itertext())]
            self.assertEqual(len(nodes), 1, label)
            self.assertIn(family, fonts[nodes[0].attrib["font"]]["family"])
            # pdftohtml rounds 10.5 to 11; a four-character width verifies 10.5 exactly.
            self.assertEqual(fonts[nodes[0].attrib["font"]]["size"], size)
            if label == "表格内容":
                self.assertEqual(nodes[0].attrib["width"], "42")


if __name__ == "__main__":
    unittest.main()
