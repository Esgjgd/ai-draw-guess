# 项目知识库

**生成时间：** 2026-03-08

## 概览
AI 你画我猜游戏：玩家在画布上绘画，后端将笔迹转换为文本并发送给 AI 进行猜测。

## 结构
```
./
├── app/                    # 主要应用程序包
├── tests/                  # 单元测试
├── .github/workflows/      # CI 流水线
├── Dockerfile              # Docker 镜像构建文件
├── docker-compose.yml      # Docker Compose 配置
├── .dockerignore           # Docker 构建忽略文件
├── pyproject.toml          # 项目配置 (Ruff, Pytest)
├── requirements.txt        # 生产依赖项
├── requirements-dev.txt    # 开发依赖项
└── README.md               # 文档
```

## 查找位置
| 任务 | 位置 | 备注 |
|------|----------|-------|
| API 端点 | app/main.py | FastAPI 路由 |
| AI 客户端 | app/ai_client.py | HTTPX 调用百山 API |
| 提示构建 | app/prompt_builder.py | 将笔迹转换为文本 |
| 配置 | app/config.py | 环境变量 |
| 前端 | app/templates/index.html | 画布绘制 UI |
| 数据模型 | app/schemas.py | Pydantic 模型 |
| 测试 | tests/test_prompt_builder.py | 单元测试 |
| CI | .github/workflows/ci.yml | Ruff + Pytest |
| Docker | Dockerfile, docker-compose.yml | 容器化配置 |

## 命令

### 开发环境
```bash
# 使用 uv 安装依赖
uv venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows
uv pip install -r requirements.txt -r requirements-dev.txt

# 启动开发服务器
uvicorn app.main:app --reload

# 使用 Docker 启动
docker-compose up -d
docker-compose logs -f  # 查看日志
docker-compose down     # 停止服务
```

### 测试
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_prompt_builder.py

# 运行单个测试
pytest tests/test_prompt_builder.py::test_build_guess_prompt_contains_counts

# 带覆盖率测试
pytest --cov=app --cov-report=html

# 调试模式运行测试
pytest -v -s tests/test_prompt_builder.py
```

### 代码检查和格式化
```bash
# 检查代码（不修复）
ruff check .

# 自动修复可修复的问题
ruff check . --fix

# 格式化代码
ruff format .

# 检查类型（如果配置了 mypy）
mypy app/
```

### Docker 操作
```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重新构建并启动
docker-compose up -d --build
```

## 代码风格指南

### 导入
- 每个文件以 `from __future__ import annotations` 开头
- 分组导入：标准库、三方库、本地 (app.)
- 在 app 包内使用绝对导入 (例如 `from app.config import get_settings`)
- 避免通配符导入 (`from module import *`)
- 使用 isort 自动排序导入（由 Ruff 处理）

### 命名约定
- **函数/方法**：snake_case (例如 `build_guess_prompt`, `get_settings`)
- **变量**：snake_case (例如 `stroke_count`, `payload`)
- **类**：PascalCase (例如 `BaishanAIClient`, `GuessRequest`)
- **常量**：UPPER_CASE (暂无)
- **模块**：snake_case (例如 `ai_client.py`)
- **私有方法/属性**：以下划线开头 (例如 `_settings`, `_build_payload`)

### 格式化
- 行长度：100 个字符
- 由 Ruff 强制执行，规则 E (pycodestyle), F (Pyflakes), I (isort), B (flake8-bugbear)
- 使用 4 个空格缩进
- 多行结构中使用尾随逗号
- 字符串使用双引号，除非字符串包含双引号

### 类型提示
- 始终为函数参数和返回值使用类型提示
- 使用泛型 (例如 `list[StrokePoint]`, `dict[str, Any]`)
- 在 dataclass 和 Pydantic 模型中注释类属性
- 利用 `from __future__ import annotations` 进行前向引用
- 对可选参数使用 `Optional` 或联合类型 (例如 `str | None`)

### 错误处理
- 尽可能捕获特定异常 (例如 `RuntimeError`, `ValueError`, `HTTPStatusError`)
- 使用 `raise ... from exc` 进行异常链式传递以保留堆栈跟踪
- 在 FastAPI 路由中，引发带有适当状态码的 `HTTPException`
- 为难以测试的错误分支添加 `# pragma: no cover`
- 使用日志记录错误，不要只打印到控制台

### 异步编程
- 对 I/O 操作使用 `async`/`await` (HTTP 调用，文件读取)
- 所有 FastAPI 路由处理器都是异步的
- 对 HTTP 请求使用 `httpx.AsyncClient`
- 在测试中使用 `pytest-asyncio` 和 `pytest.mark.asyncio`

### 日志记录
- 使用 `logging` 模块进行日志记录
- 在每个模块中创建 logger: `logger = logging.getLogger(__name__)`
- 使用适当的日志级别：DEBUG, INFO, WARNING, ERROR
- 为生产部署配置合适的日志格式和级别

### API 设计
- 使用 RESTful 约定
- 返回一致的 JSON 响应格式
- 使用 HTTP 状态码正确表示操作结果
- 在响应中使用 snake_case 字段名
- 为所有端点编写 OpenAPI 文档

### 配置管理
- 使用环境变量进行配置
- 在 `app/config.py` 中定义所有配置
- 使用 `pydantic.BaseSettings` 或 `@dataclass(frozen=True)` 定义配置类
- 为敏感信息（如 API 密钥）提供安全的处理方式

### 测试实践
- 使用 pytest 进行单元测试
- 在 pyproject.toml 中配置异步模式为 "auto"
- 编写描述性测试函数名 (例如 `test_build_guess_prompt_contains_counts`)
- 使用带有清晰失败消息的断言
- 测试异常情况和边界条件
- 使用 fixtures 复用测试设置

### 安全考虑
- 验证所有用户输入
- 使用 HTTPS 进行生产部署
- 不要在日志中记录敏感信息
- 实施适当的速率限制
- 验证 API 密钥的有效性

## 约定

### 项目结构
- 保持 `app/` 目录整洁，按功能分组模块
- 测试文件与源文件保持相同结构 (`tests/test_*.py`)
- 使用 `__init__.py` 文件定义包

### 版本控制
- 使用语义化版本控制
- 提交信息使用英文，遵循约定式提交格式
- 保持提交原子性（每个提交一个逻辑更改）

### 性能优化
- 使用异步操作处理并发请求
- 缓存频繁访问的数据
- 监控内存使用和响应时间
- 使用连接池进行外部 API 调用

## 反模式 (避免)

- 不要在 FastAPI 路由中使用阻塞操作
- 不要直接在代码中硬编码配置值
- 不要忽略异常或使用空的 except 块
- 不要在生产代码中保留调试 print 语句
- 不要创建过大的函数或类

## 独特风格

- 直接 HTTP 调用 AI API (无 SDK)
- 在 FastAPI 中嵌入 HTML 模板
- 中文界面和提示文本
- 使用百山 AI API 进行绘画猜测
- 简化的前端实现（仅基础画布功能）

## 备注

- 健康检查端点：`GET /api/health`
- 猜测 API 端点：`POST /api/guess`
- 前端界面：`GET /`
- API 文档：`GET /docs` (自动生成)

## Docker 部署说明

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