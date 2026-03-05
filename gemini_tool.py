#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini API 工具集 - 主入口
=========================

模块化架构：
- chat_mode: 对话模式（单轮、多轮、多模态、超长上下文）
- generation_mode: 生成模式（文生图、图文生图、文生视频、图生视频）
- multi_turn_mode: 多轮生成模式（持续优化图片/视频）

作者：Gemini Tool
版本：1.3.0
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

# 导入各模块
from chat_mode import (
    chat_with_text,
    multi_turn_chat,
    multi_turn_chat_programmatic,
    chat_with_image,
    chat_with_long_context,
    count_tokens,
    load_long_text,
    load_image
)

from generation_mode import (
    generate_image,
    generate_image_from_image,
    generate_video,
    generate_image_to_video,
    generate_image_with_video
)

from multi_turn_mode import (
    multi_turn_image_generation,
    multi_turn_video_generation
)


# ============================================================================
# 初始化配置
# ============================================================================

def initialize_gemini():
    """
    初始化 Gemini API 配置
    
    返回:
        配置好的 Gemini 模型实例
    """
    # 加载环境变量（API Key 存储在 .env 文件中）
    load_dotenv()

    # 从环境变量获取 API Key 并配置
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("未找到 GOOGLE_API_KEY，请在 .env 文件中配置")
    
    genai.configure(api_key=api_key)

    # 生成参数配置
    generation_config = {
        "temperature": 0.7,           # 创造性控制：0-1，越高越有创意，越低越精确
        "top_p": 0.95,                # 核采样：控制输出多样性
        "top_k": 64,                  # 限制每步考虑的词数
        "max_output_tokens": 64000,   # 最大输出token数
        "response_mime_type": "text/plain",  # 输出格式
    }

    # 安全过滤设置（使用中等强度过滤）
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    # 创建对话模型
    # 使用 Gemini 2.5 Flash - 速度快、免费额度高
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config=generation_config,
        safety_settings=safety_settings,
        system_instruction="你是资深编程导师，解决复杂算法问题时步骤清晰、逻辑严谨。"
    )

    return model


# ============================================================================
# 主程序入口
# ============================================================================

if __name__ == "__main__":
    # 初始化 Gemini
    model = initialize_gemini()

    print("=" * 60)
    print("Gemini API 工具集 v1.3.0")
    print("=" * 60)
    print("\n支持的功能模块：")
    print("1. 对话模式 (chat_mode)")
    print("   - 单轮对话、多轮对话、多模态对话、超长上下文")
    print("\n2. 生成模式 (generation_mode)")
    print("   - 文生图、图文生图、文生视频、图生视频")
    print("\n3. 多轮生成模式 (multi_turn_mode)")
    print("   - 多轮图片生成、多轮视频生成（迭代优化）")
    print("=" * 60)

    # ============ 示例用法 ============
    # 根据需要取消注释以下调用

    # ============ 对话模式 ============
    # 1. 单轮对话
    # chat_with_text(model, "用Python实现快速排序")

    # 2. 多轮对话（交互式）
    # multi_turn_chat(model)

    # 3. 多轮对话（编程式）
    # messages = ["你好", "介绍一下Python", "它有什么优点"]
    # multi_turn_chat_programmatic(model, messages)

    # 4. 多模态对话
    # chat_with_image(model, "描述这张图片", ["demo.jpg"])

    # 5. 超长上下文
    # chat_with_long_context(model, "总结这个文件", file_path="gemini.py")

    # ============ 生成模式 ============
    # 单次生成
    # generate_image("一只可爱的小猫在草地上玩耍")
    # generate_image_from_image("把这幅画变成水彩画风格", "reference.jpg")
    # generate_video("一只狗在海滩上奔跑")
    # generate_image_to_video("input.jpg", "让画面动起来")
    # generate_image_with_video("让场景更具动感", image_paths=["image.jpg"])

    # ============ 多轮生成模式 ============
    # 多轮图片生成（持续迭代优化）
    # multi_turn_image_generation()

    # 多轮视频生成（持续迭代优化）
    multi_turn_video_generation()
    
    # 验证模块加载成功
    print("\n✓ 所有模块加载成功！")
    print("\n取消注释相应代码即可使用对应功能。")
