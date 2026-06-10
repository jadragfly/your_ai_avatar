# -*- coding: utf-8 -*-
"""
Flask 后端服务 - Ollama 版本
提供本地 Ollama 模型 API 代理，解决前端 CORS 问题
"""

import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# ==================== 配置 ====================
DEBUG = os.environ.get('DEBUG', 'true').lower() == 'true'

# Ollama API 配置
OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'qwen3:4b')

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
        'model': OLLAMA_MODEL,
        'backend': 'ollama'
    })

@app.route('/api/config', methods=['GET'])
def get_config():
    """获取前端配置"""
    return jsonify({
        'model': OLLAMA_MODEL,
        'api_url': f'http://localhost:5000',
        'api_path': '/api/chat'
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    聊天接口 - 代理 Ollama API
    """
    try:
        # 获取请求数据
        data = request.get_json()
        messages = data.get('messages', [])
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 2048)

        # 构建 Ollama 请求格式
        # 提取最后一条用户消息作为 prompt
        user_prompt = ''
        for msg in reversed(messages):
            if msg.get('role') == 'user':
                user_prompt = msg.get('content', '')
                break

        # 构建消息历史 (Ollama 格式)
        ollama_messages = []
        for msg in messages[:-1]:  # 除了最后一条
            ollama_messages.append({
                'role': msg.get('role', 'user'),
                'content': msg.get('content', '')
            })

        log(f'发送请求到 {OLLAMA_BASE_URL}/api/chat')
        log(f'模型: {OLLAMA_MODEL}')
        log(f'消息数: {len(messages)}')

        # 构建 Ollama 请求体
        payload = {
            'model': OLLAMA_MODEL,
            'messages': ollama_messages if ollama_messages else [{'role': 'user', 'content': user_prompt}],
            'stream': False,
            'options': {
                'temperature': temperature,
                'num_predict': max_tokens
            }
        }

        # 发送请求到 Ollama
        response = requests.post(
            f'{OLLAMA_BASE_URL}/api/chat',
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
                        'content': result.get('message', {}).get('content', '')
                    },
                    'finish_reason': 'stop'
                }],
                'model': OLLAMA_MODEL
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
        return jsonify({'error': 'API 请求超时，请确保 Ollama 服务正在运行'}), 504

    except requests.exceptions.ConnectionError:
        log_error('无法连接到 Ollama 服务')
        return jsonify({'error': '无法连接到 Ollama 服务，请确保 Ollama 已启动 (ollama serve)'}), 503

    except requests.exceptions.RequestException as e:
        log_error(f'API 请求异常: {e}')
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

    except Exception as e:
        log_error(f'未知错误: {e}')
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

# ==================== 启动服务器 ====================

if __name__ == '__main__':
    log('=' * 50)
    log('AI Avatar 后端服务 (Ollama 版本)')
    log('=' * 50)
    log(f'模型: {OLLAMA_MODEL}')
    log(f'Ollama 地址: {OLLAMA_BASE_URL}')
    log(f'调试模式: {DEBUG}')
    log('=' * 50)
    log('提示: 请确保 Ollama 服务已启动 (ollama serve)')
    log('服务地址: http://localhost:5000')
    log('=' * 50)

    app.run(host='0.0.0.0', port=5000, debug=DEBUG)
