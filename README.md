# 西南财经大学硕士论文模块

修改自[上海交通大学论文](https://github.com/sjtug/sjtuthesis)模板，适用于西南财经大学硕士论文的撰写。

## 格式依据与符合情况

格式要求参考西南财经大学研究生院发布的[《西南财经大学关于研究生学位论文形式与格式的基本要求》](https://graduate.swufe.edu.cn/info/1036/2142.htm)。该网页发布于 2018-11-13，正文注明“2007年3月修订”，并附有“2019年5月调整”的 Word 文件。

模板的五项印刷格式设置集中在 [`swufe-layout.tex`](swufe-layout.tex)：A4；正文上、下、左、右边距分别为 3.9、3.4、3.45、3.45 cm；小四号宋体，以 1.37 倍率校准到每页 30 行、每行 33 个全角汉字；一级标题二号方正小标宋、二级小三号黑体、三级小四号黑体；图表五号、表题黑体、内容宋体、表注小五号宋体；页眉页脚小五号宋体，奇偶页页眉不同。

页眉框顶边距纸顶 2.8 cm，页码基线距纸底 2.5 cm。封面使用独立版心；含标题、图表、公式或段落留白的页面不要求实际填满 30 行。2026-10-16 的回归检查已验证连续正文页面为 **30 行 × 33 字**，同时核对了正文、标题、图表和页码的字体字号。具体实测值、参数定义和核查范围见[排版核查记录](docs/layout-audit.md)。

`font/FZXiaoBiaoSong.ttf` 用于一级标题，来源为[提供的字体仓库](https://github.com/genqiaolynn/fonts/blob/master/%E6%96%B9%E6%AD%A3%E5%B0%8F%E6%A0%87%E5%AE%8B%E7%AE%80%E4%BD%93.ttf)；`STZHONGS.TTF` 是内封使用的华文中宋。四个 Times New Roman 文件用于西文。正文宋体、黑体以及页眉页码使用的宋体由 TeX Live 的 Fandol 字体提供。

## 编译环境与版本要求

本项目已适配 **SJTUTeX 2.3.1（2026-02-26）**，最低要求为该版本，使用 **XeLaTeX** 编译。推荐使用 **TeX Live 2026**；使用其他发行版时，请确认已安装 `sjtutex` 2.3.1 或更新版本，以及 `jsonparse` 等依赖宏包。当前验证环境为 TeX Live 2026 / SJTUTeX 2.3.1；更新版本仍需确认兼容性。

[SJTUTeX 已被 CTAN 收录，并由 TeX Live、MiKTeX 分发](https://ctan.org/pkg/sjtutex)。本项目直接使用发行版安装的文档类，不再附带旧版 `texmf/`，也不需要配置本地 `TEXINPUTS`。西财专用的封面、格式与 JSON 配置仍由本项目提供，`font/`、`figures/` 和示例正文引用的 `img/` 目录仍需完整保留。

使用 TeX Live 官方安装器安装的环境，可通过以下命令安装或更新依赖：

```bash
tlmgr update --self
tlmgr install sjtutex jsonparse
tlmgr update sjtutex jsonparse
```

若 TeX Live 由操作系统包管理器安装，请通过对应包管理器安装或更新；MiKTeX 用户可在 MiKTeX Console 中安装并更新宏包。

编译日志开头应显示 `Document Class: sjtuthesis ... 2.3.1 ...`（或更新版本）。从旧版项目迁移时，请移除旧的 `texmf/` 和自定义 `TEXINPUTS` 搜索配置，避免旧文档类覆盖发行版中的版本。摘要与目录已使用 2.3.1 的接口：`abstract` 环境（如 `[lang=zh,notintoc]`）和 `\tableofcontents[notintoc]`。

修改模板后，可运行 `python3 -m unittest discover -s tests -v` 检查 JSON 配置、`setup.tex` 回退配置、终稿与盲审模式、封面标题、版心恢复、30 行 × 33 字、字体字号及旧版本检测。检查需要 Python 3、XeLaTeX、`latexmk` 和 Poppler 的 `pdfinfo`、`pdftotext`、`pdftohtml`，会在临时目录中编译，不修改论文内容。

## 获取模板

### 下载模版

普通用户可以直接 `clone` 或者下载压缩包。

```bash
git clone https://github.com/SWUFE-DB-Group/SWUFE-Thesis.git
```

### Overleaf

使用 Overleaf 在线编译时，请按以下步骤操作：

1. 将项目源文件打包为 ZIP，保留根目录下的 `main.tex`、`setup.tex`、`swufe-layout.tex`、`config.json`，以及完整的 `contents/`、`figures/`、`font/`、`img/` 目录。
2. 在 Overleaf 中选择 **New Project → Upload Project**，上传 ZIP。上传后确认 `main.tex` 位于在线项目根目录。
3. 在项目设置中，将 **Main document** 设为 `main.tex`，将 **Compiler** 设为 **XeLaTeX**，将 **TeX Live version** 设为 **2026**（[Overleaf 已提供 TeX Live 2026](https://www.overleaf.com/blog/tex-live-2026-is-now-available)）。该流程直接使用平台安装的 SJTUTeX，无需上传 `texmf/` 或创建、重命名 `latexmkrc`；项目中的 `.latexmkrc` 用于本地 `latexmk` 编译。
4. 修改 `config.json` 中的论文信息和 `contents/` 中的论文内容，点击 **Recompile**，编译完成后下载 PDF。若提示 `SJTUTeX 2.3.1 or newer is required`，请检查 TeX Live 版本，并确认在线项目中没有残留的旧版文档类。

## 模板使用

如果你不熟悉 LaTeX 的编译流程，推荐使用下列编译工具和脚本，以自动处理交叉引用与多轮编译。编译前请满足上述版本要求。

### VSCode 用户

安装 “LaTeX Workshop” 后，选择 `Recipe: latexmk (xelatex)` 编译即可，并在设置中将 `latex-workshop.latex.recipe.default` 改为 `lastUsed` 以一直使用该选项编译。

### Linux 与 macOS 用户

推荐使用模版提供的 `Makefile` 进行编译，具体来说我们提供了如下几条可用的命令：

```bash
make all                      # 编译生成 main.pdf
make clean                    # 删除编译所产生的中间文件
make cleanall                 # 删除 main.pdf 和所有中间文件
make wordcount                # 论文字数统计
```

### Windows 用户

对于 Windows 用户，我们也提供了编译脚本 `Compile.bat`。可以双击直接编译，也可以在命令提示符窗口中使用脚本提供的额外功能：

```bash
.\Compile.bat thesis          # 编译生成 main.pdf
.\Compile.bat clean           # 删除编译所产生的中间文件
.\Compile.bat cleanall        # 删除 main.pdf 和所有中间文件
.\Compile.bat wordcount       # 论文字数统计
```

## 论文信息配置与模式切换

本项目支持两种配置方式：

1. **JSON 配置文件（推荐，零依赖）**：直接编辑根目录下的 `config.json`，无需接触 LaTeX 代码。
2. **LaTeX 配置文件**：若无 `config.json`（或将其删除），则自动无缝回退至 [setup.tex](file:///run/media/zhongpu/DATA/projects/latex/SWUFE-Thesis/setup.tex) 中的原生设置。

### 1. 方式一：使用 `config.json` 配置（推荐）

模板基于 TeX Live 内置的 `jsonparse` 宏包实现了**原生零依赖**的 JSON 解析，**无需安装 Python、无需开启 `--shell-escape`，在本地与 Overleaf 均可开箱即用**。

编辑根目录下的 [config.json](file:///run/media/zhongpu/DATA/projects/latex/SWUFE-Thesis/config.json) 即可统一管理论文元数据与模式：

```json
{
  "review": false,
  "hide_coverone_in_review": false,
  "info": {
    "title": {
      "zh": "西南财经大学学位论文 \\LaTeX{} 模板示例文档",
      "en": "A Sample Document for \\LaTeX-based SWUFE Thesis Template",
      "display_zh": "",
      "display_en": ""
    },
    "keywords": {
      "zh": "西南财经大学；历史沿革；211工程",
      "en": "SWUFE; LaTeX; Python"
    },
    "author": {
      "zh": "某\\quad{}某",
      "en": "Mo Mo"
    },
    "supervisor": {
      "zh": "某某教授",
      "en": "Prof.\\ Mou Mou"
    },
    "student_id": "0010900990",
    "degree": {
      "zh": "工学硕士",
      "en": "Master of Engineering"
    },
    "major": {
      "zh": "计算机科学与技术",
      "en": "Computer Science and Technology"
    },
    "research_direction": "大模型",
    "department": {
      "zh": "计算机与人工智能学院",
      "en": "School of Computing and Artificial Intelligence"
    },
    "classification": "",
    "secret_level": "",
    "udc": "",
    "final_date": "2026年3月"
  }
}
```

> **注意**：
>
> - **关于注释**：标准 JSON 规范（RFC 8259）**不支持** `//` 或 `/* */` 注释，直接添加会导致编译报错。如需添加说明，建议使用 `"_comment": "说明文字"` 形式的键值（模板会自动忽略所有未定义的额外键），或者直接使用下述方式二的 [setup.tex](file:///run/media/zhongpu/DATA/projects/latex/SWUFE-Thesis/setup.tex)（原生支持 `%` 注释）。
> - **转义字符**：在 JSON 字符串中，若包含 LaTeX 转义命令（例如 `\LaTeX`、`\quad`），需写为双反斜杠转义（如 `\\LaTeX{}`、`\\quad{}`）。
> - **换行标题**：`display_zh` / `display_en` 可选，仅在封面标题需要手动控制断行（如 `标题第一行\\\\标题第二行`）时填写；留空时将自动使用 `title`。

---

### 2. 方式二：直接在 `setup.tex` 中配置

如果不使用 `config.json`，直接删除或重命名该文件即可。论文的所有核心信息均在 [setup.tex](file:///run/media/zhongpu/DATA/projects/latex/SWUFE-Thesis/setup.tex) 的 `\sjtusetup{ info = { ... } }` 中集中配置：

- `zh / title`、`en / title`：中英文标题（页眉、PDF 书签与元数据自动同步）
- `zh / display-title`、`en / display-title`：封面换行标题（可选，支持用 `\\` 手动换行）
- `zh / author`、`en / author`：作者姓名
- `zh / supervisor`、`en / supervisor`：指导教师姓名
- `id`：学号
- `zh / major`、`zh / degree`：学科专业、学位类别
- `zh / research-direction`：研究方向（封面二自动读取）
- `classification`、`secret-level`、`udc`：分类号、密级、UDC（封面二自动读取）
- `final-date`：定稿时间（封面二自动读取，未填时自动使用当前年月）

---

### 3. 盲审 / 终稿 模式切换

无论使用 `config.json` 还是 `setup.tex`，均可一键切换盲审与终稿模式：

- **在 `config.json` 中配置**：

  ```json
  "review": false,
  "hide_coverone_in_review": false
  ```

  _(注：`review: false` 为终稿模式，`true` 为盲审模式；`hide_coverone_in_review: true` 可在盲审时跳过绿皮外封)_
- **在 `setup.tex` 中配置**：

  ```latex
  \sjtusetup{
    review                  = false,
    hide-coverone-in-review = false,
    ...
  }
  ```

_注：亦可在 [main.tex](file:///run/media/zhongpu/DATA/projects/latex/SWUFE-Thesis/main.tex) 的 `\documentclass[..., review]{sjtuthesis}` 中开启盲审。_

**模式行为差异：**

| 功能项                 | 终稿模式 (`review = false`) | 盲审模式 (`review = true`)                                                                         |
| :--------------------- | :-------------------------- | :------------------------------------------------------------------------------------------------- |
| **封面一（绿皮外封）** | 显示申请人与导师姓名        | 申请人与导师姓名自动留空（保留下划线横线）；若开启 `hide-coverone-in-review = true` 则直接跳过该页 |
| **封面二（扉页）**     | 显示申请人、学号与导师姓名  | 申请人、学号与导师姓名自动留空（保留下划线横线）                                                   |
| **原创与版权声明页**   | 正常输出带签名的声明页      | 自动略过不输出（防止手写签名泄密）                                                                 |
| **致谢**               | 正常输出                    | 自动略过不输出（防止致谢内容泄密）                                                                 |
| **页眉与成果目录**     | 正常输出                    | 页眉自动读取论文标题，成果目录保持规范匿名格式                                                     |

