#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成模式模块
支持：文生图、图文生图、文生视频、图生视频、图文生视频
"""

from typing import Optional
from google import genai
from google.genai import types
import os
import time
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


# ============================================================================
# 图片生成功能（使用新的 google.genai SDK）
# ============================================================================

def generate_image(prompt: str, output_path: str = "output.png", aspect_ratio: str = "1:1") -> None:
    """
    文生图 (Text-to-Image) - 单次生成

    使用 Gemini 2.5 Flash Image 模型生成图片

    参数:
        prompt: 文本描述 prompt
        output_path: 输出图片保存路径
        aspect_ratio: 宽高比，如 "1:1", "16:9", "9:16" 等
    """
    try:
        # 初始化客户端
        client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
        
        print(f"🎨 开始生成图片...")
        print(f"  提示词: {prompt[:50]}...")
        
        # 生成图片
        response = client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                ),
            ),
        )

        # 保存生成的图片
        saved = False
        for part in response.parts:
            if part.inline_data:
                generated_image = part.as_image()
                generated_image.save(output_path)
                saved = True
                break
        
        if saved:
            print(f"✅ 图片已保存到: {output_path}")
        else:
            print("❌ 未能生成图片")

    except Exception as e:
        print(f"❌ 调用出错: {e}")


def generate_image_from_image(
    prompt: str, 
    reference_image_path: str, 
    output_path: str = "output.png",
    aspect_ratio: str = "1:1"
) -> None:
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
        aspect_ratio: 宽高比，如 "1:1", "16:9", "9:16" 等
    """
    try:
        if not os.path.exists(reference_image_path):
            print(f"❌ 参考图片不存在: {reference_image_path}")
            return
            
        # 初始化客户端
        client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
        
        print(f"🎨 开始图文生图...")
        print(f"  参考图片: {reference_image_path}")
        print(f"  提示词: {prompt[:50]}...")
        
        # 加载参考图片
        reference_image = types.Image.from_file(location=reference_image_path)
        
        # 组合输入：图片 + 文本描述
        contents = [reference_image, prompt]

        # 生成图片
        response = client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                ),
            ),
        )

        # 保存生成的图片
        saved = False
        for part in response.parts:
            if part.inline_data:
                generated_image = part.as_image()
                generated_image.save(output_path)
                saved = True
                break
        
        if saved:
            print(f"✅ 图文生图完成，已保存到: {output_path}")
        else:
            print("❌ 未能生成图片")

    except Exception as e:
        print(f"❌ 调用出错: {e}")


# ============================================================================
# 视频生成功能（使用新的 google.genai SDK）
# ============================================================================

def generate_video(
    prompt: str, 
    output_path: str = "output.mp4",
    aspect_ratio: str = "16:9",
    resolution: str = "720p"
) -> None:
    """
    文生视频 (Text-to-Video)
    
    使用 Veo 3.1 模型生成视频（支持音频）
    
    参数:
        prompt: 文本描述 prompt（可包含对话、音效描述）
        output_path: 输出视频保存路径
        aspect_ratio: 宽高比，"16:9"（横屏）或 "9:16"（竖屏）
        resolution: 分辨率，"720p"、"1080p" 或 "4k"
    
    注意：
    - 视频时长固定为 8 秒
    - 1080p 和 4k 仅支持 8 秒时长
    - 生成的视频在服务器上仅保留 2 天
    """
    try:
        # 初始化新 SDK 客户端
        client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
        
        print(f"🎬 开始生成视频...")
        print(f"  提示词: {prompt[:50]}...")
        print(f"  分辨率: {resolution} ({aspect_ratio})")
        
        # 发起视频生成请求
        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=prompt,
            config=types.GenerateVideosConfig(
                aspect_ratio=aspect_ratio,
                resolution=resolution,
            ),
        )
        
        # 轮询操作状态
        print("⏳ 视频生成中，请等待...")
        wait_count = 0
        while not operation.done:
            wait_count += 1
            if wait_count % 3 == 0:
                print(f"   已等待 {wait_count * 10} 秒...")
            time.sleep(10)
            operation = client.operations.get(operation)
        
        # 下载生成的视频
        generated_video = operation.response.generated_videos[0]
        client.files.download(file=generated_video.video)
        generated_video.video.save(output_path)
        
        print(f"✅ 视频生成成功！")
        print(f"  保存路径: {output_path}")
        print(f"  提示: 视频在服务器上仅保留 2 天，请及时备份")
        
    except Exception as e:
        print(f"❌ 视频生成失败: {e}")
        print(f"   请检查：")
        print(f"   1. API Key 是否正确")
        print(f"   2. 是否已安装 google-genai 包: pip install google-genai")
        print(f"   3. 网络连接是否正常")


