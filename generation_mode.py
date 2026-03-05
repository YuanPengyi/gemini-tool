#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成模式模块
支持：文生图、图文生图、文生视频、图生视频、图文生视频
"""

from typing import Optional
import google.generativeai as genai
import os


# ============================================================================
# 图片生成功能
# ============================================================================

def generate_image(prompt: str, output_path: str = "output.png") -> None:
    """
    文生图 (Text-to-Image) - 单次生成

    使用 Gemini 2.5 Flash Image 模型生成图片

    参数:
        prompt: 文本描述 prompt
        output_path: 输出图片保存路径
    """
    try:
        # 使用图像生成专用模型
        image_model = genai.GenerativeModel("gemini-2.5-flash-image")

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
        image_model = genai.GenerativeModel("gemini-2.5-flash-image")

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


# ============================================================================
# 视频生成功能
# ============================================================================

def generate_video(prompt: str, output_path: str = "output.mp4") -> None:
    """
    文生视频 (Text-to-Video)

    使用 Veo 2.0 模型生成视频

    参数:
        prompt: 文本描述 prompt
        output_path: 输出视频保存路径
    """
    try:
        video_model = genai.GenerativeModel("veo-2.0-generate-001")

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
        video_model = genai.GenerativeModel("veo-2.0-generate-001")

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
        video_model = genai.GenerativeModel("veo-2.0-generate-001")

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
