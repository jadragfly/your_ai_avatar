---
name: "ai-avatar-generator"
description: "生成 3D VRM 虚拟形象 AI 聊天网页。支持豆包/TBOX/Ollama 模型，自动创建完整工程。Invoke when user wants to create an AI avatar chat web project or asks for VRM/3D character chat."
---

# AI Avatar Generator

Generate a complete 3D VRM virtual avatar AI chat web project with one click.

## When to Use

- User wants to create an AI avatar chat web project
- User asks for "VRM chat", "3D character chat", "AI virtual avatar"
- User wants to create a web page with 3D character that can chat
- User wants to add an AI chatbot with 3D character to their project

## AI Backend Options

| Backend | API | Model | Requires |
|---------|-----|-------|----------|
| **豆包** | 火山引擎 | doubao-seed-1-6-251015 | DOUBAO_API_KEY |
| **TBOX** | ModelScope | Qwen/Qwen3-235B-A22B-Instruct-2507 | MODELSCOPE_API_KEY |
| **Ollama** | 本地 | qwen3:4b | Ollama 服务运行中 |

## Execution Flow

### Step 1: Ask User for Configuration

Ask user to choose AI backend:

```
请选择 AI 后端:
1. 豆包 (火山引擎) - 需要 API Key
2. TBOX (百灵大模型) - 需要 ModelScope API Key
3. Ollama (本地模型) - 需要选择已安装的模型

请回复选项编号，或直接提供配置信息。
```

### Step 2: Collect Configuration

**For 豆包**:
- Ask for API Key (or read from environment `DOUBAO_API_KEY`)
- Default model: `doubao-seed-1-6-251015`
- API URL: `https://ark.cn-beijing.volces.com/api/v3`

**For TBOX**:
- Ask for API Key (or read from environment `MODELSCOPE_API_KEY`)
- Default model: `Qwen/Qwen3-235B-A22B-Instruct-2507`
- API URL: `https://api-inference.modelscope.cn`

**For Ollama**:
- Check available models: `curl http://localhost:11434/api/tags`
- Default model: `qwen3:4b` (if installed)
- Ask user to confirm or select another model

### Step 3: Create Project Directory

```bash
mkdir ai-avatar-web
cd ai-avatar-web
```

### Step 4: Generate Project Files

Copy templates from skill directory:
```
SKILL_DIR/templates/
├── index.html           # Frontend template
├── server_doubao.py     # Backend for 豆包
├── server_tbox.py       # Backend for TBOX
├── server_ollama.py     # Backend for Ollama
├── requirements.txt      # Python dependencies
├── download_vrm.py       # VRM model downloader
└── generator.py         # Generator script
```

Replace placeholders in templates:
| Placeholder | 豆包 | TBOX | Ollama |
|-------------|------|------|--------|
| `{{API_URL}}` | `http://localhost:5000` | `http://localhost:5000` | `http://localhost:5000` |
| `{{API_PATH}}` | `/api/chat` | `/api/chat` | `/api/chat` |
| `{{MODEL}}` | `doubao-seed-1-6-251015` | `Qwen/Qwen3-235B-A22B-Instruct-2507` | `qwen3:4b` |
| `{{AI_MODEL_NAME}}` | `豆包大模型` | `百灵大模型` | `Qwen3` |

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Step 6: VRM Model

VRM model file (`sample.vrm`) is already included in the templates directory. No download needed.

## Generated Features

The generated project includes:

| Feature | Description |
|---------|-------------|
| **3D VRM Display** | Load and render VRM model with Three.js |
| **Expression Control** | 5 emotion buttons (😊😢😲😉👋) |
| **Auto Blink** | Random blink every 3-6 seconds |
| **Eye Tracking** | Eyes follow mouse movement |
| **Lip Sync** | Mouth animation while speaking |
| **Idle Animation** | Subtle breathing and head sway |
| **AI Chat** | Multi-turn conversation |
| **Speech Bubble** | Display AI responses |

## Project Structure

```
ai-avatar-web/
├── index.html          # Main page (all frontend code)
├── server.py           # Flask backend
├── requirements.txt    # Python dependencies
├── download_vrm.py     # VRM downloader
└── sample.vrm          # VRM model (downloaded)
```

## Run Instructions

### Start Backend (Port 5000)

**For 豆包**:
```bash
export DOUBAO_API_KEY=your_api_key
export DOUBAO_API_URL=https://ark.cn-beijing.volces.com/api/v3
export DOUBAO_MODEL=doubao-seed-1-6-251015
python server.py
```

**For TBOX**:
```bash
export MODELSCOPE_API_KEY=your_api_key
export MODELSCOPE_BASE_URL=https://api-inference.modelscope.cn
python server.py
```

**For Ollama**:
```bash
export OLLAMA_MODEL=qwen3:4b
python server.py
```

### Start Frontend (Port 8080)

```bash
python -m http.server 8080
```

### Access

Open browser: http://localhost:8080

## API Reference

### POST /api/chat

**Request**:
```json
{
    "model": "doubao-seed-1-6-251015",
    "messages": [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！"}
    ],
    "temperature": 0.7,
    "max_tokens": 2048
}
```

**Response**:
```json
{
    "choices": [{
        "message": {"content": "回复内容", "role": "assistant"}
    }]
}
```

### GET /api/config

Returns frontend configuration.

### GET /health

Health check endpoint.

## Debug Mode

Add `/debug on` command in chat to enable debug logging:
- Console logs visible
- Debug panel shows internal states
- API requests/responses logged

## Important Notes

1. **VRM Model**: Must be valid .vrm file
2. **豆包**: Get API key from [火山引擎控制台](https://console.volcengine.com/)
3. **TBOX**: Ensure API key has sufficient quota
4. **Ollama**: Must run `ollama serve` before starting backend
5. **Browser**: Must support ES6+ and WebGL
6. **CORS**: Handled by backend proxy

## Error Handling

| Error | Solution |
|-------|----------|
| VRM 404 | Check sample.vrm exists, try different path |
| API 401/403 | Check API key is correct |
| API 500 | Check network connection, API quota |
| Ollama Connection | Run `ollama serve` |
| WebGL not supported | Update browser or graphics drivers |