def generate_image_to_video(
    image_path: str, 
    prompt: str = "",
    output_path: str = "image_to_video.mp4",
    aspect_ratio: str = "16:9",
    resolution: str = "720p"
) -> None:
    """
    图生视频 (Image-to-Video)
    
    将静态图片转换为动态视频，图片作为起始帧
    
    参数:
        image_path: 输入图片路径
        prompt: 可选，附加文本描述（描述视频动作）
        output_path: 输出视频保存路径
        aspect_ratio: 宽高比，"16:9" 或 "9:16"
        resolution: 分辨率，"720p"、"1080p" 或 "4k"
    """
    try:
        if not os.path.exists(image_path):
            print(f"❌ 图片不存在: {image_path}")
            return
            
        # 初始化新 SDK 客户端
        client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
        
        print(f"🎬 开始图生视频...")
        print(f"  输入图片: {image_path}")
        print(f"  提示词: {prompt if prompt else '(无)'}")
        
        # 从本地文件创建 Image 对象
        print("📤 加载图片中...")
        image = types.Image.from_file(location=image_path)
        
        # 发起视频生成请求
        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=prompt if prompt else "Animate this image naturally",
            image=image,
            config=types.GenerateVideosConfig(
                aspect_ratio=aspect_ratio,
                resolution=resolution,
            ),
        )
        
        # 轮询操作状态
        print("⏳ 视频生成中，请等待...")
        wait_count = 0
        while not operation.done:
            wait_count += 1
            if wait_count % 3 == 0:
                print(f"   已等待 {wait_count * 10} 秒...")
            time.sleep(10)
            operation = client.operations.get(operation)
        
        # 下载生成的视频
        generated_video = operation.response.generated_videos[0]
        client.files.download(file=generated_video.video)
        generated_video.video.save(output_path)
        
        print(f"✅ 图生视频成功！")
        print(f"  保存路径: {output_path}")
        
    except Exception as e:
        print(f"❌ 图生视频失败: {e}")


def generate_image_with_video(
    prompt: str, 
    image_paths: Optional[list[str]] = None,
    output_path: str = "multi_image_video.mp4",
    aspect_ratio: str = "16:9",
    resolution: str = "720p"
) -> None:
    """
    图文生视频 (Image+Text-to-Video)
    
    结合多张参考图片和文本描述生成视频
    支持最多 3 张参考图片，用于指导人物、角色或产品的外观
    
    参数:
        prompt: 文本描述 prompt
        image_paths: 参考图片路径列表（最多3张）
        output_path: 输出视频保存路径
        aspect_ratio: 宽高比，"16:9" 或 "9:16"
        resolution: 分辨率，"720p"、"1080p" 或 "4k"
    """
    try:
        # 初始化新 SDK 客户端
        client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
        
        print(f"🎬 开始多图文生视频...")
        print(f"  提示词: {prompt[:50]}...")
        
        # 上传参考图片
        reference_images = []
        if image_paths:
            if len(image_paths) > 3:
                print("⚠️  最多支持 3 张参考图片，将使用前 3 张")
                image_paths = image_paths[:3]
            
            print(f"📤 加载 {len(image_paths)} 张参考图片...")
            for img_path in image_paths:
                if os.path.exists(img_path):
                    image = types.Image.from_file(location=img_path)
                    reference_images.append(
                        types.VideoGenerationReferenceImage(
                            image=image,
                            reference_type="asset"  # 用于角色、产品等
                        )
                    )
                    print(f"  ✓ {img_path}")
                else:
                    print(f"  ⚠️  跳过不存在的图片: {img_path}")
        
        # 配置生成参数
        config = types.GenerateVideosConfig(
            aspect_ratio=aspect_ratio,
            resolution=resolution,
        )
        if reference_images:
            config.reference_images = reference_images
        
        # 发起视频生成请求
        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=prompt,
            config=config,
        )
        
        # 轮询操作状态
        print("⏳ 视频生成中，请等待...")
        wait_count = 0
        while not operation.done:
            wait_count += 1
            if wait_count % 3 == 0:
                print(f"   已等待 {wait_count * 10} 秒...")
            time.sleep(10)
            operation = client.operations.get(operation)
        
        # 下载生成的视频
        generated_video = operation.response.generated_videos[0]
        client.files.download(file=generated_video.video)
        generated_video.video.save(output_path)
        
        print(f"✅ 多图文生视频成功！")
        print(f"  保存路径: {output_path}")
        
    except Exception as e:
        print(f"❌ 多图文生视频失败: {e}")


def extend_video(
    video_path: str,
    prompt: str,
    output_path: str = "extended_video.mp4"
) -> None:
    """
    视频扩展 (Video Extension)
    
    将已有视频延长 7 秒（最多可延长 20 次）
    
    参数:
        video_path: 输入视频路径（必须是之前由 Veo 生成的视频）
        prompt: 描述扩展部分的提示词
        output_path: 输出视频保存路径
    
    注意：
    - 仅支持 720p 分辨率
    - 输入视频时长上限为 141 秒
    - 每次延长 7 秒
    """
    try:
        if not os.path.exists(video_path):
            print(f"❌ 视频不存在: {video_path}")
            return
            
        # 初始化新 SDK 客户端
        client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
        
        print(f"🎬 开始视频扩展...")
        print(f"  输入视频: {video_path}")
        print(f"  提示词: {prompt[:50]}...")
        
        # 上传视频
        print("📤 上传视频中...")
        uploaded_video = client.files.upload(file=video_path)
        
        # 发起视频扩展请求
        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            video=uploaded_video,
            prompt=prompt,
            config=types.GenerateVideosConfig(
                resolution="720p"  # 扩展必须使用 720p
            ),
        )
        
        # 轮询操作状态
        print("⏳ 视频扩展中，请等待...")
        wait_count = 0
        while not operation.done:
            wait_count += 1
            if wait_count % 3 == 0:
                print(f"   已等待 {wait_count * 10} 秒...")
            time.sleep(10)
            operation = client.operations.get(operation)
        
        # 下载扩展后的视频
        generated_video = operation.response.generated_videos[0]
        client.files.download(file=generated_video.video)
        generated_video.video.save(output_path)
        
        print(f"✅ 视频扩展成功！")
        print(f"  保存路径: {output_path}")
        print(f"  💡 可以继续扩展此视频（最多 20 次）")
        
    except Exception as e:
        print(f"❌ 视频扩展失败: {e}")
        print(f"   提示: 请确保输入的是由 Veo 生成的视频")
