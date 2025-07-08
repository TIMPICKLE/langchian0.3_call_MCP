# Langchain 0.3 + MCP Server 详细教学手册

## 目录
1. [基础概念](#基础概念)
2. [环境搭建](#环境搭建)
3. [MCP Server 详解](#mcp-server-详解)
4. [Langchain 集成](#langchain-集成)
5. [实战示例](#实战示例)
6. [常见问题与解决方案](#常见问题与解决方案)

## 基础概念

### 什么是 Langchain？

Langchain 是一个用于构建基于大语言模型 (LLM) 应用程序的框架。它提供了：
- **链 (Chains)**: 将多个组件组合在一起的方式
- **代理 (Agents)**: 可以使用工具的 LLM
- **工具 (Tools)**: LLM 可以调用的函数
- **内存 (Memory)**: 在对话中保持状态

### 什么是 MCP (Model Context Protocol)？

MCP 是一个标准化协议，用于：
- 连接 AI 模型和外部数据源
- 提供安全的工具访问机制
- 标准化模型与环境的交互方式

### 核心组件关系图

```
用户输入 → Langchain Agent → MCP Server → 工具执行 → 结果返回 → LLM 处理 → 最终输出
```

## 环境搭建

### 第一步：检查 Python 环境

```bash
# 检查 Python 版本（需要 3.8+）
python --version

# 检查 pip 版本
pip --version
```

### 第二步：创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv langchain_mcp_env

# 激活虚拟环境 (Windows)
langchain_mcp_env\Scripts\activate

# 激活虚拟环境 (Linux/Mac)
source langchain_mcp_env/bin/activate
```

### 第三步：安装依赖包

```bash
pip install -r requirements.txt
```

### 第四步：配置环境变量

复制 `.env.example` 到 `.env` 并填入配置：

```env
# API 配置
API_BASE_URL=http://xx.xx.xx.xxx:xxxx/v1
MODEL_NAME=DeepSeek-V3-0324-HSW
API_TIMEOUT=30

# MCP Server 配置
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8080

# 日志配置
LOG_LEVEL=INFO
```

## MCP Server 详解

### MCP Server 的作用

MCP Server 是一个服务程序，它：
1. 提供标准化的工具接口
2. 管理工具的安全访问
3. 处理工具调用和结果返回

### 工具类型

我们的 MCP Server 提供三类工具：

#### 1. 文件操作工具
- `read_file`: 读取文件内容
- `write_file`: 写入文件内容
- `list_files`: 列出目录中的文件

#### 2. 计算工具
- `calculate`: 执行基础数学运算
- `get_random_number`: 生成随机数

#### 3. 时间工具
- `get_current_time`: 获取当前时间
- `format_time`: 格式化时间字符串

### MCP Server 代码解析

```python
# 这是一个简化的 MCP Server 结构示例
class MCPServer:
    def __init__(self):
        self.tools = {}  # 存储所有可用工具
        
    def register_tool(self, name, function, description):
        """注册一个新工具"""
        self.tools[name] = {
            'function': function,
            'description': description
        }
    
    def execute_tool(self, tool_name, parameters):
        """执行指定的工具"""
        if tool_name in self.tools:
            return self.tools[tool_name]['function'](**parameters)
        else:
            raise ValueError(f"工具 {tool_name} 不存在")
```

## Langchain 集成

### Agent 的工作原理

Langchain Agent 的工作流程：

1. **接收用户输入**
2. **分析需要什么工具**
3. **调用 MCP Server 工具**
4. **处理工具返回结果**
5. **生成最终回复**

### 关键代码解析

```python
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import Tool

# 创建工具列表
tools = [
    Tool(
        name="文件读取",
        description="读取指定文件的内容",
        func=mcp_client.read_file
    ),
    # ... 更多工具
]

# 创建 Agent
agent = create_openai_functions_agent(
    llm=llm,           # 语言模型
    tools=tools,       # 可用工具列表
    prompt=prompt      # 系统提示词
)

# 创建执行器
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True       # 显示详细执行过程
)
```

## 实战示例

### 示例 1：文件操作

```python
# 用户: "请帮我创建一个名为 hello.txt 的文件，内容是 'Hello World'"

# Agent 的思考过程：
# 1. 用户想要创建文件
# 2. 需要使用 write_file 工具
# 3. 参数：文件名="hello.txt", 内容="Hello World"

# 执行步骤：
result = agent_executor.invoke({
    "input": "请帮我创建一个名为 hello.txt 的文件，内容是 'Hello World'"
})
```

### 示例 2：数学计算

```python
# 用户: "请计算 (25 + 75) * 2 的结果"

# Agent 的思考过程：
# 1. 用户需要数学计算
# 2. 使用 calculate 工具
# 3. 参数：expression="(25 + 75) * 2"

result = agent_executor.invoke({
    "input": "请计算 (25 + 75) * 2 的结果"
})
```

### 示例 3：组合操作

```python
# 用户: "获取当前时间并保存到 time.txt 文件中"

# Agent 的思考过程：
# 1. 首先获取当前时间 (get_current_time)
# 2. 然后将时间写入文件 (write_file)

result = agent_executor.invoke({
    "input": "获取当前时间并保存到 time.txt 文件中"
})
```

## 代码执行流程

### 完整的执行流程

```
1. 用户输入问题
   ↓
2. Langchain Agent 分析问题
   ↓
3. Agent 决定需要哪些工具
   ↓
4. 调用 MCP Server 工具
   ↓
5. MCP Server 执行工具函数
   ↓
6. 返回执行结果
   ↓
7. Agent 处理结果并生成回复
   ↓
8. 返回最终答案给用户
```

### 错误处理流程

```
工具调用失败
   ↓
MCP Server 返回错误信息
   ↓
Agent 接收错误信息
   ↓
Agent 尝试其他方法或报告错误
   ↓
返回错误信息给用户
```

## 常见问题与解决方案

### Q1: 安装依赖时出现错误

**问题**: `pip install -r requirements.txt` 失败

**解决方案**:
```bash
# 升级 pip
python -m pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### Q2: MCP Server 启动失败

**问题**: 端口被占用

**解决方案**:
```bash
# 检查端口占用
netstat -ano | findstr :8080

# 更换端口（修改 .env 文件中的 MCP_SERVER_PORT）
```

### Q3: LLM API 调用失败

**问题**: 连接超时或认证失败

**解决方案**:
1. 检查网络连接
2. 验证 API 地址和端口
3. 确认 API 服务状态
4. 调整超时时间

### Q4: Agent 不使用工具

**问题**: Agent 直接回答而不调用工具

**解决方案**:
1. 检查工具描述是否清晰
2. 优化系统提示词
3. 确认模型支持函数调用

## 扩展开发

### 添加新工具

1. **在 MCP Server 中定义工具函数**:
```python
def new_tool_function(parameter1, parameter2):
    """新工具的实现"""
    # 工具逻辑
    return result
```

2. **注册工具**:
```python
server.register_tool(
    name="new_tool",
    function=new_tool_function,
    description="新工具的描述"
)
```

3. **在 Langchain 中添加工具**:
```python
Tool(
    name="新工具",
    description="新工具的描述",
    func=mcp_client.new_tool
)
```

### 自定义 Agent 行为

通过修改系统提示词来定制 Agent 行为：

```python
system_message = """
你是一个专业的助手，专门帮助用户处理文件和计算任务。

使用原则：
1. 优先使用可用的工具
2. 解释你的操作步骤
3. 确认操作结果
4. 提供有用的建议

可用工具：
- 文件操作：读取、写入、列出文件
- 计算工具：数学运算、随机数生成
- 时间工具：获取和格式化时间
"""
```

## 性能优化

### 1. 缓存机制
实现工具结果缓存，避免重复计算：

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_calculation(expression):
    return calculate(expression)
```

### 2. 异步处理
对于耗时操作，使用异步处理：

```python
import asyncio

async def async_file_operation(filename):
    # 异步文件操作
    pass
```

### 3. 连接池
使用连接池管理 API 连接：

```python
import requests
from requests.adapters import HTTPAdapter

session = requests.Session()
adapter = HTTPAdapter(pool_connections=10, pool_maxsize=20)
session.mount('http://', adapter)
```

## 总结

通过本教程，你已经学会了：

1. **基础概念**: 理解 Langchain 和 MCP 的作用
2. **环境搭建**: 正确配置开发环境
3. **代码理解**: 掌握核心代码的工作原理
4. **实战应用**: 运行和修改示例代码
5. **问题解决**: 处理常见的开发问题
6. **扩展开发**: 添加新功能和优化性能

继续学习建议：
- 尝试添加更多自定义工具
- 探索更复杂的工作流
- 学习更高级的 Langchain 功能
- 参与开源项目贡献代码

祝你在 AI 开发的道路上越走越远！
