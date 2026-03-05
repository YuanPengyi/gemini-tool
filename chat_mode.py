#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对话模式模块
支持：单轮对话、多轮对话、多模态对话、超长上下文
"""

from typing import Optional, Any, Union, TYPE_CHECKING
import google.generativeai as genai
import os

if TYPE_CHECKING:
    from google.generativeai.types import GenerativeModel


# ============================================================================
# 工具函数
# ============================================================================

def count_tokens(model: 'GenerativeModel', text_or_file: Union[str, Any]) -> Union[int, str]:
    """
    计算文本或文件的Token数量

    参数:
        model: Gemini 模型实例
        text_or_file: 字符串文本或文件路径

    返回:
        Token数量或错误信息
    """
    try:
        # 如果是文件路径，先上传再计算
        if isinstance(text_or_file, str) and os.path.exists(text_or_file):
            uploaded = genai.upload_file(path=text_or_file)
            return model.count_tokens(uploaded)
        # 直接计算文本token
        return model.count_tokens(text_or_file)
    except Exception as e:
        return f"计算Token出错: {e}"


def load_long_text(model: 'GenerativeModel', file_path: str, chunk_size: int = 500000) -> Union[str, Any]:
    """
    加载超长文本/文档（自动处理）

    支持格式：
    - PDF文件：直接上传
    - 文本文件：读取内容

    参数:
        model: Gemini 模型实例
        file_path: 文件路径
        chunk_size: 分块大小（默认50万Token）

    返回:
        文件内容或上传后的文件对象
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    file_ext = os.path.splitext(file_path)[1].lower()

    # PDF文件直接上传（Google会自动处理）
    if file_ext == ".pdf":
        uploaded_file = genai.upload_file(path=file_path)
        print(f"文件已上传，Token数: {model.count_tokens(uploaded_file)}")
        return uploaded_file

    # 文本文件读取内容
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 计算token
    tokens = model.count_tokens(content)
    print(f"文件总Token数: {tokens}")

    # 未超过限制，直接返回
    if tokens.total_tokens <= chunk_size:
        return content

    # 超过限制
    print(f"文件超过 {chunk_size} Token，建议分段处理")
    return content


