# PPTX2MD

[English](README.md) | [简体中文](README_CN.md)

[![Downloads](https://pepy.tech/badge/pptx2md)](https://pepy.tech/project/pptx2md)

一个将 PowerPoint `.pptx` 文件转换为 Markdown 的工具。

## 关于这个 Fork

这个 fork 主要用于个人维护和日常使用。上游仓库积累了一些未合并的 PR 和未发布的修复，因此这里保留了一份可直接安装使用的版本。

当前 fork 包含以下本地修复：

- 处理「幻灯片存在备注页，但备注文本框为空」导致的转换崩溃。
- 修复清理损坏的 `NULL` 关系时使用固定 `_purged.pptx` 文件名的问题，避免临时文件冲突。
- 将图片编号状态限制在单次解析过程内，避免解析器级别的可变全局状态。

如果你需要这些修复，请从这个 fork 安装，而不是从 PyPI 安装上游发布包。

## 保留的格式

- 标题。支持通过模糊匹配使用自定义目录。
- 任意层级的列表。
- 文本中的 **加粗**、_斜体_、颜色和 [超链接](https://github.com/ssine/pptx2md/blob/master/README.md)。
- 图片。图片会被提取到文件中，并在 Markdown 中插入相对路径。
- 含合并单元格的表格。
- 按「从上到下、从左到右」的顺序处理内容块。

## 支持的输出格式

- Markdown
- [TiddlyWiki](https://tiddlywiki.com/) 的 wikitext
- [Madoko](https://www.madoko.net/)
- [Quarto](https://quarto.org/)

## 安装与使用

### 安装

这个 fork 的修复可能还没有发布到 PyPI。不要使用下面这个命令：

```sh
pip install pptx2md
```

这个命令会安装 PyPI 上的上游发布包，而不是当前 fork。

请直接从 Git 安装：

```sh
pip install --upgrade "git+https://github.com/BinaryHusk/pptx2md.git"
```

如果要进行本地开发，可以 clone 仓库并使用 editable 模式安装：

```sh
git clone https://github.com/BinaryHusk/pptx2md.git
cd pptx2md
pip install -e .
```

### 使用

安装完成后，使用下面的命令将 `.pptx` 文件转换为 Markdown：

```sh
pptx2md input.pptx
```

默认输出文件名为 `out.md`，提取出的图片会保存到 `img/` 目录，并在 Markdown 中以相对路径引用。

旧版 `.ppt` 文件不受支持，请先将它转换为新版 `.pptx` 文件。

### 升级与卸载

```sh
pip install --upgrade "git+https://github.com/BinaryHusk/pptx2md.git"

pip uninstall pptx2md
```

## 自定义标题

默认情况下，工具会把所有 PPTX 标题解析为 `level 1` 的 Markdown 标题。如果你需要生成分层目录，可以准备一个标题列表文件，并通过 `-t` 参数传入。

标题文件示例（`titles.txt`）：

```text
Heading 1
  Heading 1.1
    Heading 1.1.1
  Heading 1.2
  Heading 1.3
Heading 2
  Heading 2.1
  Heading 2.2
    Heading 2.1.1
    Heading 2.1.2
  Heading 2.3
Heading 3
```

标题文件中，第一次出现缩进的行会被视为二级标题，并以该行的空格数作为缩进单位。比如 `  Heading 1.1` 有 2 个前导空格，会输出为 `## Heading 1.1`；`    Heading 1.1.1` 有 4 个前导空格，会输出为 `### Heading 1.1.1`。

工具会用模糊匹配将 PPTX 中的标题匹配到标题文件。没有匹配上的标题会使用最深的标题级别。

使用方式：

```sh
pptx2md input.pptx -t titles.txt
```

## 完整参数

- `-t [filename]`：指定标题文件。
- `-o [filename]`：指定输出文件路径。
- `-i [path]`：指定图片提取目录。
- `--image-width [width]`：设置图片最大宽度，单位为 px。设置后会使用 HTML `img` 标签输出图片。
- `--disable-image`：禁用图片提取。
- `--disable-escaping`：不转义特殊字符。
- `--disable-notes`：不输出演示者备注。
- `--disable-wmf`：保留 WMF 图片，不尝试转换，适用于 Linux 下避免转换异常的场景。
- `--disable-color`：禁用 HTML 颜色标签。
- `--enable-slides`：在幻灯片之间加入 `\n---\n` 分隔符，适合将 PPTX 转成 Markdown 幻灯片。
- `--try-multi-column`：尝试检测多栏布局，速度较慢。
- `--min-block-size [size]`：设置文本块被输出所需的最小字符数。
- `--wiki` / `--mdk`：输出为 TiddlyWiki 或 Madoko 格式。
- `--qmd`：输出为 [Quarto reveal.js](https://quarto.org/docs/presentations/revealjs/) 演示文稿格式。
- `--page [number]`：只转换指定页码。
- `--keep-similar-titles`：保留相似标题，并为重复标题添加 `(cont.)` 后缀。

如需提高 WMF 图片转换成功率，可以安装 [wand](https://docs.wand-py.org/en/0.6.12/)。

## 截图

```text
Data Link Layer Design Issues
  Services Provided to the Network Layer
  Framing
  Error Control & Flow Control
Error Detection and Correction
  Error Correcting Code (ECC)
  Error Detecting Code
Elementary Data Link Protocols
Sliding Window Protocols
  One-Bit Sliding Window Protocol
  Protocol Using Go Back N
  Using Selective Repeat
Performance of Sliding Window Protocols
Example Data Link Protocols
  PPP
```

<img src="https://raw.githubusercontent.com/ssine/image_bed/master/pic1.png" height=550 >

- **上方**：标题列表文件内容。
- **下方**：生成的目录。

![2](https://raw.githubusercontent.com/ssine/image_bed/master/pic2.png)

- **左侧**：源 PPTX 文件。
- **右侧**：生成的 Markdown 文件（由 Madoko 渲染）。

## API 用法

也可以在 Python 代码中以编程方式使用 pptx2md：

```python
from pathlib import Path

from pptx2md import ConversionConfig, convert

convert(
    ConversionConfig(
        pptx_path=Path("presentation.pptx"),
        output_path=Path("output.md"),
        image_dir=Path("img"),
        disable_notes=True,
    )
)
```

`ConversionConfig` 接受与命令行参数对应的配置：

- `pptx_path`：输入 PPTX 文件路径，必填。
- `output_path`：输出 Markdown 文件路径，必填。
- `image_dir`：提取图片的保存目录，必填。
- `title_path`：自定义标题文件路径。
- `image_width`：图片最大宽度，单位为 px。
- `disable_image`：跳过图片提取。
- `disable_escaping`：跳过特殊字符转义。
- `disable_notes`：跳过演示者备注。
- `disable_wmf`：跳过 WMF 图片转换。
- `disable_color`：跳过 HTML 颜色标签。
- `enable_slides`：添加幻灯片分隔符。
- `try_multi_column`：尝试检测多栏布局。
- `min_block_size`：最小文本块大小。
- `wiki`：输出为 TiddlyWiki 格式。
- `mdk`：输出为 Madoko 格式。
- `qmd`：输出为 Quarto 格式。
- `page`：只转换指定页码。
- `keep_similar_titles`：保留相似标题，并添加 `(cont.)` 后缀。

## 解析规则

### 文本与布局

- 文本块通过两种方式识别：
  - 幻灯片中标记为 `body` 的占位符段落。
  - 字符数超过最小文本块大小的文本形状。
- 如果同一个文本块中的段落存在不同缩进级别，会生成列表。
- 单层级段落会输出为普通文本块。
- 可以使用 `--try-multi-column` 检测多栏布局。
- 分组形状会被递归展开后再处理。
- 形状按「从上到下、从左到右」的顺序处理。

### 标题处理

- 使用自定义标题时，会通过模糊匹配将幻灯片标题匹配到标题列表。
- 匹配分数需要大于 92 才会被接受。
- 未匹配的标题默认使用最深标题级别。
- 默认会省略相似标题（匹配分数大于 92）。如果需要保留，请使用 `--keep-similar-titles`。

### 格式与样式

- 文本格式会转换为 Markdown 语法：
  - PPT 中的加粗文本会转换为 `**bold**`。
  - 斜体文本会转换为 `_italic_`。
  - 超链接会保留为 `[text](url)`。
- 颜色处理：
  - 标记为 `Accent 1-6` 的主题色会被保留。
  - RGB 颜色会转换为 HTML 颜色代码。
  - 深色主题色会转换为加粗文本。
  - 可以使用 `--disable-color` 禁用颜色标签。

### 特殊元素

- 图片：
  - 会提取到指定图片目录。
  - WMF 图片会在可能的情况下转换为 PNG。
  - 可以通过 `--image-width` 限制图片宽度。
  - 设置宽度后会使用 HTML `img` 标签输出。
- 表格：
  - 支持合并单元格。
  - 单元格中的复杂格式会被保留。
- 默认会转义特殊字符，可以通过 `--disable-escaping` 禁用。
- 默认会包含演示者备注，可以通过 `--disable-notes` 禁用。
