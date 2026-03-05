#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini API 工具集
=================

支持功能：
- 纯文本对话（单轮 & 多轮）
- 多模态对话（文本 + 图片）
- 超长上下文（100万Token）
- 文生图、图文生图、文生视频、图生视频、图文生视频
- 多轮迭代生成（持续优化图片/视频）

作者：Gemini Tool
版本：1.2.0
"""

from typing import Optional, Any, Union
import google.generativeai as genai
import os
from dotenv import load_dotenv

# ============================================================================
# 初始化配置
# ============================================================================

# 加载环境变量（API Key 存储在 .env 文件中）
load_dotenv()

# 从环境变量获取 API Key 并配置
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("未找到 GOOGLE_API_KEY，请在 .env 文件中配置")
genai.configure(api_key=API_KEY)


# ============================================================================
# 生成参数配置
# ============================================================================

# 基础生成参数
GENERATION_CONFIG = {
    "temperature": 0.7,           # 创造性控制：0-1，越高越有创意，越低越精确
    "top_p": 0.95,                # 核采样：控制输出多样性
    "top_k": 64,                  # 限制每步考虑的词数
    "max_output_tokens": 64000,   # 最大输出token数
    "response_mime_type": "text/plain",  # 输出格式
}

# 推理增强配置（Gemini 2.0+ 支持）
THINKING_CONFIG = {
    "include_thoughts": True  # 是否返回思考过程
}

# 安全过滤设置（使用中等强度过滤）
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]


# ============================================================================
# 模型初始化
# ============================================================================

# 对话模型（支持100万Token上下文）
MODEL_NAME = "gemini-1.5-pro"
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config=GENERATION_CONFIG,
    safety_settings=SAFETY_SETTINGS,
    system_instruction="你是资深编程导师，解决复杂算法问题时步骤清晰、逻辑严谨。"
)


# ============================================================================
# 工具函数
# ============================================================================

def count_tokens(text_or_file: Union[str, Any]) -> Union[int, str]:
    """
    计算文本或文件的Token数量

    参数:
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


def load_long_text(file_path: str, chunk_size: int = 500000) -> Union[str, Any]:
    """
    加载超长文本/文档（自动处理）

    支持格式：
    - PDF文件：直接上传
    - 文本文件：读取内容

    参数:
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

def chat_with_text(text_prompt: str) -> None:
    """
    单轮文本对话

    参数:
        text_prompt: 用户输入的文本提示
    """
    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(text_prompt)
        print("=== Gemini 响应 ===")
        print(response.text)
    except Exception as e:
        print(f"调用出错: {e}")


def multi_turn_chat() -> None:
    """
    多轮对话（交互式）

    支持功能：
    - 持续对话，保留上下文
    - 输入 'exit'/'quit'/'bye' 退出
    - 输入 'clear' 清空历史
    - 输入 'history' 查看对话历史
    - 输入 'tokens' 查看Token使用情况
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


def multi_turn_chat_programmatic(messages: list[str]) -> list[str]:
    """
    编程式多轮对话（批量处理）

    适用于需要批量处理多轮对话的场景

    参数:
        messages: 用户消息列表

    返回:
        AI 响应列表

    示例:
        messages = ["你好", "介绍一下Python", "它有什么优点"]
        responses = multi_turn_chat_programmatic(messages)
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


def chat_with_image(text_prompt: str, image_paths: list[str]) -> None:
    """
    多模态对话（文本 + 图片）

    参数:
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


def chat_with_long_context(text_prompt: str, file_path: Optional[str] = None) -> None:
    """
    超长上下文对话（支持100万Token）

    适用于：
    - 分析整个代码库
    - 阅读长文档/PDF
    - 处理大型数据集

    参数:
        text_prompt: 用户输入的文本提示
        file_path: 可选，附加文件路径（支持PDF/TXT/代码文件）
    """
    try:
        contents = []

        # 加载文件内容
        if file_path:
            file_content = load_long_text(file_path)
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


