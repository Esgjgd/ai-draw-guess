# AI 你画我猜 (AI Draw & Guess)

这是一个在线你画我猜游戏：玩家在画布上作画，后端会把绘画笔迹转成文字描述提示给 AI 模型进行猜测，并返回猜测结果。

## 功能

- 浏览器画板（支持清空、撤销不做，仅保留简单清空）
- 将笔迹数据发送到后端
- 后端调用[白山 AI API](https://ai.baishan.com/auth/login?referralCode=KX7YrYhDw5)进行猜测
- 基础健康检查接口

## 技术栈

- Python 3.10+
- FastAPI + Uvicorn
- HTTPX（直接调用 API）
- Pytest + Ruff

## 快速开始

### 方法一：使用 uv（推荐开发环境）

1. 安装 uv（如果尚未安装）

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. 创建虚拟环境并安装依赖

```bash
uv venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows
uv pip install -r requirements.txt -r requirements-dev.txt
```

3. 配置环境变量

复制 `.env.example` 并填写 API Key：

```bash
cp .env.example .env
```

示例：

```env
BAISHAN_API_KEY=你的API_KEY
BAISHAN_MODEL=DeepSeek-R1-0528
BAISHAN_BASE_URL=https://api.edgefn.net/v1
```

4. 启动服务

```bash
uvicorn app.main:app --reload
```

### 方法二：使用 Docker（推荐生产环境）

1. 确保安装了 Docker 和 Docker Compose

2. 配置环境变量

复制 `.env.example` 并填写 API Key：

```bash
cp .env.example .env
```

3. 启动服务

```bash
docker-compose up -d
```

4. 查看日志（可选）

```bash
docker-compose logs -f
```

### 访问应用

打开浏览器访问 `http://127.0.0.1:8000` 开始作画。

## API 说明

- `GET /api/health`：健康检查
- `POST /api/guess`：提交笔迹并获取 AI 猜测

## 调用方式

后端使用 **HTTP 直接调用** 百山 AI API：

- Base URL: `https://api.edgefn.net/v1`
- Endpoint: `POST /v1/chat/completions`
- Auth: `Authorization: Bearer YOUR_API_KEY`

参考文档：
- https://ai.baishan.com/docs/docs/llm-api.html

## Docker 部署

### 本地开发
```bash
# 克隆仓库
git clone <repository-url>
cd ai-draw-guess

# 复制环境变量文件
cp .env.example .env

# 编辑 .env 文件，设置 API 密钥
# BAISHAN_API_KEY=your_api_key_here

# 使用 Docker Compose 启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 生产部署
```bash
# 构建生产镜像
docker build -t ai-draw-guess:latest .

# 运行容器
docker run -d \
  --name ai-draw-guess \
  -p 8000:8000 \
  -e BAISHAN_API_KEY=your_api_key \
  ai-draw-guess:latest

# 或使用 docker-compose.prod.yml（如果存在）
docker-compose -f docker-compose.prod.yml up -d
```

## GitHub Actions

本项目包含 CI：

- Ruff 格式检查
- Pytest 单元测试

`.github/workflows/ci.yml`

---

如需上线或扩展多房间游戏逻辑，可增加 WebSocket 广播与多人房间管理。作为基础演示，该版本只实现单人画图与 AI 猜测。
