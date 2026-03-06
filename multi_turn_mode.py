#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多轮生成模式模块
支持：多轮图片生成、多轮视频生成（迭代优化）
"""

from google import genai
from google.genai import types
import os
import time
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


# ============================================================================
# 多轮图片生成
# ============================================================================

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
    print("🎨 多轮图片生成模式")
    print("命令提示:")
    print("  - 输入描述词生成新图片")
    print("  - 输入调整需求基于当前图片优化")
    print("  - 'show' 显示当前图片路径")
    print("  - 'history' 查看生成历史")
    print("  - 'save <名称>' 保存当前版本")
    print("  - 'exit' 退出")
    print("=" * 60)

    # 初始化客户端
    client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
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
                    print(f"✅ 已保存到: {save_path}")
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
                reference_image = types.Image.from_file(location=current_image)
                contents = [reference_image, user_input]
            else:
                # 首次生成
                contents = user_input

            response = client.models.generate_content(
                model='gemini-2.5-flash-image',
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(
                        aspect_ratio="1:1",
                    ),
                ),
            )

            # 保存生成的图片
            saved = False
            for part in response.parts:
                if part.inline_data:
                    generated_image = part.as_image()
                    generated_image.save(output_path)
                    current_image = output_path
                    generation_history.append({
                        "version": version,
                        "prompt": user_input,
                        "path": output_path
                    })
                    saved = True
                    break
            
            if saved:
                print(f"✅ [版本 {version}] 已生成: {output_path}")
            else:
                print("❌ 生成失败")
                version -= 1

        except KeyboardInterrupt:
            print(f"\n\n生成中断，共生成 {version} 个版本")
            break
        except Exception as e:
            print(f"❌ 出错: {e}")
            version -= 1
            continue


# ============================================================================
# 多轮视频生成
# ============================================================================

def multi_turn_video_generation() -> None:
    """
    多轮视频生成（交互式迭代优化）

    功能特性：
    - 持续优化视频生成（基于视频扩展功能）
    - 从图片开始或文本开始生成视频
    - 每次可扩展 7 秒（最多 20 次）
    - 支持调整提示词进行优化

    命令：
    - 输入描述词生成/扩展视频
    - 'image <路径>' - 从图片开始生成视频
    - 'history' - 查看生成历史
    - 'exit' - 退出
    """
    print("=" * 70)
    print("🎬 多轮视频生成模式 (Veo 3.1)")
    print("=" * 70)
    print("命令提示:")
    print("  - 输入描述词生成/扩展视频")
    print("  - 'image <路径>' 从图片生成视频")
    print("  - 'history' 查看生成历史")
    print("  - 'exit' 退出")
    print("=" * 70)

    # 初始化客户端
    client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
    
    generation_history = []
    version = 0
    current_video_path = None
    start_with_image = None

    while True:
        try:
            user_input = input("\n🎬 描述/调整: ").strip()

            # 处理退出
            if user_input.lower() in ['exit', 'quit', '退出']:
                print(f"\n生成结束，共生成 {version} 个版本")
                break

            # 设置起始图片
            if user_input.lower().startswith('image '):
                image_path = user_input[6:].strip()
                if os.path.exists(image_path):
                    start_with_image = image_path
                    print(f"✅ 已设置起始图片: {start_with_image}")
                else:
                    print("❌ 图片不存在")
                continue

            # 查看历史
            if user_input.lower() == 'history':
                if generation_history:
                    print("\n=== 生成历史 ===")
                    for i, record in enumerate(generation_history, 1):
                        print(f"{i}. [{record['type']}] {record['prompt'][:40]}...")
                        print(f"   保存路径: {record['path']}")
                else:
                    print("暂无历史记录")
                continue

            if not user_input:
                print("请输入描述或调整需求")
                continue

            # 生成/扩展视频
            version += 1
            output_path = f"video_v{version}.mp4"
            
            print(f"\n[版本 {version}] 生成中（视频生成较慢，请耐心等待）...")

            if current_video_path:
                # 扩展现有视频
                print("📹 基于上一个视频进行扩展...")
                uploaded_video = client.files.upload(file=current_video_path)
                
                operation = client.models.generate_videos(
                    model="veo-3.1-generate-preview",
                    video=uploaded_video,
                    prompt=user_input,
                    config=types.GenerateVideosConfig(
                        resolution="720p"  # 扩展必须使用 720p
                    ),
                )
                video_type = "扩展"
                
            elif start_with_image:
                # 从图片生成
                print("🖼️  从图片生成视频...")
                image = types.Image.from_file(location=start_with_image)
                
                operation = client.models.generate_videos(
                    model="veo-3.1-generate-preview",
                    prompt=user_input,
                    image=image,
                    config=types.GenerateVideosConfig(
                        aspect_ratio="16:9",
                        resolution="720p",
                    ),
                )
                video_type = "图生视频"
                start_with_image = None  # 用过后清除
                
            else:
                # 从文本生成
                print("📝 从文本生成视频...")
                operation = client.models.generate_videos(
                    model="veo-3.1-generate-preview",
                    prompt=user_input,
                    config=types.GenerateVideosConfig(
                        aspect_ratio="16:9",
                        resolution="720p",
                    ),
                )
                video_type = "文生视频"

            # 轮询操作状态
            wait_count = 0
            while not operation.done:
                wait_count += 1
                if wait_count % 3 == 0:
                    print(f"   已等待 {wait_count * 10} 秒...")
                time.sleep(10)
                operation = client.operations.get(operation)

            # 下载视频
            generated_video = operation.response.generated_videos[0]
            client.files.download(file=generated_video.video)
            generated_video.video.save(output_path)
            
            current_video_path = output_path  # 保存路径供下次扩展使用
            
            generation_history.append({
                "version": version,
                "type": video_type,
                "prompt": user_input,
                "path": output_path
            })
            
            print(f"✅ [版本 {version}] 视频生成成功！")
            print(f"  类型: {video_type}")
            print(f"  保存路径: {output_path}")
            if version < 20:
                print(f"  💡 可以继续输入描述扩展视频（剩余 {20 - version} 次）")
            else:
                print("  ⚠️  已达到最大扩展次数（20次）")

        except KeyboardInterrupt:
            print(f"\n\n生成中断，共生成 {version} 个版本")
            break
        except Exception as e:
            print(f"❌ 出错: {e}")
            version -= 1
            continue