# ============================================================================
# 生成功能（文生图/视频）
# ============================================================================

def generate_image(prompt: str, output_path: str = "output.png") -> None:
    """
    文生图 (Text-to-Image) - 单次生成

    使用 Imagen 3.0 模型生成图片

    参数:
        prompt: 文本描述 prompt
        output_path: 输出图片保存路径
    """
    try:
        # 使用图像生成专用模型
        image_model = genai.GenerativeModel("imagen-3.0-generate-002")

        # 生成图片
        response = image_model.generate_content(
            prompt,
            generation_config={"response_mime_type": "image/png"}
        )

        # 保存生成的图片
        if response.generated_images:
            image = response.generated_images[0]
            with open(output_path, "wb") as f:
                f.write(image.image.bytes)
            print(f"✓ 图片已保存到: {output_path}")
        else:
            print("✗ 未能生成图片")

    except Exception as e:
        print(f"调用出错: {e}")


def multi_turn_image_generation() -> None:
    """
    多轮图片生成（交互式迭代优化）

    功能特性：
    - 持续优化图片生成
    - 基于上一张图片进行调整
    - 保留所有版本历史

    命令：
    - 输入描述词生成/优化图片
    - 'show' - 显示当前图片路径
    - 'history' - 查看生成历史
    - 'save <name>' - 保存当前版本为指定名称
    - 'exit' - 退出
    """
    print("=" * 60)
    print("多轮图片生成模式")
    print("命令提示:")
    print("  - 输入描述词生成新图片")
    print("  - 输入调整需求基于当前图片优化")
    print("  - 'show' 显示当前图片路径")
    print("  - 'history' 查看生成历史")
    print("  - 'save <名称>' 保存当前版本")
    print("  - 'exit' 退出")
    print("=" * 60)

    image_model = genai.GenerativeModel("imagen-3.0-generate-002")
    current_image = None
    generation_history = []
    version = 0

    while True:
        try:
            user_input = input("\n描述/调整: ").strip()

            # 处理退出
            if user_input.lower() in ['exit', 'quit', '退出']:
                print(f"\n生成结束，共生成 {version} 个版本")
                break

            # 显示当前图片
            if user_input.lower() == 'show':
                if current_image:
                    print(f"当前图片: {current_image}")
                else:
                    print("还未生成图片")
                continue

            # 查看历史
            if user_input.lower() == 'history':
                if generation_history:
                    print("\n=== 生成历史 ===")
                    for i, record in enumerate(generation_history, 1):
                        print(f"{i}. {record['prompt'][:50]}... -> {record['path']}")
                else:
                    print("暂无历史记录")
                continue

            # 保存当前版本
            if user_input.lower().startswith('save '):
                if current_image:
                    save_name = user_input[5:].strip()
                    import shutil
                    save_path = f"{save_name}.png"
                    shutil.copy(current_image, save_path)
                    print(f"✓ 已保存到: {save_path}")
                else:
                    print("还未生成图片")
                continue

            if not user_input:
                print("请输入描述或调整需求")
                continue

            # 生成新图片
            version += 1
            output_path = f"generated_v{version}.png"

            print(f"\n[版本 {version}] 生成中...")

            # 如果有当前图片，基于它进行优化
            if current_image:
                uploaded_image = genai.upload_file(path=current_image)
                contents = [uploaded_image, user_input]
                response = image_model.generate_content(
                    contents,
                    generation_config={"response_mime_type": "image/png"}
                )
            else:
                # 首次生成
                response = image_model.generate_content(
                    user_input,
                    generation_config={"response_mime_type": "image/png"}
                )

            # 保存生成的图片
            if response.generated_images:
                image = response.generated_images[0]
                with open(output_path, "wb") as f:
                    f.write(image.image.bytes)
                current_image = output_path
                generation_history.append({
                    "version": version,
                    "prompt": user_input,
                    "path": output_path
                })
                print(f"✓ [版本 {version}] 已生成: {output_path}")
            else:
                print("✗ 生成失败")
                version -= 1

        except KeyboardInterrupt:
            print(f"\n\n生成中断，共生成 {version} 个版本")
            break
        except Exception as e:
            print(f"出错: {e}")
            version -= 1
            continue


