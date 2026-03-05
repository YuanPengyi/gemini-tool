# 🚀 Gemini API 工具集

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.3.0-orange)](https://github.com/YuanPengyi/gemini-tool)
[![GitHub Stars](https://img.shields.io/github/stars/YuanPengyi/gemini-tool?style=social)](https://github.com/YuanPengyi/gemini-tool)

> 一个功能强大、模块化的 Google Gemini API 工具集，支持对话、图像生成、视频生成等多种 AI 能力。

## 🎯 核心特性

- 🧠 **智能对话**：支持单轮、多轮、多模态对话，100万Token超长上下文
- 🎨 **AI 绘画**：文生图、图文生图，多轮迭代优化
- 🎬 **视频创作**：文生视频、图生视频、图文生视频
- 🔄 **持续优化**：交互式多轮生成，版本管理，历史追溯
- 📦 **模块化设计**：清晰的代码结构，易于扩展和维护
- 🛡️ **安全可靠**：环境变量管理，敏感信息保护

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

## 📦 快速安装

### 方式一：使用 pip 安装依赖

```bash
# 克隆项目
git clone https://github.com/YuanPengyi/gemini-tool.git
cd gemini-tool

# 安装依赖
pip install -r requirements.txt
```

### 方式二：手动安装

```bash
pip install google-generativeai python-dotenv
```

### 配置 API Key

1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey) 获取免费 API Key
2. 在项目根目录创建 `.env` 文件：

```env
GOOGLE_API_KEY=你的API密钥
```

> ⚠️ **注意**：请勿将 `.env` 文件提交到 Git 仓库！`.gitignore` 已自动配置。

## 🚀 快速开始

### 5 分钟上手

```python
# 1. 导入模块
from gemini_tool import initialize_gemini
from chat_mode import chat_with_text, multi_turn_chat
from generation_mode import generate_image

# 2. 初始化模型
model = initialize_gemini()

# 3. 开始对话
chat_with_text(model, "用Python实现快速排序")

# 4. 生成图片
generate_image("一只可爱的小猫在草地上玩耍", "cat.png")
```

### 或者直接运行主程序

```bash
python3 gemini_tool.py
```

## 📚 功能模块详解

## 📚 功能模块详解

### 💬 对话模式 (`chat_mode.py`)

<details>
<summary><b>📝 单轮对话</b> - 快速问答</summary>

```python
from chat_mode import chat_with_text

chat_with_text(model, "解释一下量子计算的原理")
```
</details>

<details>
<summary><b>🔄 多轮对话（交互式）</b> - 保持上下文的连续对话</summary>

```python
from chat_mode import multi_turn_chat

multi_turn_chat(model)
```

**支持的命令**：
| 命令 | 功能 |
|------|------|
| `exit/quit/bye` | 退出对话 |
| `clear` | 清空历史记录 |
| `history` | 查看对话历史 |
| `tokens` | 查看Token使用情况 |

</details>

<details>
<summary><b>💻 多轮对话（编程式）</b> - 批量处理对话</summary>

```python
from chat_mode import multi_turn_chat_programmatic

messages = ["你好", "介绍一下Python", "它有什么优点"]
responses = multi_turn_chat_programmatic(model, messages)
```
</details>

<details>
<summary><b>🖼️ 多模态对话</b> - 支持文本 + 图片输入</summary>

```python
from chat_mode import chat_with_image

chat_with_image(model, "描述这张图片的内容", ["image1.jpg", "image2.jpg"])
```
</details>

<details>
<summary><b>📄 超长上下文对话</b> - 支持100万Token</summary>

```python
from chat_mode import chat_with_long_context

# 分析代码文件
chat_with_long_context(model, "总结这个文件的主要功能", file_path="large_file.py")

# 分析PDF文档
chat_with_long_context(model, "提取关键信息", file_path="document.pdf")
```

**适用场景**：
- 📚 分析整个代码库
- 📖 阅读长文档/PDF
- 📊 处理大型数据集

</details>

---

### 🎨 生成模式 (`generation_mode.py`)

<details>
<summary><b>✨ 文生图</b> - 根据文本描述生成图片</summary>

```python
from generation_mode import generate_image

generate_image(
    prompt="一只可爱的橘猫在樱花树下玩耍，阳光明媚，日本动漫风格",
    output_path="cat_sakura.png"
)
```
</details>

<details>
<summary><b>🎭 图文生图</b> - 基于参考图片进行风格转换</summary>

```python
from generation_mode import generate_image_from_image

generate_image_from_image(
    prompt="把这幅画变成水彩画风格，色彩柔和",
    reference_image_path="original.jpg",
    output_path="watercolor.png"
)
```

**适用场景**：
- 🎨 图片风格转换
- ✏️ 图片编辑/修改
- 🖌️ 以图生图创作

</details>

<details>
<summary><b>🎬 文生视频</b> - 根据文本描述生成视频</summary>

```python
from generation_mode import generate_video

generate_video(
    prompt="一只金毛犬在海滩上快乐地奔跑，夕阳余晖，慢镜头",
    output_path="dog_beach.mp4"
)
```
</details>

<details>
<summary><b>🎞️ 图生视频</b> - 将静态图片转换为动态视频</summary>

```python
from generation_mode import generate_image_to_video

generate_image_to_video(
    image_path="landscape.jpg",
    prompt="让画面动起来，云朵飘动，树叶摇曳"
)
```
</details>

---

### 🔄 多轮生成模式 (`multi_turn_mode.py`)

<details>
<summary><b>🎨 多轮图片生成</b> - 持续迭代优化图片</summary>

```python
from multi_turn_mode import multi_turn_image_generation

multi_turn_image_generation()
```

**交互式命令**：
| 命令 | 功能 |
|------|------|
| 输入描述词 | 生成新图片或优化当前图片 |
| `show` | 显示当前图片路径 |
| `history` | 查看生成历史 |
| `save <名称>` | 保存当前版本为指定名称 |
| `exit` | 退出 |

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

**功能特性**：
- ✅ 持续优化图片生成
- ✅ 基于上一张图片进行调整
- ✅ 自动保存所有版本历史
- ✅ 支持手动命名保存

</details>

<details>
<summary><b>🎬 多轮视频生成</b> - 持续迭代优化视频</summary>

```python
from multi_turn_mode import multi_turn_video_generation

multi_turn_video_generation()
```

**交互式命令**：
| 命令 | 功能 |
|------|------|
| 输入描述词 | 生成视频 |
| `image <路径>` | 从图片开始生成视频 |
| `history` | 查看生成历史 |
| `exit` | 退出 |

</details>

## 🏗️ 项目结构

```
gemini-tool/
├── 📄 gemini_tool.py          # 主入口文件，统一初始化和示例
├── 💬 chat_mode.py            # 对话模式模块
├── 🎨 generation_mode.py      # 生成模式模块
├── 🔄 multi_turn_mode.py      # 多轮生成模式模块
├── 📦 requirements.txt        # 依赖列表
├── 🔐 .env                    # API Key 配置（不提交到Git）
├── 🚫 .gitignore              # Git 忽略配置
└── 📖 README.md               # 项目说明文档
```

## 🤖 AI 模型说明

| 模型类型 | 模型名称 | 能力描述 |
|---------|---------|---------|
| 💬 对话 | `gemini-2.5-flash` | ⚡ 速度快、免费额度高（推荐） |
| 💬 对话 | `gemini-2.5-pro` | 💪 功能强大、高精度输出 |
| 🎨 图像 | `gemini-2.5-flash-image` | 多模态图像生成（支持 generateContent） |
| 🎬 视频 | `veo-3.1-generate-preview` | 🎥 视频生成（支持音频、扩展功能） |

> ✅ **视频生成已重新实现**：使用新的 `google.genai` SDK，支持完整的视频生成功能
> 
> 💡 **最新更新**：对话和图像生成模型已升级到最新版本
> 
> 📝 **图像模型变更**：从 `imagen-3.0` 迁移到 `gemini-2.5-flash-image`，API 更简单高效

## ⚙️ 高级配置

<details>
<summary><b>生成参数配置</b></summary>

在 `gemini_tool.py` 的 `initialize_gemini()` 函数中调整：

```python
generation_config = {
    "temperature": 0.7,        # 创造性 (0-1)：越高越有创意
    "top_p": 0.95,             # 核采样：控制输出多样性
    "top_k": 64,               # 限制每步考虑的词数
    "max_output_tokens": 64000 # 最大输出 token 数
}
```
</details>

<details>
<summary><b>安全过滤设置</b></summary>

```python
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
```

**可选阈值**：
| 阈值 | 说明 |
|------|------|
| `BLOCK_NONE` | 不过滤 |
| `BLOCK_ONLY_HIGH` | 仅阻止高风险 |
| `BLOCK_MEDIUM_AND_ABOVE` | 阻止中高风险（推荐） |
| `BLOCK_LOW_AND_ABOVE` | 阻止低中高风险 |

</details>

<details>
<summary><b>Token 使用统计</b></summary>

```python
from chat_mode import count_tokens

# 计算文本 Token
token_count = count_tokens(model, "你的文本内容")

# 计算文件 Token
token_count = count_tokens(model, "large_file.txt")
```
</details>

## ❓ 常见问题

<details>
<summary><b>如何获取 API Key？</b></summary>

1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 使用 Google 账号登录
3. 点击 "Create API Key" 生成免费密钥
4. 复制密钥并配置到 `.env` 文件

> 💡 **提示**：免费版本有一定的请求限制，查看[定价详情](https://ai.google.dev/pricing)了解更多。
</details>

<details>
<summary><b>生成的视频 URI 如何下载？</b></summary>

视频生成返回的是 Google Cloud Storage URI。下载方法：

1. **使用 Google Cloud SDK**：
```bash
gsutil cp gs://your-video-uri ./video.mp4
```

2. **通过 API 下载**：
```python
import requests
response = requests.get(video_uri)
with open("video.mp4", "wb") as f:
    f.write(response.content)
```
</details>

<details>
<summary><b>多轮对话如何清空历史？</b></summary>

在交互模式下输入 `clear` 命令：
```
你: clear
✓ 历史记录已清空
```
</details>

<details>
<summary><b>图片生成失败怎么办？</b></summary>

**检查清单**：
- ✅ API Key 是否正确配置在 `.env` 文件中
- ✅ 提示词是否符合 [内容政策](https://ai.google.dev/gemini-api/docs/safety-settings)
- ✅ 网络连接是否正常
- ✅ 是否达到 API 调用限额

**调试建议**：
```python
# 查看详细错误信息
try:
    generate_image("your prompt")
except Exception as e:
    print(f"详细错误: {e}")
```
</details>

<details>
<summary><b>看到 FutureWarning 警告怎么办？</b></summary>

这是正常提示，`google.generativeai` 包已停止维护，建议未来迁移到新的 `google.genai` 包。

**当前影响**：不影响任何功能使用

**未来计划**：后续版本将升级到新的 SDK
</details>

<details>
<summary><b>如何处理超长文本？</b></summary>

使用 `chat_with_long_context` 函数，支持高达 100 万 Token：

```python
from chat_mode import chat_with_long_context

# 自动处理大文件
chat_with_long_context(
    model, 
    "分析这个代码库的架构",
    file_path="large_codebase.py"
)
```

**支持的文件格式**：
- 📝 文本文件 (.txt, .py, .js, .java 等)
- 📄 PDF 文档 (.pdf)
- 📊 代码文件 (各种编程语言)
</details>

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

## 📝 版本历史

### v1.3.0 (2026-03-05) 🎉
- ✨ 重构为模块化架构，代码结构更清晰
- 📦 拆分为三个独立功能模块
- 🎯 优化代码组织，提升可维护性
- 📖 完善项目文档和使用指南
- 🔐 添加 .gitignore 保护敏感信息

### v1.2.0
- ✨ 新增多轮图片生成功能
- ✨ 新增多轮视频生成功能
- 🔄 支持迭代优化和版本管理
- 💾 添加历史记录追溯

### v1.1.0
- ✨ 新增多轮对话功能
- 📊 添加 Token 使用统计
- 💾 支持历史记录管理
- 🎮 添加交互式命令系统

### v1.0.2
- 🐛 修复类型注解警告
- 📝 添加完整类型提示
- ♻️ 代码优化和性能提升

## 🛠️ 技术栈

```yaml
语言: Python 3.9+
核心依赖:
  - google-generativeai: Google Gemini API 客户端
  - python-dotenv: 环境变量管理
AI 模型:
  - Gemini 1.5 Pro: 对话模型
  - Imagen 3.0: 图像生成
  - Veo 2.0: 视频生成
```

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 贡献规范
- 💡 提交清晰的 commit 信息
- 📝 为新功能添加文档
- ✅ 确保代码风格一致
- 🧪 添加必要的测试

## 📧 联系与支持

- 📮 **GitHub Issues**: [提交问题](https://github.com/YuanPengyi/gemini-tool/issues)
- 💬 **Discussions**: [参与讨论](https://github.com/YuanPengyi/gemini-tool/discussions)
- 👤 **作者**: [@YuanPengyi](https://github.com/YuanPengyi)

## 🙏 致谢

感谢以下技术和项目：

- 🤖 [Google Gemini API](https://ai.google.dev/) - 强大的多模态 AI 能力
- 🎨 [Imagen 3.0](https://deepmind.google/technologies/imagen-3/) - 先进的图像生成技术
- 🎬 [Veo 2.0](https://deepmind.google/technologies/veo/veo-2/) - 革命性的视频生成技术
- 🐍 Python 社区 - 优秀的开发生态

---

<div align="center">

**⚡ 快速开始**: `python3 gemini_tool.py`

**📚 完整文档**: 查看各模块文件中的详细注释

**🌟 喜欢这个项目？给个 Star 支持一下！**

Made with ❤️ by [YuanPengyi](https://github.com/YuanPengyi)

</div>
