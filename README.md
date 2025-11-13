# EPUB Translator

一个基于 Python 的 EPUB 电子书翻译工具，使用 LLM (大语言模型) 进行翻译，并提供图形用户界面。

A Python-based EPUB e-book translator that uses LLM (Large Language Models) for translation with a graphical user interface.

## 功能特点 (Features)

- 📚 解析和翻译 EPUB 电子书 (Parse and translate EPUB e-books)
- 🤖 使用 OpenAI 兼容的 API 进行翻译 (Use OpenAI-compatible APIs for translation)
- 🔧 支持多种模型选择 (Support multiple model selection: GPT-3.5, GPT-4, GPT-4o, etc.)
- ✍️ 自定义翻译提示词 (Customize translation prompts for better results)
- 🎨 保留原始格式和图片 (Preserve original formatting and images)
- 🌍 支持多种语言互译 (Support multiple language translations)
- 📝 根据目标语言自动调整文本方向和字体 (Automatically adjust text direction and fonts for target language)
- 💻 友好的图形用户界面 (User-friendly GUI)
- 🏗️ 模块化代码结构，易于维护和扩展 (Modular code structure for easy maintenance and extension)

## 安装 (Installation)

### 前置要求 (Prerequisites)

- Python 3.8 或更高版本 (Python 3.8 or higher)
- pip 包管理器 (pip package manager)

### 安装步骤 (Installation Steps)

1. 克隆仓库 (Clone the repository):
```bash
git clone https://github.com/KimmyXYC/EPUB-Translator.git
cd EPUB-Translator
```

2. 安装依赖 (Install dependencies):
```bash
pip install -r requirements.txt
```

## 使用方法 (Usage)

### 启动应用 (Start the Application)

```bash
python epub_translator.py
```

### 使用步骤 (Steps to Use)

1. **配置 API**:
   - 输入你的 OpenAI API 密钥或兼容 API 的密钥
   - (可选) 修改 API Base URL 如果使用其他兼容的服务
   - 选择要使用的模型 (Model): 如 gpt-3.5-turbo, gpt-4, gpt-4o-mini 等

2. **自定义提示词 (可选)**:
   - 在"Translation Prompt"区域可以自定义翻译提示词
   - 使用 `{target_language}` 作为目标语言的占位符
   - 默认提示词已针对一般翻译优化

3. **选择语言**:
   - 源语言: 选择原文语言 (auto 为自动检测)
   - 目标语言: 选择要翻译成的语言

4. **选择文件**:
   - 点击 "Browse..." 选择输入的 EPUB 文件
   - 选择输出文件的保存位置

5. **开始翻译**:
   - 点击 "Translate" 按钮开始翻译
   - 进度条将显示翻译进度
   - 翻译完成后会显示成功消息

## 支持的语言 (Supported Languages)

- 中文 (Chinese) - zh
- 英文 (English) - en
- 日文 (Japanese) - ja
- 韩文 (Korean) - ko
- 西班牙文 (Spanish) - es
- 法文 (French) - fr
- 德文 (German) - de
- 俄文 (Russian) - ru
- 阿拉伯文 (Arabic) - ar

## 特殊功能 (Special Features)

### 文本方向调整 (Text Direction Adjustment)

对于从左到右 (LTR) 和从右到左 (RTL) 的语言，程序会自动调整文本方向：
- 阿拉伯语、希伯来语等 RTL 语言会自动设置为从右到左
- 其他语言默认从左到右

For left-to-right (LTR) and right-to-left (RTL) languages, the program automatically adjusts text direction:
- Arabic, Hebrew, etc. RTL languages are automatically set to right-to-left
- Other languages default to left-to-right

### 字体配置 (Font Configuration)

根据目标语言自动选择合适的字体系列：
- 中文: 'Noto Sans SC', 'Microsoft YaHei', SimSun
- 日文: 'Noto Sans JP', 'Yu Gothic', 'MS Gothic'
- 韩文: 'Noto Sans KR', 'Malgun Gothic'
- 阿拉伯文: 'Noto Sans Arabic', 'Arial'
- 其他: 'Noto Sans', Arial