def multi_turn_video_generation() -> None:
    """
    多轮视频生成（交互式迭代优化）

    功能特性：
    - 持续优化视频生成
    - 基于上一个视频或图片进行调整
    - 支持图生视频和文生视频

    命令：
    - 输入描述词生成/优化视频
    - 'image <路径>' - 从图片开始生成视频
    - 'history' - 查看生成历史
    - 'exit' - 退出
    """
    print("=" * 60)
    print("多轮视频生成模式")
    print("命令提示:")
    print("  - 输入描述词生成视频")
    print("  - 'image <路径>' 从图片生成视频")
    print("  - 'history' 查看生成历史")
    print("  - 'exit' 退出")
    print("=" * 60)

    video_model = genai.GenerativeModel("veo-2.0-generate-002")
    generation_history = []
    version = 0
    base_image = None

    while True:
        try:
            user_input = input("\n描述/调整: ").strip()

            # 处理退出
            if user_input.lower() in ['exit', 'quit', '退出']:
                print(f"\n生成结束，共生成 {version} 个版本")
                break

            # 设置基础图片
            if user_input.lower().startswith('image '):
                image_path = user_input[6:].strip()
                if os.path.exists(image_path):
                    base_image = image_path
                    print(f"✓ 已设置基础图片: {base_image}")
                else:
                    print("图片不存在")
                continue

            # 查看历史
            if user_input.lower() == 'history':
                if generation_history:
                    print("\n=== 生成历史 ===")
                    for i, record in enumerate(generation_history, 1):
                        print(f"{i}. {record['prompt'][:50]}... -> {record['uri']}")
                else:
                    print("暂无历史记录")
                continue

            if not user_input:
                print("请输入描述或调整需求")
                continue

            # 生成视频
            version += 1
            print(f"\n[版本 {version}] 生成中（视频生成较慢，请耐心等待）...")

            contents = []
            if base_image:
                uploaded_image = genai.upload_file(path=base_image)
                contents.append(uploaded_image)

            contents.append(user_input)

            response = video_model.generate_content(contents)

            if response.generated_videos:
                video_uri = response.generated_videos[0].uri
                generation_history.append({
                    "version": version,
                    "prompt": user_input,
                    "uri": video_uri
                })
                print(f"✓ [版本 {version}] 视频生成成功")
                print(f"  视频URI: {video_uri}")
            else:
                print("✗ 生成失败")
                version -= 1

        except KeyboardInterrupt:
            print(f"\n\n生成中断，共生成 {version} 个版本")
            break
        except Exception as e:
            print(f"出错: {e}")
            version -= 1
            continue


def generate_image_from_image(prompt: str, reference_image_path: str, output_path: str = "output.png") -> None:
    """
    图文生图 (Image-to-Image)

    基于参考图片和文本描述生成新图片

    适用场景：
    - 图片风格转换
    - 图片编辑/修改
    - 以图生图创作

    参数:
        prompt: 文本描述 prompt
        reference_image_path: 参考图片路径
        output_path: 输出图片保存路径
    """
    try:
        image_model = genai.GenerativeModel("imagen-3.0-generate-002")

        # 加载参考图片
        uploaded_image = genai.upload_file(path=reference_image_path)

        # 组合输入：图片 + 文本描述
        contents = [uploaded_image, prompt]

        # 生成图片
        response = image_model.generate_content(
            contents,
            generation_config={"response_mime_type": "image/png"}
        )

        # 保存生成的图片
        if response.generated_images:
            image = response.generated_images[0]
            with open(output_path, "wb") as f:
                f.write(image.image.bytes)
            print(f"✓ 图文生图完成，已保存到: {output_path}")
        else:
            print("✗ 未能生成图片")

    except Exception as e:
        print(f"调用出错: {e}")


