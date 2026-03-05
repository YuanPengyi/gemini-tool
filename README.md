# Gemini API 工具集

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.3.0-orange)](https://github.com/yourusername/gemini-tool)

一个功能强大、模块化的 Google Gemini API 工具集，支持对话、图像生成、视频生成等多种 AI 能力。

## ✨ 主要功能

### 📝 对话模式 (`chat_mode.py`)
- **单轮对话**：快速问答
- **多轮对话**：保持上下文的连续对话
- **多模态对话**：支持文本 + 图片输入
- **超长上下文**：支持 100 万 Token 的超长文档分析

### 🎨 生成模式 (`generation_mode.py`)
- **文生图**：根据文本描述生成图片
- **图文生图**：基于参考图片进行风格转换和编辑
- **文生视频**：根据文本描述生成视频
- **图生视频**：将静态图片转换为动态视频
- **图文生视频**：结合图片和文本生成视频

### 🔄 多轮生成模式 (`multi_turn_mode.py`)
- **多轮图片生成**：持续迭代优化图片效果
- **多轮视频生成**：持续迭代优化视频效果
- **版本管理**：自动保存所有生成版本
- **历史记录**：查看完整的生成历史

## 📦 安装

### 1. 克隆项目

```bash
git clone https://github.com/YuanPengyi/gemini-tool.git
cd gemini-tool
```

### 2. 安装依赖

```bash
pip install google-generativeai python-dotenv
```

### 3. 配置 API Key

在项目根目录创建 `.env` 文件：

```bash
GOOGLE_API_KEY=你的_Gemini_API_Key
```

> 💡 获取 API Key：访问 [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🚀 快速开始

### 基础使用

```python
from gemini_tool import initialize_gemini
from chat_mode import chat_with_text, multi_turn_chat
from generation_mode import generate_image

# 初始化模型
model = initialize_gemini()

# 单轮对话
chat_with_text(model, "用Python实现快速排序")

# 多轮交互式对话
multi_turn_chat(model)

# 生成图片
generate_image("一只可爱的小猫在草地上玩耍", "cat.png")
```

### 运行主程序

```bash
python3 gemini_tool.py
```

## 📖 详细使用指南

### 对话模式

#### 单轮对话

```python
from chat_mode import chat_with_text

chat_with_text(model, "解释一下量子计算的原理")
```

#### 多轮对话（交互式）

```python
from chat_mode import multi_turn_chat

multi_turn_chat(model)
```

**支持命令**：
- `exit/quit/bye` - 退出对话
- `clear` - 清空历史记录
- `history` - 查看对话历史
- `tokens` - 查看 Token 使用情况

#### 多轮对话（编程式）

```python
from chat_mode import multi_turn_chat_programmatic

messages = [
    "你好",
    "介绍一下 Python",
    "它有什么优点"
]
responses = multi_turn_chat_programmatic(model, messages)
```

#### 多模态对话

```python
from chat_mode import chat_with_image

chat_with_image(model, "描述这张图片的内容", ["image1.jpg", "image2.jpg"])
```

#### 超长上下文对话

```python
from chat_mode import chat_with_long_context

# 分析整个代码文件
chat_with_long_context(model, "总结这个文件的主要功能", file_path="large_file.py")

# 分析 PDF 文档
chat_with_long_context(model, "提取关键信息", file_path="document.pdf")
```

### 生成模式

#### 文生图

```python
from generation_mode import generate_image

generate_image(
    prompt="一只可爱的橘猫在樱花树下玩耍，阳光明媚，日本动漫风格",
    output_path="cat_sakura.png"
)
```

#### 图文生图

```python
from generation_mode import generate_image_from_image

generate_image_from_image(
    prompt="把这幅画变成水彩画风格，色彩柔和",
    reference_image_path="original.jpg",
    output_path="watercolor.png"
)
```

#### 文生视频

```python
from generation_mode import generate_video

generate_video(
    prompt="一只金毛犬在海滩上快乐地奔跑，夕阳余晖，慢镜头",
    output_path="dog_beach.mp4"
)
```

#### 图生视频

```python
from generation_mode import generate_image_to_video

generate_image_to_video(
    image_path="landscape.jpg",
    prompt="让画面动起来，云朵飘动，树叶摇曳"
)
```

### 多轮生成模式

#### 多轮图片生成

```python
from multi_turn_mode import multi_turn_image_generation

multi_turn_image_generation()
```

**交互式命令**：
- 输入描述词 - 生成新图片或优化当前图片
- `show` - 显示当前图片路径
- `history` - 查看生成历史
- `save <名称>` - 保存当前版本为指定名称
- `exit` - 退出

**使用示例**：
```
描述/调整: 一只可爱的小猫
[版本 1] 已生成: generated_v1.png

描述/调整: 让猫咪的眼睛更大更明亮
[版本 2] 已生成: generated_v2.png

描述/调整: 添加樱花背景
[版本 3] 已生成: generated_v3.png

描述/调整: save final_cat
✓ 已保存到: final_cat.png
```

#### 多轮视频生成

```python
from multi_turn_mode import multi_turn_video_generation

multi_turn_video_generation()
```

**交互式命令**：
- 输入描述词 - 生成视频
- `image <路径>` - 从图片开始生成视频
- `history` - 查看生成历史
- `exit` - 退出

## 🏗️ 项目结构

```
gemini-tool/
├── gemini_tool.py          # 主入口文件
├── chat_mode.py            # 对话模式模块
├── generation_mode.py      # 生成模式模块
├── multi_turn_mode.py      # 多轮生成模式模块
├── gemini.py               # 原始单文件版本（保留）
├── .env                    # API Key 配置文件
├── README.md               # 项目说明文档
└── requirements.txt        # 依赖列表
```

## 🔧 配置说明

### 生成参数配置

在 `gemini_tool.py` 的 `initialize_gemini()` 函数中可以调整生成参数：

```python
generation_config = {
    "temperature": 0.7,        # 创造性 (0-1)：越高越有创意
    "top_p": 0.95,             # 核采样：控制输出多样性
    "top_k": 64,               # 限制每步考虑的词数
    "max_output_tokens": 64000 # 最大输出 token 数
}
```

### 安全过滤设置

```python
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    # ...
]
```

可选阈值：
- `BLOCK_NONE` - 不过滤
- `BLOCK_ONLY_HIGH` - 仅阻止高风险
- `BLOCK_MEDIUM_AND_ABOVE` - 阻止中高风险
- `BLOCK_LOW_AND_ABOVE` - 阻止低中高风险

## 🤖 支持的模型

- **对话模型**：`gemini-1.5-pro` (支持 100 万 Token)
- **图像生成**：`imagen-3.0-generate-002`
- **视频生成**：`veo-2.0-generate-002`

## 📊 Token 使用统计

使用 `count_tokens()` 函数查看 Token 消耗：

```python
from chat_mode import count_tokens

# 计算文本 Token
token_count = count_tokens(model, "你的文本内容")

# 计算文件 Token
token_count = count_tokens(model, "large_file.txt")
```

## 🔍 常见问题

### Q: 如何获取 API Key？

A: 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)，登录后即可生成免费的 API Key。

### Q: 生成的视频 URI 如何下载？

A: 视频生成返回的是 Google Cloud Storage URI，需要使用 Google Cloud SDK 或通过 API 下载。

### Q: 多轮对话如何清空历史？

A: 在交互模式下输入 `clear` 命令即可清空历史记录。

### Q: 图片生成失败怎么办？

A: 检查：
1. API Key 是否正确配置
2. 提示词是否符合内容政策
3. 网络连接是否正常

### Q: 看到 FutureWarning 警告

A: `google.generativeai` 包已停止维护，建议迁移到新的 `google.genai` 包，但不影响当前功能使用。

## 🛠️ 依赖项

```txt
google-generativeai>=0.3.0
python-dotenv>=1.0.0
```

创建 `requirements.txt`：

```bash
echo "google-generativeai>=0.3.0" > requirements.txt
echo "python-dotenv>=1.0.0" >> requirements.txt
```

安装：

```bash
pip install -r requirements.txt
```

## 📝 更新日志

### v1.3.0 (2026-03-05)
- ✨ 重构为模块化架构
- 📦 拆分为独立的功能模块
- 🎯 优化代码组织结构
- 📖 添加完整文档

### v1.2.0
- ✨ 新增多轮图片生成
- ✨ 新增多轮视频生成
- 🔄 支持迭代优化

### v1.1.0
- ✨ 新增多轮对话功能
- 📊 添加 Token 统计
- 💾 支持历史记录管理

### v1.0.2
- 🐛 修复类型注解警告
- 📝 添加完整类型提示
- ♻️ 代码优化

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 致谢

- [Google Gemini API](https://ai.google.dev/)
- [Imagen 3.0](https://deepmind.google/technologies/imagen-3/)
- [Veo 2.0](https://deepmind.google/technologies/veo/veo-2/)

---

**⚡ 快速开始**：`python3 gemini_tool.py`

**📚 文档**：查看各模块文件中的详细注释

**🌟 如果这个项目对你有帮助，请给个 Star！**
