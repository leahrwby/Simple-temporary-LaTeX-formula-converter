# LaTeX 公式转换器

一个面向 Word 用户的桌面小工具，用于把 LaTeX 公式或包含公式的科研文本转换为 Word 可编辑公式。

## 功能

- 纯公式转换：把单条 LaTeX 公式转换为 MathML 并复制到剪贴板，方便粘贴到 Word 公式编辑器。
- 整段文本转换：支持中文、普通文本和 `$...$` / `$$...$$` 包裹的 LaTeX 公式混排，并生成 Word 文档。
- 自动检测 Pandoc：首次运行如果未检测到 Pandoc，会尝试通过 `pypandoc` 自动下载。
- 窗口置顶：适合边看文献边转换公式。

## 运行环境

- Python 3.9 或更高版本
- Windows / macOS / Linux
- Microsoft Word 或其他支持 `.docx` / MathML 的编辑器

> Windows 用户通常需要安装 Python 时勾选 `Add Python to PATH`。

## 安装

克隆或下载本项目后，在项目目录中执行：

```bash
pip install -r requirements.txt
```

## 使用

启动程序：

```bash
python latex_to_word_app.py
```

Windows 用户也可以双击：

```text
run.bat
```

### 打包为 exe

```text
build_exe.bat
```

打包后的文件会生成在 `dist\latex公式转换器_免安装.exe`。

## 两种模式

### 主功能：纯公式转换

适合只转换一条公式，例如：

```latex
\rho = \frac{m}{V}
```

点击“仅转换纯公式 -> 复制到剪贴板”后，在 Word 中按 `Alt + =` 进入公式输入状态，再粘贴即可。

### 次功能：整段文本转换

适合包含文字和公式的内容，例如：

```text
我们知道，行内密度公式可以写为 $\rho = \frac{m}{V}$。

它的体积分形式如下：
$$ \bar{\rho} = \frac{1}{V} \int_V \rho(\mathbf{r}) d^3r $$
```

点击“智能排版并自动打开 Word”后，程序会生成 `Temp_Rendered_Paragraph.docx` 并自动打开。

## 常见问题

### 首次运行比较慢

首次运行可能会下载 Pandoc，取决于网络环境，等待完成后再次使用即可。

### 转换失败

请检查：

- LaTeX 公式语法是否正确。
- 整段文本模式中公式是否使用 `$...$` 或 `$$...$$` 包裹。
- 当前网络是否允许下载 Pandoc。

## 项目结构

```text
.
├── dist/
│   └── latex公式转换器_免安装.exe
├── latex_to_word_app.py
├── requirements.txt
├── run.bat
├── build_exe.bat
├── LICENSE
├── .gitignore
└── README.md
```

## 许可证

本项目使用 MIT License。
