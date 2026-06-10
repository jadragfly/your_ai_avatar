#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Avatar 项目生成器
根据配置生成完整的 AI Avatar 3D 虚拟形象网页工程
"""

import os
import sys
import shutil
import requests

# ==================== 模板替换标记 ====================
PLACEHOLDERS = {
    'API_URL': '{{API_URL}}',
    'API_PATH': '{{API_PATH}}',
    'MODEL': '{{MODEL}}',
    'AI_MODEL_NAME': '{{AI_MODEL_NAME}}'
}

def log(*args):
    print('[Generator]', *args)

def error(*args):
    print('[Error]', *args)

def generate_project(project_dir, backend_type, config):
    """
    生成 AI Avatar 项目

    Args:
        project_dir: 项目目录路径
        backend_type: 'tbox' 或 'ollama'
        config: 配置字典
    """
    log('=' * 50)
    log('AI Avatar 项目生成器')
    log('=' * 50)

    # 创建项目目录
    os.makedirs(project_dir, exist_ok=True)
    log(f'项目目录: {project_dir}')

    # 获取模板目录
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(skill_dir, 'templates')

    if not os.path.exists(template_dir):
        error('模板目录不存在')
        return False

    # 复制模板文件
    files_to_copy = ['index.html', 'requirements.txt', 'server_doubao.py']

    for filename in files_to_copy:
        src = os.path.join(template_dir, filename)
        dst = os.path.join(project_dir, filename.replace('server_doubao.py', 'server.py'))

        if os.path.exists(src):
            shutil.copy2(src, dst)
            log(f'复制文件: {filename}')
        else:
            log(f'跳过文件: {filename} (不存在)')

    # 复制 VRM 模型文件（已包含在模板中）
    vrm_src = os.path.join(template_dir, 'sample.vrm')
    vrm_dst = os.path.join(project_dir, 'sample.vrm')
    if os.path.exists(vrm_src):
        shutil.copy2(vrm_src, vrm_dst)
        log('复制 VRM 模型文件')

    # 处理 index.html 中的占位符
    index_path = os.path.join(project_dir, 'index.html')
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 替换占位符
        content = content.replace(PLACEHOLDERS['API_URL'], config.get('api_url', 'http://localhost:5000'))
        content = content.replace(PLACEHOLDERS['API_PATH'], config.get('api_path', '/api/chat'))
        content = content.replace(PLACEHOLDERS['MODEL'], config.get('model', ''))
        content = content.replace(PLACEHOLDERS['AI_MODEL_NAME'], config.get('model_name', 'AI'))

        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)

        log('替换 index.html 占位符完成')

    # 选择并复制后端文件
    if backend_type == 'tbox':
        server_src = os.path.join(template_dir, 'server_tbox.py')
        server_dst = os.path.join(project_dir, 'server.py')
    else:
        server_src = os.path.join(template_dir, 'server_ollama.py')
        server_dst = os.path.join(project_dir, 'server.py')

    if os.path.exists(server_src):
        shutil.copy2(server_src, server_dst)
        log(f'复制后端文件: server.py ({backend_type})')

    log('=' * 50)
    log('项目生成完成!')
    log('=' * 50)

    return True

def get_ollama_models():
    """获取本地 Ollama 可用模型"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [m['name'] for m in data.get('models', [])]
    except:
        pass
    return []

def main():
    """主函数 - 演示用法"""
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║           AI Avatar 项目生成器                         ║
    ║                                                       ║
    ║  用法:                                                ║
    ║    from generator import generate_project             ║
    ║                                                       ║
    ║    # TBOX 配置                                        ║
    ║    config = {                                         ║
    ║        'model': 'Qwen/Qwen3-235B-A22B-Instruct-2507',║
    ║        'model_name': '百灵大模型'                     ║
    ║    }                                                  ║
    ║    generate_project('./ai-avatar-web', 'tbox', config)║
    ║                                                       ║
    ║    # Ollama 配置                                      ║
    ║    config = {                                         ║
    ║        'model': 'qwen3:4b',                          ║
    ║        'model_name': 'Qwen3 4B'                      ║
    ║    }                                                  ║
    ║    generate_project('./ai-avatar-web', 'ollama', config)║
    ╚═══════════════════════════════════════════════════════╝
    """)

if __name__ == '__main__':
    main()
