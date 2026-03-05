#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频生成功能测试脚本
用于测试新的 Veo 3.1 API
"""

import os
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from generation_mode import generate_video

def test_text_to_video():
    """测试文生视频"""
    print("=" * 70)
    print("测试 1: 文生视频")
    print("=" * 70)
    
    prompt = """A close up of a cute cat sleeping peacefully on a sunny windowsill,
with soft light filtering through the curtains. The cat's whiskers gently move 
as it breathes."""
    
    generate_video(
        prompt=prompt,
        output_path="test_cat_video.mp4",
        aspect_ratio="16:9",
        resolution="720p"
    )

if __name__ == "__main__":
    print("\n🎬 Veo 3.1 视频生成测试\n")
    
    # 测试文生视频
    try:
        test_text_to_video()
        print("\n✅ 测试完成！")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        print("\n请检查:")
        print("  1. 是否安装了 google-genai: pip install google-genai")
        print("  2. API Key 是否正确设置在 .env 文件中")
        print("  3. 网络连接是否正常")