def generate_video(prompt: str, output_path: str = "output.mp4") -> None:
    """
    文生视频 (Text-to-Video)

    使用 Veo 2.0 模型生成视频

    参数:
        prompt: 文本描述 prompt
        output_path: 输出视频保存路径
    """
    try:
        video_model = genai.GenerativeModel("veo-2.0-generate-002")

        response = video_model.generate_content(prompt)

        if response.generated_videos:
            video = response.generated_videos[0]
            print(f"✓ 视频生成中，请等待...")
            print(f"  视频URI: {video.uri}")
            print(f"  保存路径: {output_path}")
        else:
            print("✗ 未能生成视频")

    except Exception as e:
        print(f"调用出错: {e}")


def generate_image_to_video(image_path: str, prompt: str = "") -> None:
    """
    图生视频 (Image-to-Video)

    将静态图片转换为动态视频

    参数:
        image_path: 输入图片路径
        prompt: 可选，附加文本描述
    """
    try:
        video_model = genai.GenerativeModel("veo-2.0-generate-002")

        # 加载图片
        uploaded_image = genai.upload_file(path=image_path)

        # 组合输入
        contents = [uploaded_image]
        if prompt:
            contents.append(prompt)

        response = video_model.generate_content(contents)

        print(f"✓ 图生视频生成中，请等待...")
        if response.generated_videos:
            print(f"  视频URI: {response.generated_videos[0].uri}")

    except Exception as e:
        print(f"调用出错: {e}")


def generate_image_with_video(prompt: str, image_paths: Optional[list[str]] = None) -> None:
    """
    图文生视频 (Image+Text-to-Video)

    结合图片和文本描述生成视频

    参数:
        prompt: 文本描述 prompt
        image_paths: 输入图片路径列表
    """
    try:
        video_model = genai.GenerativeModel("veo-2.0-generate-002")

        contents = []

        # 添加所有图片
        if image_paths:
            for img_path in image_paths:
                contents.append(genai.upload_file(path=img_path))

        # 添加文本提示
        contents.append(prompt)

        response = video_model.generate_content(contents)

        print(f"✓ 图文生视频生成中，请等待...")
        if response.generated_videos:
            print(f"  视频URI: {response.generated_videos[0].uri}")

    except Exception as e:
        print(f"调用出错: {e}")


# ============================================================================
# 主程序入口
# ============================================================================

if __name__ == "__main__":
    # 根据需要取消注释以下调用

    # ============ 对话模式 ============
    # 1. 单轮对话
    # chat_with_text("用Python实现快速排序")

    # 2. 多轮对话（交互式）
    # multi_turn_chat()

    # 3. 多轮对话（编程式）
    # messages = ["你好", "介绍一下Python", "它有什么优点"]
    # multi_turn_chat_programmatic(messages)

    # 4. 多模态对话
    # chat_with_image("描述这张图片", ["demo.jpg"])

    # 5. 超长上下文
    # chat_with_long_context("总结这个文件", file_path="gemini.py")

    # ============ 生成模式 ============
    # 单次生成
    # generate_image("一只可爱的小猫在草地上玩耍")
    # generate_image_from_image("把这幅画变成水彩画风格", "reference.jpg")
    # generate_video("一只狗在海滩上奔跑")
    # generate_image_to_video("input.jpg", "让画面动起来")
    # generate_image_with_video("让场景更具动感", image_paths=["image.jpg"])

    # ============ 多轮生成模式 ============
    # 多轮图片生成（持续迭代优化）
    multi_turn_image_generation()

    # 多轮视频生成（持续迭代优化）
    # multi_turn_video_generation()
