# 🔧 模型更新说明

## 问题描述

遇到错误：`404 models/gemini-1.5-pro is not found for API version v1beta`

## 原因分析

1. **API 已更新**：Google Gemini API 已升级，`gemini-1.5-pro` 模型名称已不再支持
2. **SDK 警告**：`google.generativeai` 包已停止维护，建议迁移到 `google.genai`

## 解决方案

### ✅ 已修复

已将模型更新为 `gemini-2.5-flash`：

```python
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",  # 新模型
    generation_config=generation_config,
    safety_settings=safety_settings,
)
```

### 📋 当前可用模型（2026-03）

**推荐使用的模型**：

| 模型名称 | 特点 | 使用场景 |
|---------|------|---------|
| `gemini-2.5-flash` | 🚀 速度快、免费额度高 | **日常对话、快速响应**（推荐） |
| `gemini-2.5-pro` | 💪 功能强大、精度高 | 复杂任务、高质量输出 |
| `gemini-2.0-flash` | ⚡ 超快速响应 | 简单查询、实时交互 |
| `gemini-pro-latest` | 🎯 自动使用最新版本 | 保持最新功能 |

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

### 2026-03-05
- ✅ 修复模型 404 错误
- ✅ 更新为 `gemini-2.5-flash`
- ✅ 添加模型说明文档
- ✅ 优化免费额度使用

---

**问题已解决** ✅  
当前使用模型：`gemini-2.5-flash`  
状态：正常运行
