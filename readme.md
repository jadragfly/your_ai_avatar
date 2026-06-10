# 3D 虚拟形象生成使用技能

本文档介绍如何使用 `.trae\skills\ai-avatar-generator` 技能快速创建一个基于 3D VRM 虚拟形象的 AI 聊天网页项目。

---

## 目录

1. [技能简介](#技能简介)
2. [功能特性](#功能特性)
3. [AI 后端选项](#ai-后端选项)
4. [快速开始](#快速开始)
5. [配置说明](#配置说明)
6. [项目结构](#项目结构)
7. [运行指南](#运行指南)
8. [API 接口](#api-接口)
9. [功能演示](#功能演示)
10. [常见问题](#常见问题)

---

## 技能简介

`ai-avatar-generator` 是一个 Trae AI 技能，用于一键生成完整的 3D VRM 虚拟形象 AI 聊天网页项目。

**技能位置**: `.trae\skills\ai-avatar-generator`

**核心能力**:
- 自动创建包含前端和后端的完整项目
- 支持多种 AI 后端（豆包/TBOX/Ollama）
- 内置 VRM 模型文件，无需额外下载
- 包含丰富的 3D 交互功能

---

## 功能特性

### 3D 渲染
- Three.js 实现的 3D VRM 模型加载和渲染
- 可调整的相机视角（FOV 30，参考 ai-avatar-web 的清晰设置）
- 优化的灯光配置（0.5 环境光 + 1.5 主光源 + 0.3 补光）

### 表情系统
- 9 种表情按钮：😊😠😢😌😲👁👈👉😐
- **睁眼作为默认待机表情**（neutral 表情）
- 自动眨眼系统（每 3-6 秒随机眨眼一次）
- 说话时自动关闭眨眼

### 视线追踪
- 眼睛跟随鼠标移动
- 平滑的视线过渡动画
- 说话时视线追踪暂停

### 唇形同步
- 说话时口型动画
- 平滑的唇形过渡

### 待机动画
- 微弱的呼吸效果（位置上下浮动）
- 头部轻微晃动

### 聊天功能
- 多轮对话支持
- 实时思考状态显示
- 语音气泡显示 AI 回复
- 快捷功能按钮（讲笑话、唱歌、跳舞、夸奖）

### 特效背景（可选）
- 渐变球形幕布
- 闪烁星星粒子
- 浮动光点
- 光晕环效果

---

## AI 后端选项

技能支持三种 AI 后端：

| 后端 | API 提供商 | 默认模型 | 环境变量 | 说明 |
|------|-----------|---------|---------|------|
| **豆包** | 火山引擎 | doubao-seed-1-6-251015 | `DOUBAO_API_KEY` | 推荐国内使用 |
| **TBOX** | ModelScope | Qwen/Qwen3-235B-A22B-Instruct-2507 | `MODELSCOPE_API_KEY` | 需要申请 |
| **Ollama** | 本地模型 | qwen3:4b | 无需 API Key | 需要本地安装 |

### 豆包配置示例

```bash
# 设置环境变量
export DOUBAO_API_KEY=your_api_key_here
export DOUBAO_API_URL=https://ark.cn-beijing.volces.com/api/v3
export DOUBAO_MODEL=doubao-seed-1-6-251015
```

### TBOX 配置示例

```bash
# 设置环境变量
export MODELSCOPE_API_KEY=your_api_key_here
export MODELSCOPE_BASE_URL=https://api-inference.modelscope.cn
```

### Ollama 配置示例

```bash
# 确保 Ollama 服务运行中
ollama serve

# 设置环境变量
export OLLAMA_MODEL=qwen3:4b
```

---

## 快速开始

### 方式一：使用 AI 对话创建

告诉 AI：
> "用 ai-avatar-generator 技能创建一个 AI 虚拟形象聊天项目"

AI 会引导你选择后端并自动创建项目。

### 方式二：手动创建

1. 创建项目目录
2. 复制技能模板文件
3. 安装依赖
4. 启动服务

```bash
# 1. 创建项目目录
mkdir my-avatar-project
cd my-avatar-project

# 2. 复制模板文件（从技能目录）
# templates/index.html      -> 前端页面
# templates/server_*.py     -> 后端服务
# templates/requirements.txt -> Python 依赖
# templates/sample.vrm      -> VRM 模型

# 3. 安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 4. 设置环境变量并启动后端
export DOUBAO_API_KEY=your_key
python server.py

# 5. 新开终端，启动前端
python -m http.server 8080

# 6. 打开浏览器访问
# http://localhost:8080
```

---

## 配置说明

### 技能模板文件说明

```
.trae\skills\ai-avatar-generator\templates\
├── index.html           # 前端页面模板
├── server_doubao.py     # 豆包后端模板
├── server_tbox.py       # TBOX 后端模板
├── server_ollama.py     # Ollama 后端模板
├── requirements.txt      # Python 依赖
├── sample.vrm           # VRM 模型文件（已包含）
└── generator.py         # 项目生成脚本
```

### 前端配置（index.html）

```javascript
const CONFIG = {
    API_URL: 'http://localhost:5000',  // 后端地址
    API_PATH: '/api/chat',              // 聊天接口路径
    MODEL: 'doubao-seed-1-6-251015',    // 模型名称
    DEBUG: false                         // 调试模式
};
```

### 后端配置（server_*.py）

```python
# 豆包 API 配置
DOUBAO_API_KEY = os.environ.get('DOUBAO_API_KEY', '')
DOUBAO_API_URL = os.environ.get('DOUBAO_API_URL', 'https://ark.cn-beijing.volces.com/api/v3')
MODEL = os.environ.get('DOUBAO_MODEL', 'doubao-seed-1-6-251015')

# Flask 应用
app = Flask(__name__)
CORS(app)  # 处理跨域
```

### 渲染配置（已优化）

技能模板使用与 ai-avatar-web 相同的渲染配置，确保模型显示清晰：

```javascript
// 相机配置
const camera = new THREE.PerspectiveCamera(
    30,  // FOV 30（更小的视角 = 更清晰的模型）
    container.clientWidth / container.clientHeight,
    0.1,
    1000
);

// 灯光配置
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);      // 环境光 0.5
const directionalLight = new THREE.DirectionalLight(0xffffff, 1.5); // 主光 1.5
const fillLight = new THREE.DirectionalLight(0x8888ff, 0.3);     // 补光
```

---

## 项目结构

生成的 `ai_avatar_web_test3` 项目结构：

```
ai_avatar_web_test3/
├── index.html          # 主页面（所有前端代码）
├── server.py           # Flask 后端服务
├── requirements.txt    # Python 依赖
├── sample.vrm          # VRM 模型文件
└── ...

# 运行后：
# 后端服务: http://localhost:5002
# 前端页面: http://localhost:8084/index.html
```

---

## 运行指南

### 启动后端服务

```bash
# 进入项目目录
cd ai_avatar_web_test3

# 设置环境变量（以豆包为例）
export DOUBAO_API_KEY=your_api_key

# 启动后端（端口 5002）
python server.py
```

后端启动日志：
```
[Server] ==================================================
[Server] AI Avatar 后端服务 (豆包版本)
[Server] ==================================================
[Server] 模型: doubao-seed-1-6-251015
[Server] API 地址: https://ark.cn-beijing.volces.com/api/v3
[Server] 服务地址: http://localhost:5002
[Server] ==================================================
```

### 启动前端服务

```bash
# 新开终端，进入项目目录
cd ai_avatar_web_test3

# 启动 HTTP 服务器（端口 8084）
python -m http.server 8084
```

### 访问页面

打开浏览器访问：
```
http://localhost:8084/index.html
```

---

## API 接口

### POST /api/chat

聊天接口，代理到 AI 后端。

**请求**:
```json
{
    "model": "doubao-seed-1-6-251015",
    "messages": [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！有什么可以帮助你的吗？"}
    ],
    "temperature": 0.7,
    "max_tokens": 2048
}
```

**响应**:
```json
{
    "choices": [{
        "message": {
            "content": "你好！很高兴为你服务！",
            "role": "assistant"
        },
        "finish_reason": "stop"
    }],
    "model": "doubao-seed-1-6-251015"
}
```

### GET /api/config

获取前端配置。

**响应**:
```json
{
    "model": "doubao-seed-1-6-251015",
    "api_url": "http://localhost:5002",
    "api_path": "/api/chat"
}
```

### GET /health

健康检查。

**响应**:
```json
{
    "status": "ok",
    "service": "ai-avatar-backend",
    "model": "doubao-seed-1-6-251015",
    "backend": "doubao"
}
```

---

## 功能演示

### 表情按钮

页面底部有 9 个表情按钮：

| 按钮 | 表情 | 描述 |
|------|------|------|
| 😊 | happy | 开心 |
| 😠 | angry | 生气 |
| 😢 | sad | 伤心 |
| 😌 | relaxed | 放松 |
| 😲 | surprised | 惊讶 |
| 👁 | blink | 眨眼 |
| 👈 | blinkLeft | 左眼眨 |
| 👉 | blinkRight | 右眼眨 |
| 😐 | neutral | 中性（睁眼待机）|

点击任意表情按钮，角色会显示对应表情，2 秒后恢复睁眼的待机状态。

### 快捷功能

| 按钮 | 功能 |
|------|------|
| 讲笑话 | 让 AI 讲一个笑话 |
| 唱首歌 | 让 AI 唱一首简单的歌 |
| 跳舞 | 让 AI 描述一段舞蹈动作 |
| 夸奖 | 让 AI 夸奖你 |

### 调试模式

在聊天框输入 `/debug on` 可开启调试模式，会显示：
- 控制台日志面板
- 内部状态信息
- API 请求/响应详情

---

## 常见问题

### 1. 模型显示模糊

**原因**: 相机 FOV 或灯光配置不当

**解决**: 技能模板已修复，使用 FOV 30 和优化的灯光配置

### 2. 表情按钮无反应

**原因**: ES 模块作用域导致函数未暴露到全局

**解决**: 技能模板已修复，通过 `window.playExpression = playExpression` 暴露函数

### 3. API 请求 404

**原因**: API URL 缺少 `/api/v3` 路径

**解决**: 技能模板已添加自动修正逻辑，确保 URL 以 `/api/v3` 结尾

### 4. VRM 模型加载失败

**解决**:
- 确保 `sample.vrm` 文件存在于项目目录
- 检查浏览器控制台的网络请求
- 技能模板已内置 VRM 文件

### 5. 豆包 API 错误

| 错误码 | 原因 | 解决 |
|--------|------|------|
| 401 | API Key 错误 | 检查 `DOUBAO_API_KEY` |
| 403 | 权限不足 | 检查 API Key 配额 |
| 404 | URL 错误 | 检查 `DOUBAO_API_URL` 是否包含 `/api/v3` |
| 500 | 服务器错误 | 检查网络或稍后重试 |

---

## 技能更新日志

### 2026-06-10 最新修复

- ✅ FOV 调整为 30（更清晰的模型）
- ✅ 灯光配置优化（0.5 环境光 + 1.5 主光）
- ✅ 添加 `initIdleExpression` 函数，睁眼作为默认待机表情
- ✅ 修复 `playExpression` 恢复逻辑
- ✅ 全局函数正确暴露到 window 对象
- ✅ API URL 自动修正确保包含 `/api/v3`
- ✅ VRM 模型文件已内置于模板

---

## 获取帮助

- 技能位置: `.trae\skills\ai-avatar-generator`
- 参考项目: `d:\impotent\interesting\vrm\ai-avatar-web`
- 测试项目: `d:\impotent\interesting\vrm\ai_avatar_web_test3`

---

*本文档由 AI 生成，如有疑问请检查技能模板源码。*
