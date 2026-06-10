# -*- coding: utf-8 -*-
"""
下载示例 VRM 模型
使用 three-vrm 官方示例模型
"""

import os
import requests

# VRM 模型 URL (three-vrm 官方示例)
VRM_URL = "https://pixiv.github.io/three-vrm/packages/three-vrm/examples/models/VRM1_Constraint_Twist_Sample.vrm"

def download_vrm():
    """下载示例 VRM 模型"""
    output_path = "sample.vrm"

    if os.path.exists(output_path):
        print(f'[Info] {output_path} 已存在，跳过下载')
        return True

    print(f'[Download] 开始下载 VRM 模型...')
    print(f'[URL] {VRM_URL}')

    try:
        response = requests.get(VRM_URL, stream=True, timeout=60)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        print(f'[Info] 文件大小: {total_size / 1024 / 1024:.2f} MB')

        downloaded = 0
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f'\r[Progress] {progress:.1f}%', end='', flush=True)

        print(f'\n[Success] VRM 模型已保存到 {output_path}')
        return True

    except requests.exceptions.RequestException as e:
        print(f'\n[Error] 下载失败: {e}')
        return False

if __name__ == '__main__':
    download_vrm()