def load_image(image_path: str) -> Any:
    """
    加载图片文件

    参数:
        image_path: 图片文件路径

    返回:
        上传后的文件对象
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片不存在: {image_path}")
    return genai.upload_file(path=image_path)


# ============================================================================
# 对话功能
# ============================================================================

def chat_with_text(model: 'GenerativeModel', text_prompt: str) -> None:
    """
    单轮文本对话

    参数:
        model: Gemini 模型实例
        text_prompt: 用户输入的文本提示
    """
    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(text_prompt)
        print("=== Gemini 响应 ===")
        print(response.text)
    except Exception as e:
        print(f"调用出错: {e}")


def multi_turn_chat(model: 'GenerativeModel') -> None:
    """
    多轮对话（交互式）

    支持功能：
    - 持续对话，保留上下文
    - 输入 'exit'/'quit'/'bye' 退出
    - 输入 'clear' 清空历史
    - 输入 'history' 查看对话历史
    - 输入 'tokens' 查看Token使用情况

    参数:
        model: Gemini 模型实例
    """
    print("=" * 60)
    print("多轮对话模式已启动")
    print("命令提示:")
    print("  - 输入 'exit'/'quit'/'bye' 退出对话")
    print("  - 输入 'clear' 清空历史记录")
    print("  - 输入 'history' 查看对话历史")
    print("  - 输入 'tokens' 查看Token统计")
    print("=" * 60)

    # 创建会话（保留历史记录）
    chat_session = model.start_chat(history=[])
    turn_count = 0

    while True:
        try:
            # 获取用户输入
            user_input = input("\n你: ").strip()

            # 处理退出命令
            if user_input.lower() in ['exit', 'quit', 'bye', '退出']:
                print("\n再见！对话已结束。")
                print(f"总共进行了 {turn_count} 轮对话。")
                break

            # 处理清空历史命令
            if user_input.lower() in ['clear', '清空']:
                chat_session = model.start_chat(history=[])
                turn_count = 0
                print("✓ 历史记录已清空")
                continue

            # 处理查看历史命令
            if user_input.lower() in ['history', '历史']:
                if chat_session.history:
                    print("\n=== 对话历史 ===")
                    for i, msg in enumerate(chat_session.history):
                        role = "你" if msg.role == "user" else "AI"
                        content = msg.parts[0].text[:100] + "..." if len(msg.parts[0].text) > 100 else msg.parts[0].text
                        print(f"{i+1}. {role}: {content}")
                else:
                    print("暂无历史记录")
                continue

            # 处理查看Token命令
            if user_input.lower() in ['tokens', 'token']:
                if chat_session.history:
                    token_count = model.count_tokens(chat_session.history)
                    print(f"\n当前对话Token数: {token_count.total_tokens}")
                else:
                    print("暂无对话记录")
                continue

            # 空输入跳过
            if not user_input:
                print("请输入有效内容")
                continue

            # 发送消息并获取响应
            response = chat_session.send_message(user_input)
            turn_count += 1

            # 显示响应
            print(f"\nAI: {response.text}")

            # 显示Token使用情况（可选）
            if hasattr(response, 'usage_metadata'):
                print(f"\n[本轮Token] 输入: {response.usage_metadata.prompt_token_count} | "
                      f"输出: {response.usage_metadata.candidates_token_count}")

        except KeyboardInterrupt:
            print("\n\n对话被中断。")
            print(f"总共进行了 {turn_count} 轮对话。")
            break
        except Exception as e:
            print(f"出错: {e}")
            continue


def multi_turn_chat_programmatic(model: 'GenerativeModel', messages: list[str]) -> list[str]:
    """
    编程式多轮对话（批量处理）

    适用于需要批量处理多轮对话的场景

    参数:
        model: Gemini 模型实例
        messages: 用户消息列表

    返回:
        AI 响应列表

    示例:
        messages = ["你好", "介绍一下Python", "它有什么优点"]
        responses = multi_turn_chat_programmatic(model, messages)
    """
    chat_session = model.start_chat(history=[])
    responses = []

    try:
        for i, msg in enumerate(messages, 1):
            print(f"\n[第{i}轮] 用户: {msg}")
            response = chat_session.send_message(msg)
            print(f"[第{i}轮] AI: {response.text}")
            responses.append(response.text)

        return responses

    except Exception as e:
        print(f"调用出错: {e}")
        return responses


def chat_with_image(model: 'GenerativeModel', text_prompt: str, image_paths: list[str]) -> None:
    """
    多模态对话（文本 + 图片）

    参数:
        model: Gemini 模型实例
        text_prompt: 用户输入的文本提示
        image_paths: 图片文件路径列表
    """
    try:
        # 加载所有图片
        contents = [load_image(img) for img in image_paths]
        # 添加文本提示
        contents.append(text_prompt)

        # 发送请求
        response = model.generate_content(contents)

        print("=== Gemini 多模态响应 ===")
        print(response.text)
    except Exception as e:
        print(f"调用出错: {e}")


def chat_with_long_context(model: 'GenerativeModel', text_prompt: str, file_path: Optional[str] = None) -> None:
    """
    超长上下文对话（支持100万Token）

    适用于：
    - 分析整个代码库
    - 阅读长文档/PDF
    - 处理大型数据集

    参数:
        model: Gemini 模型实例
        text_prompt: 用户输入的文本提示
        file_path: 可选，附加文件路径（支持PDF/TXT/代码文件）
    """
    try:
        contents = []

        # 加载文件内容
        if file_path:
            file_content = load_long_text(model, file_path)
            contents.append(file_content)

        # 添加用户提示
        contents.append(text_prompt)

        # 发送请求
        response = model.generate_content(contents)

        print("=== Gemini 超长上下文响应 ===")
        print(response.text)

        # 显示Token使用统计
        if hasattr(response, 'usage_metadata'):
            print(f"\n[Token统计]")
            print(f"  输入: {response.usage_metadata.prompt_token_count} tokens")
            print(f"  输出: {response.usage_metadata.candidates_token_count} tokens")

    except Exception as e:
        print(f"调用出错: {e}")
