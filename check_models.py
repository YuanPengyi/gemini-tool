#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查当前项目使用的模型是否正确"""

import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

print('=' * 70)
print('模型检查工具 - 验证项目中使用的模型是否可用')
print('=' * 70)

# 获取所有可用模型
available_models = {model.name for model in genai.list_models()}

print(f'\n✓ API 当前可用模型总数: {len(available_models)}\n')

# 项目中使用的模型
project_models = {
    '对话模型': ['gemini-2.5-flash', 'gemini-2.5-pro'],
    '图像模型': ['gemini-2.5-flash-image'],
    '视频模型': []  # Veo 已不再支持 generateContent，功能已禁用
}

print('检查项目使用的模型：\n')

all_valid = True
for category, models in project_models.items():
    print(f'{category}:')
    for model in models:
        full_name = f'models/{model}'
        if full_name in available_models:
            print(f'  ✅ {model} - 可用')
        else:
            print(f'  ❌ {model} - 不可用！')
            all_valid = False
            # 查找相似模型
            similar = [m for m in available_models if model.split('-')[0] in m]
            if similar:
                print(f'     建议使用: {", ".join([m.replace("models/", "") for m in similar[:3]])}')
    print()

# 显示推荐的生成模型
print('=' * 70)
print('可用的生成模型（支持 generateContent）：\n')

categories = {
    '图像': ['imagen'],
    '视频': ['veo'],
    '对话（Flash）': ['flash'],
    '对话（Pro）': ['2.5-pro', '2.0-pro']
}

for cat_name, keywords in categories.items():
    models = []
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            model_name = model.name.replace('models/', '')
            if any(kw in model_name.lower() for kw in keywords):
                models.append(model_name)
    
    if models:
        print(f'{cat_name}:')
        for m in models[:5]:  # 只显示前5个
            print(f'  • {m}')
        print()

print('=' * 70)
if all_valid:
    print('✅ 所有模型检查通过！项目配置正确。')
else:
    print('⚠️  发现不可用的模型，请更新配置！')
print('=' * 70)
