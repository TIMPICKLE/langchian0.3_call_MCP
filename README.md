# Langchain + MCP 集成项目

## 🎯 项目简介

这是一个展示如何将 **Langchain 0.3** 与 **Model Context Protocol (MCP)** 集成的完整项目。项目实现了符合 MCP 标准的 JSON-RPC 2.0 协议，让 AI 代理能够通过标准化协议调用外部工具。

## ✨ 核心特性

### 🔧 MCP 协议标准实现
- ✅ **JSON-RPC 2.0 协议**：完全符合 MCP 标准
- ✅ **Client-Server 架构**：清晰的角色分离
- ✅ **工具发现机制**：动态获取可用工具列表
- ✅ **标准化通信**：规范的请求/响应格式
- ✅ **错误处理**：标准化的错误码和消息

### 🤖 AI 模型集成
- ✅ **自定义 LLM 支持**：使用现有 API 接口
- ✅ **Langchain 集成**：完整的代理工作流
- ✅ **工具调用**：AI 模型自动选择和调用工具
- ✅ **对话管理**：支持多轮对话和上下文保持

### 🛠️ 内置工具集
- ✅ **文件操作**：读取和写入文件
- ✅ **数学计算**：执行数学表达式计算
- ✅ **时间工具**：获取当前系统时间
- ✅ **可扩展**：易于添加新工具

## 📁 项目结构

```
Langchain-MCP/
├── src/
│   ├── mcp_server.py           # MCP 服务器实现
│   ├── mcp_client.py           # MCP 客户端实现
│   ├── langchain_client.py     # Langchain 集成
│   ├── config.py               # 配置管理
│   └── main.py                 # 主入口
├── examples/                   # 示例代码
├── docs/                       # 文档
├── workspace/                  # 工作目录
├── test_mcp.py                 # MCP 协议测试
├── requirements.txt            # 依赖包
└── README.md                   # 项目说明
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd Langchain-MCP

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置设置

编辑 `src/config.py` 中的 API 配置：

```python
class Config:
    def __init__(self):
        # API 配置
        self.api_base_url = "http://xx.xx.xx.xxx:xxxx/v1"  # 你的 API 地址
        self.api_key = "your-api-key-here"                # 你的 API 密钥
        self.model_name = "DeepSeek-V3-0324-HSW"          # 模型名称
```

### 3. 运行测试

```bash
# 测试 MCP 协议
python test_mcp.py

# 测试 Langchain 集成
python src/langchain_client.py

# 运行主程序
python src/main.py
```

## 🧪 测试说明

### MCP 协议测试
```bash
python test_mcp.py
```
这将测试：
- MCP 服务器初始化
- 客户端连接和握手
- 工具发现机制
- 工具调用和响应

### Langchain 集成测试
```bash
python src/langchain_client.py
```
这将测试：
- AI 模型与 MCP 的集成
- 自动工具选择和调用
- 多轮对话处理

## 📚 详细说明

### MCP 协议实现

#### 1. 服务器端 (`src/mcp_server.py`)
```python
# 创建 MCP 服务器
server = MCPServer()

# 处理客户端请求
response = await server.handle_request(request)
```

#### 2. 客户端 (`src/mcp_client.py`)
```python
# 创建 MCP 客户端
client = MCPClient(server=server)

# 初始化连接
await client.initialize()

# 调用工具
result = await client.call_tool("tool_name", {"param": "value"})
```

#### 3. Langchain 集成 (`src/langchain_client.py`)
```python
# 创建集成客户端
mcp_client = MCPLangchainClient()

# 初始化
await mcp_client.initialize()

# 处理用户消息
result = await mcp_client.chat("帮我计算 10 + 5 * 2")
```

### JSON-RPC 协议格式

#### 请求格式
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "calculate",
    "arguments": {
      "expression": "10 + 5 * 2"
    }
  }
}
```

#### 响应格式
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"result\": 20}"
      }
    ],
    "isError": false
  },
  "error": null
}
```

## 🛠️ 扩展开发

### 添加新工具

1. 在 `MCPServer` 类中注册新工具：
```python
# 定义工具函数
async def my_custom_tool(param1: str, param2: int):
    # 工具逻辑
    return {"result": "success"}

# 注册工具
server.register_tool(
    name="my_tool",
    description="我的自定义工具",
    function=my_custom_tool,
    parameters={
        "param1": {"type": "string", "description": "参数1"},
        "param2": {"type": "integer", "description": "参数2"}
    }
)
```

### 自定义 LLM

修改 `src/langchain_client.py` 中的 `CustomLLM` 类以支持你的 API：

```python
class CustomLLM(LLM):
    def __init__(self):
        self.api_url = "your-api-url"
        self.headers = {"Authorization": "Bearer your-token"}
    
    def _call(self, prompt: str, **kwargs) -> str:
        # 实现你的 API 调用逻辑
        pass
```

## 🔧 配置选项

### API 配置
- `api_base_url`: API 基础地址
- `api_key`: API 认证密钥
- `model_name`: 使用的模型名称
- `max_tokens`: 最大 token 数量
- `temperature`: 生成温度

### MCP 配置
- `protocol_version`: MCP 协议版本 (默认: "2024-11-05")
- `client_name`: 客户端名称
- `server_capabilities`: 服务器能力声明

## 📖 学习资源

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [JSON-RPC 2.0 规范](https://www.jsonrpc.org/specification)
- [Langchain 文档](https://langchain.readthedocs.io/)

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## ❓ 常见问题

### Q: 如何更换不同的 LLM？
A: 修改 `src/config.py` 中的 API 配置，或者继承 `CustomLLM` 类实现你的模型接口。

### Q: 如何添加更多工具？
A: 在 `MCPServer` 类中使用 `register_tool` 方法注册新工具，参考现有工具的实现。

### Q: 如何部署到生产环境？
A: 修改客户端连接方式，使用真正的网络连接替代本地服务器实例。

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和社区成员！
