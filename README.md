# 西南财经大学硕士论文模块

修改自[上海交通大学论文](https://github.com/sjtug/sjtuthesis)模板，适用于西南财经大学硕士论文的撰写。


## 获取模板

### 下载模版

普通用户可以直接 `clone` 或者下载压缩包。

```bash
git clone https://github.com/SWUFE-DB-Group/SWUFE-Thesis.git
```

### Overleaf

您可以下载最新版压缩包，然后上传至Overleaf等平台。请注意，Overleaf 默认使用 pdflatex 编译，您需要设置使用 XeLaTeX 编译器。

## 模板使用

如果你不熟悉 LaTeX 的编译流程，请**不要**直接使用编译器进行编译。针对不同的平台，模版提供了相应的编译脚本。在编译前，需要安装最新的 TeXLive 发行版。

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
> - 在 JSON 字符串中，若包含 LaTeX 转义命令（例如 `\LaTeX`、`\quad`），需写为双反斜杠转义（如 `\\LaTeX{}`、`\\quad{}`）。
> - `display_zh` / `display_en` 可选，仅在封面标题需要手动控制断行（如 `标题第一行\\\\标题第二行`）时填写；留空时将自动使用 `title`。

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
  *(注：`review: false` 为终稿模式，`true` 为盲审模式；`hide_coverone_in_review: true` 可在盲审时跳过绿皮外封)*
- **在 `setup.tex` 中配置**：
  ```latex
  \sjtusetup{
    review                  = false,
    hide-coverone-in-review = false,
    ...
  }
  ```
*注：亦可在 [main.tex](file:///run/media/zhongpu/DATA/projects/latex/SWUFE-Thesis/main.tex) 的 `\documentclass[..., review]{sjtuthesis}` 中开启盲审。*

**模式行为差异：**

| 功能项 | 终稿模式 (`review = false`) | 盲审模式 (`review = true`) |
| :--- | :--- | :--- |
| **封面一（绿皮外封）** | 显示申请人与导师姓名 | 申请人与导师姓名自动留空（保留下划线横线）；若开启 `hide-coverone-in-review = true` 则直接跳过该页 |
| **封面二（扉页）** | 显示申请人、学号与导师姓名 | 申请人、学号与导师姓名自动留空（保留下划线横线） |
| **原创与版权声明页** | 正常输出带签名的声明页 | 自动略过不输出（防止手写签名泄密） |
| **致谢** | 正常输出 | 自动略过不输出（防止致谢内容泄密） |
| **页眉与成果目录** | 正常输出 | 页眉自动读取论文标题，成果目录保持规范匿名格式 |