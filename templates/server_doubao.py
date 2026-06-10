# -*- coding: utf-8 -*-
"""
Flask 后端服务 - 豆包版本
提供豆包(火山引擎) API 代理，解决前端 CORS 问题
"""

import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# ==================== 配置 ====================
DEBUG = os.environ.get('DEBUG', 'true').lower() == 'true'

# 豆包 API 配置
DOUBAO_API_KEY = os.environ.get('DOUBAO_API_KEY', '')
# 确保 API URL 以 /api/v3 结尾
_raw_url = os.environ.get('DOUBAO_API_URL', 'https://ark.cn-beijing.volces.com/api/v3')
if not _raw_url.endswith('/api/v3'):
    _raw_url = _raw_url.rstrip('/') + '/api/v3'
DOUBAO_API_URL = _raw_url
MODEL = os.environ.get('DOUBAO_MODEL', 'doubao-seed-1-6-251015')

# Flask 应用
app = Flask(__name__)
CORS(app)

# ==================== 调试日志 ====================
def log(*args):
    """调试日志输出"""
    if DEBUG:
        print('[Server]', *args)

def log_error(*args):
    """错误日志输出"""
    print('[Error]', *args)

# ==================== API 路由 ====================

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'service': 'ai-avatar-backend',
        'model': MODEL,
        'backend': 'doubao'
    })

@app.route('/api/config', methods=['GET'])
def get_config():
    """获取前端配置"""
    return jsonify({
        'model': MODEL,
        'api_url': f'http://localhost:5000',
        'api_path': '/api/chat'
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    聊天接口 - 代理豆包 API
    """
    try:
        # 获取请求数据
        data = request.get_json()
        messages = data.get('messages', [])
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 2048)

        # 检查 API Key
        if not DOUBAO_API_KEY:
            return jsonify({
                'error': 'DOUBAO_API_KEY 未设置'
            }), 500

        # 构建请求头
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {DOUBAO_API_KEY}'
        }

        # 构建请求体 - 豆包格式
        payload = {
            'model': MODEL,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': max_tokens
        }

        log(f'发送请求到 {DOUBAO_API_URL}/chat/completions')
        log(f'模型: {MODEL}')
        log(f'消息数: {len(messages)}')

        # 发送请求
        response = requests.post(
            f'{DOUBAO_API_URL}/chat/completions',
            headers=headers,
            json=payload,
            timeout=120
        )

        if response.status_code == 200:
            result = response.json()

            # 转换为 OpenAI 兼容格式
            openai_response = {
                'choices': [{
                    'message': {
                        'role': 'assistant',
                        'content': result.get('choices', [{}])[0].get('message', {}).get('content', '')
                    },
                    'finish_reason': result.get('choices', [{}])[0].get('finish_reason', 'stop')
                }],
                'model': MODEL
            }

            log('API 请求成功')
            return jsonify(openai_response)
        else:
            log_error(f'API 请求失败: {response.status_code}')
            log_error(f'响应内容长度: {len(response.content)} bytes')
            return jsonify({
                'error': f'API 请求失败: {response.status_code}',
                'details': response.text[:500]
            }), response.status_code

    except requests.exceptions.Timeout:
        log_error('API 请求超时')
        return jsonify({'error': 'API 请求超时，请稍后重试'}), 504

    except requests.exceptions.RequestException as e:
        log_error(f'API 请求异常: {e}')
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

    except Exception as e:
        log_error(f'未知错误: {e}')
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

# ==================== 启动服务器 ====================

if __name__ == '__main__':
    log('=' * 50)
    log('AI Avatar 后端服务 (豆包版本)')
    log('=' * 50)
    log(f'模型: {MODEL}')
    log(f'API 地址: {DOUBAO_API_URL}')
    log(f'调试模式: {DEBUG}')
    log('=' * 50)
    log('提示: 请设置环境变量 DOUBAO_API_KEY')
    log('服务地址: http://localhost:5000')
    log('=' * 50)

    app.run(host='0.0.0.0', port=5000, debug=DEBUG)