Automatically selects appropriate font families based on target language:
- Chinese: 'Noto Sans SC', 'Microsoft YaHei', SimSun
- Japanese: 'Noto Sans JP', 'Yu Gothic', 'MS Gothic'
- Korean: 'Noto Sans KR', 'Malgun Gothic'
- Arabic: 'Noto Sans Arabic', 'Arial'
- Others: 'Noto Sans', Arial

## API 兼容性 (API Compatibility)

本工具使用 OpenAI 的 API 格式，也兼容其他使用相同格式的 API 服务，如：
- OpenAI GPT-3.5/GPT-4
- Azure OpenAI
- 本地部署的兼容 API (如 LocalAI, FastChat 等)

This tool uses OpenAI's API format and is compatible with other API services using the same format, such as:
- OpenAI GPT-3.5/GPT-4
- Azure OpenAI
- Locally deployed compatible APIs (e.g., LocalAI, FastChat, etc.)

## 技术栈 (Tech Stack)

- **Python 3.8+**: 主要编程语言 (Main programming language)
- **tkinter**: GUI 框架 (GUI framework)
- **ebooklib**: EPUB 文件处理 (EPUB file processing)
- **BeautifulSoup4**: HTML 解析 (HTML parsing)
- **OpenAI**: LLM API 客户端 (LLM API client)
- **lxml**: XML 处理 (XML processing)

## 编程使用 (Programmatic Usage)

除了 GUI，你也可以在代码中使用 EPUB Translator：

```python
from src.epub_translator import EPUBTranslator

# 基础使用 (Basic usage)
translator = EPUBTranslator(
    api_key="your-api-key",
    api_base="https://api.openai.com/v1"
)
translator.source_lang = "en"
translator.target_lang = "zh"
translator.translate_epub("input.epub", "output.epub")

# 使用特定模型 (Using specific model)
translator = EPUBTranslator(
    api_key="your-api-key",
    model="gpt-4o-mini"  # 选择模型
)

# 使用自定义提示词 (Using custom prompt)
custom_prompt = """You are an expert literary translator.
Translate to {target_language} with attention to style and tone.
Only return the translation."""

translator = EPUBTranslator(
    api_key="your-api-key",
    model="gpt-4",
    custom_prompt=custom_prompt
)
```

更多示例请参考 `example_usage.py` 文件。

See `example_usage.py` for more examples.

## 项目结构 (Project Structure)

```
EPUB-Translator/
├── src/epub_translator/      # 主包 (Main package)
│   ├── __init__.py           # 包初始化 (Package initialization)
│   ├── translator.py         # 核心翻译逻辑 (Core translation logic)
│   ├── gui.py                # GUI 界面 (GUI interface)
│   ├── config.py             # 配置和常量 (Configuration and constants)
│   └── prompts.py            # 提示词模板 (Prompt templates)
├── epub_translator.py        # 主入口文件 (Main entry point - backwards compatibility)
├── example_usage.py          # 使用示例 (Usage examples)
├── test_translator.py        # 测试文件 (Test file)
├── requirements.txt          # 依赖列表 (Dependencies list)
├── README.md                 # 项目说明 (Project documentation)
└── LICENSE                   # 许可证 (License)
```

## 注意事项 (Notes)

- 翻译质量取决于所使用的 LLM 模型
- 翻译长篇文档可能需要较长时间和较多 API 调用
- 请确保有足够的 API 额度
- 建议在翻译前备份原始文件

- Translation quality depends on the LLM model used
- Translating long documents may take considerable time and API calls
- Ensure you have sufficient API quota
- It's recommended to backup original files before translation

## 许可证 (License)

MIT License - 详见 LICENSE 文件 (See LICENSE file for details)

## 贡献 (Contributing)

欢迎提交 Issue 和 Pull Request！

Issues and Pull Requests are welcome!

## 作者 (Author)

KimmyXYC

## 致谢 (Acknowledgments)

感谢所有开源库的贡献者！

Thanks to all contributors of the open-source libraries!
