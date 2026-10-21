# 西南财经大学硕士论文模块

修改自[上海交通大学论文](https://github.com/sjtug/sjtuthesis)模板，适用于西南财经大学硕士论文的撰写。

**[查看示例 PDF](https://github.com/SWUFE-DB-Group/SWUFE-Thesis/blob/main/example.pdf)**：可在 GitHub 中预览或下载，查看封面、正文、图表和参考文献的排版效果。示例由当前模板编译生成；更新示例时，运行 `make all` 后将 `main.pdf` 复制为 `example.pdf`。

## 格式依据与符合情况

格式要求参考西南财经大学研究生院发布的[《西南财经大学关于研究生学位论文形式与格式的基本要求》](https://graduate.swufe.edu.cn/info/1036/2142.htm)。该网页发布于 2018-11-13，正文注明“2007年3月修订”，并附有“2019年5月调整”的 Word 文件。

模板的五项印刷格式设置集中在 [`swufe-layout.tex`](swufe-layout.tex)：A4；正文上、下、左、右边距分别为 3.9、3.4、3.45、3.45 cm；小四号宋体，以 1.37 倍率校准到每页 30 行、每行 33 个全角汉字；一级标题默认二号方正小标宋、二级小三号黑体、三级小四号黑体；图表五号、表题黑体、内容宋体、表注小五号宋体；页眉页脚小五号宋体，奇偶页页眉不同。

页眉框顶边距纸顶 2.8 cm，页码基线距纸底 2.5 cm。封面使用独立版心；含标题、图表、公式或段落留白的页面不要求实际填满 30 行。2026-10-16 的回归检查已验证连续正文页面为 **30 行 × 33 字**，同时核对了正文、标题、图表和页码的字体字号。具体实测值、参数定义和核查范围见[排版核查记录](docs/layout-audit.md)。

`font/` 中的字体用于让编译结果更贴近模板原始样式：`FZXiaoBiaoSong.ttf` 用于一级标题，来源为[提供的字体仓库](https://github.com/genqiaolynn/fonts/blob/master/%E6%96%B9%E6%AD%A3%E5%B0%8F%E6%A0%87%E5%AE%8B%E7%AE%80%E4%BD%93.ttf)；`STZHONGS.TTF` 是内封使用的华文中宋；四个 Times New Roman 文件用于西文。每类字体依次尝试项目内文件、系统安装的同名字体，再使用 TeX Live 替代字体。缺少 `font/` 时，如果系统安装有相应字体仍会使用；否则西文回退到 TeX Gyre Termes，小标宋和华文中宋回退到 FandolSong。回退后仍可编译，但替代字体的字形和换行可能有差异；正文宋体、黑体和页眉宋体本来就使用 TeX Live 的 Fandol 字体。

项目内的 Times New Roman 常规、粗体、斜体、粗斜体四个文件需全部存在；缺少任意一个时，整个西文字体族进入后续回退。TeX Gyre Termes 按发行版中的 `.otf` 文件加载，不依赖系统字体名称注册。**FandolSong 仅是宋体风格替代，并非小标宋；一级标题使用该回退时不再严格满足小标宋要求。用于终稿时，应保留项目中的小标宋文件或在系统中安装同名字体。**

## 编译环境与版本要求

本项目已适配 **SJTUTeX 2.3.1（2026-02-26）**，最低要求为该版本，使用 **XeLaTeX** 编译。推荐使用 **TeX Live 2026**；使用其他发行版时，请确认已安装 `sjtutex` 2.3.1 或更新版本，以及 `jsonparse` 等依赖宏包。当前验证环境为 TeX Live 2026 / SJTUTeX 2.3.1；更新版本仍需确认兼容性。

[SJTUTeX 已被 CTAN 收录，并由 TeX Live、MiKTeX 分发](https://ctan.org/pkg/sjtutex)。本项目直接使用发行版安装的文档类，不再附带旧版 `texmf/`，也不需要配置本地 `TEXINPUTS`。西财专用的封面、格式与 JSON 配置仍由本项目提供；`figures/` 和示例正文引用的 `img/` 目录需保留，`font/` 可选，缺少时按上述顺序回退。

使用 TeX Live 官方安装器安装的环境，可通过以下命令安装或更新依赖：

```bash
tlmgr update --self
tlmgr install sjtutex jsonparse
tlmgr update sjtutex jsonparse
```

若 TeX Live 由操作系统包管理器安装，请通过对应包管理器安装或更新；MiKTeX 用户可在 MiKTeX Console 中安装并更新宏包。

编译日志开头应显示 `Document Class: sjtuthesis ... 2.3.1 ...`（或更新版本）。从旧版项目迁移时，请移除旧的 `texmf/` 和自定义 `TEXINPUTS` 搜索配置，避免旧文档类覆盖发行版中的版本。摘要与目录已使用 2.3.1 的接口：`abstract` 环境（如 `[lang=zh,notintoc]`）和 `\tableofcontents[notintoc]`。

修改模板后，可运行 `python3 -m unittest discover -s tests -v` 检查 JSON 配置、`setup.tex` 回退配置、终稿与盲审模式、封面标题、版心恢复、30 行 × 33 字、字体字号、引用风格及编号排序压缩、旧版本检测。检查需要 Python 3、XeLaTeX、`latexmk` 和 Poppler 的 `pdfinfo`、`pdftotext`、`pdftohtml`，会在临时目录中编译，不修改论文内容。Linux 环境安装了 fontconfig 的 `fc-match` 时，还会检查无项目及系统字体、项目西文字体文件不完整，以及系统同名字体回退三种情形。

## 获取模板

### 下载发布版本

[GitHub Releases](https://github.com/SWUFE-DB-Group/SWUFE-Thesis/releases) 提供两种 ZIP：

| 文件名后缀 | 内容 |
| --- | --- |
| `-with-font.zip` | 模板源码、编译脚本和完整的 `font/`，保留示例使用的字体 |
| `-without-font.zip` | 相同的模板源码和编译脚本，省略 `font/`，使用系统同名字体或 TeX 发行版替代字体 |

两个 ZIP 均保留 `main.tex`、`setup.tex`、`swufe-layout.tex`、`config.json`、`refs.bib`、`contents/`、`figures/`、`img/`、`docs/`、使用说明和许可证。`main.tex` 位于 ZIP 根目录，可直接上传 Overleaf。ZIP 不包含示例 PDF、编译产物、测试及工作流文件；字体回退的效果及终稿使用限制见上文。

### Overleaf

使用 Overleaf 在线编译时，请按以下步骤操作：

1. 将项目源文件打包为 ZIP，保留根目录下的 `main.tex`、`setup.tex`、`swufe-layout.tex`、`config.json`，以及完整的 `contents/`、`figures/`、`img/` 目录。为了获得与示例更接近的字体效果，可一并保留 `font/`；省略时会自动按上述字体回退顺序处理。
2. 在 Overleaf 中选择 **New Project → Upload Project**，上传 ZIP。上传后确认 `main.tex` 位于在线项目根目录。
3. 在项目设置中，将 **Main document** 设为 `main.tex`，将 **Compiler** 设为 **XeLaTeX**，将 **TeX Live version** 设为 **2026**（[Overleaf 已提供 TeX Live 2026](https://www.overleaf.com/blog/tex-live-2026-is-now-available)）。该流程直接使用平台安装的 SJTUTeX，无需上传 `texmf/` 或创建、重命名 `latexmkrc`；项目中的 `.latexmkrc` 用于本地 `latexmk` 编译。
4. 修改 `config.json` 中的论文信息和 `contents/` 中的论文内容，点击 **Recompile**，编译完成后下载 PDF。若提示 `SJTUTeX 2.3.1 or newer is required`，请检查 TeX Live 版本，并确认在线项目中没有残留的旧版文档类。

## 模板使用

如果你不熟悉 LaTeX 的编译流程，推荐使用下列编译工具和脚本，以自动处理交叉引用与多轮编译。编译前请满足上述版本要求。

### TexLite（推荐）

推荐使用 **[TexLite](https://swufe-db-group.github.io/TexLite/)** 撰写论文。TexLite 是轻量、自托管的 LaTeX 工作台，在浏览器中集成编辑、编译和 PDF 预览，并支持实时协作，使用本机或服务器上的实际 TeX 环境。欢迎访问官网了解安装和使用方法；编译本模板时，请满足上述版本要求，并选择 **XeLaTeX**。

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

## 排版示例

基础图片、子图、三线表、公式、列表和文献引用见 [`contents/绪论.tex`](contents/绪论.tex)。新增的 [`contents/排版示例.tex`](contents/排版示例.tex) 已由 `main.tex` 加载，可直接编译并查看以下效果：

| 示例 | 环境或宏包 |
| --- | --- |
| 二分查找伪代码：输入、输出、循环、分支、行号与交叉引用 | `algorithm2e` 的 `algorithm` |
| Python、SQL 代码块，以及行内代码和外部源文件引入命令 | `listings` 的 `codeblock`、`\lstinline`、`\lstinputlisting` |
| 带分支和回路的训练流程图 | TikZ，含 `positioning`、`arrows.meta` |
| 带坐标轴、图例及不同线型的示例曲线 | PGFPlots |
| 定义、定理、证明、对齐公式、矩阵和分段函数 | SJTUTeX 与 `amsthm`、`mathtools` |
| 数值、单位、小数点对齐表格和表注 | `siunitx`、`threeparttable` |

这些示例参考 [SJTUTeX 使用说明](https://mirrors.ctan.org/macros/latex/contrib/sjtutex/sjtutex.pdf) 中的算法和数学环境功能。SJTUTeX 负责相应名称和编号的适配；代码和绘图功能通过 `setup.tex` 中显式加载的宏包提供。全部示例只需 XeLaTeX，无需 Python、Pygments、`shell-escape` 或 TikZ 外部化。表格和曲线中的数值仅用于排版演示。

`codeblock` 默认自动折行，保留代码中的美元符号等字符，使用小五号等宽字体和 12 磅行距。可用 `numbers=left` 开启行号；短代码可加 `float=htbp` 作为完整浮动块，避免被拆到两页。需要在代码中嵌入 LaTeX 时，再对单个代码块开启 `mathescape`、`texcl` 或 `escapeinside`。算法、代码标题等排版参数集中在 `swufe-layout.tex`，代码配色和语法设置在 `setup.tex`。

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
  "citation_superscript": false,
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

### 4. 引用编号风格

默认使用与正文同一基线的方括号数字引用，如 `[1]`、`[1,3]`。同一组引用会按编号排序，三个及以上连续编号自动压缩为横线范围，如 `[1–3]`、`[1–3,5]`；两个连续编号仍显示为 `[1,2]`。两种风格都使用逗号分隔，并支持连续编号压缩。

在 `config.json` 根层设置 `"citation_superscript": false`（默认）使用平排引用，改为 `true` 使用上标引用。未填写此键时，沿用 `setup.tex` 中的设置，模板默认值为 `false`。

若不使用 JSON，可在 `setup.tex` 的 `\sjtusetup{...}` 中设置：

```latex
\sjtusetup{
  citation-superscript = false, % true 为上标引用
}
```

存在 JSON 且填写了 `citation_superscript` 时，以 JSON 为准。正文继续使用 `\cite{文献键}` 或 `\cite{文献键一,文献键二,...}`，不需要手动改写编号或范围。

参考文献列表保留小四字号和正文校准后的 1.37 倍行距，条目间不再额外加空白（`\bibsep=0pt`）。相邻条目与条目内换行使用一致的行距，相关设置集中在 `swufe-layout.tex`。

## 发布版本

`.github/workflows/release.yml` 在推送任意 tag 时触发，为该 tag 创建一个 GitHub Release，并上传 `with-font`、`without-font` 两个 ZIP。例如，在包含该工作流的提交上创建并推送 tag：

```bash
git tag v1.0.0
git push origin v1.0.0
```

生成的附件名为 `SWUFE-Thesis-v1.0.0-with-font.zip` 和 `SWUFE-Thesis-v1.0.0-without-font.zip`。工作流使用内置的 `GITHUB_TOKEN` 和 `contents: write` 权限，无需额外令牌；同一 tag 的工作流重跑时，会更新已有 Release 中同名的 ZIP。工作流打包 tag 对应的已跟踪模板文件，不在发布时重新编译论文。

也可在项目根目录本地打包：

```bash
python3 scripts/package_release.py v1.0.0
```

默认输出到 `build/release/`，可通过 `--output-dir` 指定其他目录。发布打包要求六个项目字体文件完整，以确保 `with-font` 包含全部字体；`without-font` 会从相同输入中排除整个 `font/`。打包检查只需 Python 3 和 Git，可单独运行：

```bash
python3 -m unittest discover -s tests -p test_release.py -v
```

