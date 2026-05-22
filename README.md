# PDF Converter

基于 [marker](https://github.com/datalab-to/marker) 的 PDF 转 Markdown/TXT 工具，保留标题、表格、列表、图片。

## 安装

### 1. 前提

需要有 Python 3.10+：

```bash
# 检查是否已安装
python --version
```

如果没有，通过 Microsoft Store 或 [python.org](https://www.python.org/downloads/) 安装，或命令行：

```bash
winget install Python.Python.3.12
```

### 2. 安装依赖

把整个 `converter` 文件夹放到你想放的位置，然后在该目录下：

```bash
pip install -r requirements.txt
pip install -e .
```

或者直接双击 `setup.bat` 一键安装。

首次使用时 marker 会自动下载模型（约 3-5GB）到 `~/.cache/datalab/`，仅此一次。

## 使用

### 基本转换

```bash
# PDF → Markdown（默认）
converter report.pdf

# 指定输出
converter report.pdf -o result.md
```

### 批量转换

```bash
# 整个目录
converter ./pdfs/

# 通配符
converter "./docs/*.pdf"

# 指定输出目录
converter ./pdfs/ -o ./output/
```

### 输出格式

```bash
# Markdown（默认）
converter report.pdf -f md

# 纯文本
converter report.pdf -f txt
```

### 图片处理

```bash
# 默认：提取到 images/ 文件夹，markdown 中相对路径引用
converter report.pdf

# 不提取图片
converter report.pdf --no-images

# Base64 内嵌（单文件方便分发）
converter report.pdf --embed-images
```

### 扫描件 PDF

```bash
converter scanned.pdf --ocr
```

## 输出结构

转换后会生成：

```
output/报告/
├── 报告.md         # Markdown 文件
└── images/         # 提取的图片
    ├── img_001.png
    └── img_002.jpg
```

用 Typora、VS Code、Obsidian 等打开 `.md` 文件即可查看。

## 换电脑

把整个 `converter` 文件夹拷到新电脑，然后重复"安装"步骤即可。

## 故障排查

**`converter` 命令找不到：**

设置 → 应用 → 高级应用设置 → 应用执行别名 → 关闭 `python.exe` / `python3.exe`。关掉终端重开。

或直接用项目里的 `converter.bat` 替代：

```bash
converter.bat report.pdf
```
