#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多轮生成模式模块
支持：多轮图片生成、多轮视频生成（迭代优化）
"""

import google.generativeai as genai
import os


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


# ============================================================================
# 多轮视频生成
# ============================================================================

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
