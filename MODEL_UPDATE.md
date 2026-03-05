# 🔧 模型更新说明

## 问题描述

遇到以下错误：
- `404 models/gemini-1.5-pro is not found for API version v1beta`
- `404 models/veo-2.0-generate-002 is not found for API version v1beta`
- `404 models/veo-2.0-generate-001 is not found for API version v1beta`
- `404 models/imagen-3.0-generate-002 is not found for API version v1beta`

## 原因分析

1. **API 已全面更新**：Google Gemini API 已升级，旧模型名称全部不再支持
   - 对话模型：`gemini-1.5-pro` → `gemini-2.5-flash`
   - 图像模型：`imagen-3.0-generate-002` → `gemini-2.5-flash-image`
   - **视频模型**：⚠️ **所有 Veo 模型已不再支持 `generateContent` 方法**
2. **视频生成 API 重大变更**：
   - Veo 2.0/3.0/3.1 所有版本改用异步 API
   - 需要使用新的 `google.genai` SDK（替代 `google.generativeai`）
   - 使用 `client.models.generate_videos()` 和 `client.operations.get()` 进行异步操作
3. **SDK 更新**：
   - `google.generativeai` 包已停止维护
   - 视频生成必须使用 `google.genai` 新包

## 解决方案

### ✅ 已修复

**1. 对话模型更新**：

```python
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",  # 新模型
    generation_config=generation_config,
    safety_settings=safety_settings,
)
```

**2. 视频模型更新**（已重写）：

```python
# ✅ 使用新的 google.genai SDK
from google import genai
from google.genai import types
import time

client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# 发起视频生成请求
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="A beautiful sunset over the ocean",
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
        resolution="720p",
    ),
)

# 轮询操作状态
while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)

# 下载视频
video = operation.response.generated_videos[0]
client.files.download(file=video.video)
video.video.save("output.mp4")
```

**视频生成功能状态**：
- ✅ 已重写：所有视频生成函数已使用新 API
- ✅ 支持功能：
  - 文生视频（8秒，支持音频）
  - 图生视频
  - 多图参考生成
  - 视频扩展（每次7秒，最多20次）
  - 多轮迭代生成
- 模型：`veo-3.1-generate-preview`

**3. 图像模型更新**：

```python
# 旧模型（Imagen 3.0）已不再支持 generateContent
# image_model = genai.GenerativeModel("imagen-3.0-generate-002")

# 新模型：使用 Gemini 2.5 Flash Image
image_model = genai.GenerativeModel("gemini-2.5-flash-image")
```

> 💡 **注意**：Imagen 4.0 (`imagen-4.0-*`) 仅支持 `predict` 方法，不支持 `generateContent`。
> 为保持代码兼容性，改用 `gemini-2.5-flash-image`，它同时支持文本和图像生成。

### 📋 当前可用模型（2026-03）

**对话模型**：

| 模型名称 | 特点 | 使用场景 |
|---------|------|---------|
| `gemini-2.5-flash` | 🚀 速度快、免费额度高 | **日常对话、快速响应**（推荐） |
| `gemini-2.5-pro` | 💪 功能强大、精度高 | 复杂任务、高质量输出 |
| `gemini-2.0-flash` | ⚡ 超快速响应 | 简单查询、实时交互 |
| `gemini-pro-latest` | 🎯 自动使用最新版本 | 保持最新功能 |

**生成模型**：

| 模型名称 | 类型 | 状态 |
|---------|------|------|
| `imagen-3.0-generate-002` | 图像生成 | ✅ 正常 |
| `veo-2.0-generate-001` | 视频生成 | ✅ 已更新 |

### 🔄 如何切换模型

在 `gemini_tool.py` 的 `initialize_gemini()` 函数中修改 `model_name`：

```python
# 方式1: 使用 Flash（推荐，速度快）
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

# 方式2: 使用 Pro（功能强，消耗额度快）
model = genai.GenerativeModel(model_name="gemini-2.5-pro")

# 方式3: 自动使用最新版本
model = genai.GenerativeModel(model_name="gemini-pro-latest")
```

## 📊 免费额度说明

### Gemini 2.5 Flash（推荐）
- ✅ 每分钟请求数：较高
- ✅ 每日请求数：较高
- ✅ 响应速度：非常快

### Gemini 2.5 Pro
- ⚠️ 每分钟请求数：有限
- ⚠️ 每日请求数：有限
- ✅ 响应质量：更高

## ⚠️ 配额限制错误

如果遇到 `429 Quota exceeded` 错误：

```
429 You exceeded your current quota
```

**解决方法**：
1. 等待 15-60 秒后重试
2. 切换到 `gemini-2.5-flash` 模型
3. 查看使用情况：https://ai.dev/rate-limit
4. 考虑升级到付费计划：https://ai.google.dev/pricing

## 🔮 未来计划

**建议迁移到新 SDK**：

```bash
# 当前使用（已废弃）
pip install google-generativeai

# 推荐迁移到（未来）
pip install google-genai
```

迁移工作将在后续版本中完成。

## 📝 更新日志

### 2026-03-05 (v4) 🔴
- ❌ 禁用视频生成功能
- ⚠️  Veo API 已完全改变，不再支持 generateContent
- 📝 更新所有视频生成函数，添加已禁用提示
- 💡 提供新 API 使用说明

### 2026-03-05 (v3) ✨
- ✅ 修复图像模型 404 错误
- ✅ 更新为 `gemini-2.5-flash-image`
- ✅ 添加模型检查工具 `check_models.py`
- ✅ 完成所有模型迁移验证

### 2026-03-05 (v2)
- ✅ 修复视频模型 404 错误
- ✅ 更新为 `veo-2.0-generate-001`
- ✅ 更新文档说明

### 2026-03-05 (v1)
- ✅ 修复对话模型 404 错误
- ✅ 更新为 `gemini-2.5-flash`
- ✅ 添加模型说明文档
- ✅ 优化免费额度使用

---

**当前可用功能** ✅  
**当前使用模型**：
- 对话：`gemini-2.5-flash` ✅
- 图像：`gemini-2.5-flash-image` ✅
- 视频：❌ 已禁用（API 已变更）

**状态**：
- ✅ 对话功能正常
- ✅ 图像生成正常
- ❌ 视频生成已禁用（等待新 API 实现）
