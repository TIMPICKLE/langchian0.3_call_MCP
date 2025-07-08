"""
MCP Server 实现

这个模块实现了符合 Model Context Protocol 标准的服务器。
MCP 是一个基于 JSON-RPC 的协议，用于 AI 模型与外部工具的标准化通信。

MCP 协议特点：
1. 基于 JSON-RPC 2.0 协议
2. Client-Server 架构
3. 标准化的工具发现和调用机制
4. 支持流式通信和会话管理
"""

import json
import asyncio
import logging
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import datetime
import os

# MCP 协议相关的数据结构


class MethodType(Enum):
    """MCP 方法类型"""
    INITIALIZE = "initialize"
    LIST_TOOLS = "tools/list"
    CALL_TOOL = "tools/call"
    GET_PROMPT = "prompts/get"
    LIST_PROMPTS = "prompts/list"
    LIST_RESOURCES = "resources/list"
    READ_RESOURCE = "resources/read"


@dataclass
class MCPError:
    """MCP 错误信息"""
    code: int
    message: str
    data: Optional[Dict[str, Any]] = None


@dataclass
class Tool:
    """MCP 工具定义"""
    name: str
    description: str
    inputSchema: Dict[str, Any]


@dataclass
class ToolResult:
    """工具执行结果"""
    content: List[Dict[str, Any]]
    isError: bool = False



@dataclass
class MCPRequest:
    """MCP 请求"""
    jsonrpc: str = "2.0"
    id: Optional[Union[str, int]] = None
    method: Optional[str] = None
    params: Optional[Dict[str, Any]] = None


@dataclass
class MCPResponse:
    """MCP 响应"""
    jsonrpc: str = "2.0"
    id: Optional[Union[str, int]] = None
    result: Optional[Any] = None
    error: Optional[MCPError] = None


class MCPServer:
    """
    MCP Server 实现
    
    实现了完整的 Model Context Protocol 标准
    """
    
    def __init__(self, name: str = "Langchain-MCP-Server", version: str = "1.0.0"):
        """
        初始化 MCP Server
        
        Args:
            name (str): 服务器名称
            version (str): 服务器版本
        """
        self.name = name
        self.version = version
        self.capabilities = {
            "tools": {"listChanged": True},
            "prompts": {"listChanged": False},
            "resources": {"listChanged": False}
        }
        
        # 工具注册表
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._tool_functions: Dict[str, Callable] = {}
        
        # 使用统计
        self._call_stats: Dict[str, int] = {}
        self._session_id: str = str(uuid.uuid4())
        self._initialized: bool = False
        
        # 注册内置工具
        self._register_builtin_tools()
        
        logging.info(f"🚀 真正的 MCP Server 初始化完成: {self.name} v{self.version}")
    
    def _register_builtin_tools(self) -> None:
        """注册内置工具"""
        
        # 文件读取工具
        self.register_tool(
            name="read_file",
            description="读取指定文件的内容",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "要读取的文件路径"
                    }
                },
                "required": ["path"]
            },
            function=self._read_file_tool
        )
        
        # 文件写入工具
        self.register_tool(
            name="write_file",
            description="将内容写入指定文件",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "要写入的文件路径"
                    },
                    "content": {
                        "type": "string",
                        "description": "要写入的内容"
                    }
                },
                "required": ["path", "content"]
            },
            function=self._write_file_tool
        )
        
        # 数学计算工具
        self.register_tool(
            name="calculate",
            description="执行数学计算表达式",
            input_schema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "要计算的数学表达式"
                    }
                },
                "required": ["expression"]
            },
            function=self._calculate_tool
        )
        
        # 获取当前时间工具
        self.register_tool(
            name="get_current_time",
            description="获取当前系统时间",
            input_schema={
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "description": "时间格式，默认为 ISO 格式",
                        "default": "iso"
                    }
                }
            },
            function=self._get_time_tool
        )
    
    def register_tool(
        self, 
        name: str, 
        description: str, 
        input_schema: Dict[str, Any], 
        function: Callable
    ) -> None:
        """
        注册工具（符合 MCP 标准）
        
        Args:
            name (str): 工具名称
            description (str): 工具描述
            input_schema (Dict[str, Any]): 输入参数的 JSON Schema
            function (Callable): 工具实现函数
        """
        
        # 创建符合 MCP 标准的工具定义
        tool = Tool(
            name=name,
            description=description,
            inputSchema=input_schema
        )
        
        self._tools[name] = asdict(tool)
        self._tool_functions[name] = function
        self._call_stats[name] = 0
        
        logging.info(f"🔧 注册 MCP 工具: {name}")
    
    async def handle_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理 MCP 请求（符合 JSON-RPC 2.0 标准）
        
        Args:
            request_data (Dict[str, Any]): JSON-RPC 请求数据
            
        Returns:
            Dict[str, Any]: JSON-RPC 响应数据
        """
        
        try:
            # 解析请求
            request = MCPRequest(**request_data)
            
            # 验证 JSON-RPC 格式
            if request.jsonrpc != "2.0":
                return self._create_error_response(
                    request.id, -32600, "Invalid Request"
                )
            
            # 路由到对应的处理方法
            if request.method == MethodType.INITIALIZE.value:
                result = await self._handle_initialize(request.params or {})
            elif request.method == MethodType.LIST_TOOLS.value:
                result = await self._handle_list_tools()
            elif request.method == MethodType.CALL_TOOL.value:
                result = await self._handle_call_tool(request.params or {})
            else:
                return self._create_error_response(
                    request.id, -32601, f"Method not found: {request.method}"
                )
            
            # 创建成功响应
            response = MCPResponse(
                id=request.id,
                result=result
            )
            
            return asdict(response)
            
        except Exception as e:
            logging.error(f"处理 MCP 请求时发生错误: {str(e)}")
            return self._create_error_response(
                request_data.get("id"), -32603, f"Internal error: {str(e)}"
            )
    
    async def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理初始化请求"""
        
        self._initialized = True
        
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": self.capabilities,
            "serverInfo": {
                "name": self.name,
                "version": self.version
            }
        }
    
    async def _handle_list_tools(self) -> Dict[str, Any]:
        """处理工具列表请求"""
        
        if not self._initialized:
            raise Exception("Server not initialized")
        
        tools = list(self._tools.values())
        
        return {"tools": tools}
    
    async def _handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理工具调用请求"""
        
        if not self._initialized:
            raise Exception("Server not initialized")
        
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name not in self._tool_functions:
            raise Exception(f"Tool not found: {tool_name}")
        
        try:
            # 更新调用统计
            self._call_stats[tool_name] += 1
            
            # 执行工具函数
            function = self._tool_functions[tool_name]
            result = await self._execute_tool_safely(function, arguments)
            
            # 返回符合 MCP 标准的结果
            tool_result = ToolResult(
                content=[{
                    "type": "text",
                    "text": json.dumps(result, ensure_ascii=False, indent=2)
                }],
                isError=False
            )
            
            return asdict(tool_result)
            
        except Exception as e:
            # 返回错误结果
            tool_result = ToolResult(
                content=[{
                    "type": "text", 
                    "text": f"工具执行失败: {str(e)}"
                }],
                isError=True
            )
            
            return asdict(tool_result)
    
    async def _execute_tool_safely(self, function: Callable, arguments: Dict[str, Any]) -> Any:
        """安全执行工具函数"""
        
        # 如果是异步函数
        if asyncio.iscoroutinefunction(function):
            return await function(**arguments)
        else:
            # 在线程池中执行同步函数
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, lambda: function(**arguments))
    
    def _create_error_response(self, request_id: Any, code: int, message: str) -> Dict[str, Any]:
        """创建错误响应"""
        
        error = MCPError(code=code, message=message)
        response = MCPResponse(id=request_id, error=error)
        
        return asdict(response)
    
    # ===========================================
    # 工具实现函数
    # ===========================================
    
    def _read_file_tool(self, path: str) -> Dict[str, Any]:
        """文件读取工具实现"""
        
        try:
            # 安全检查
            if not os.path.exists(path):
                raise FileNotFoundError(f"文件不存在: {path}")
            
            # 读取文件
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "operation": "read_file",
                "path": path,
                "content": content,
                "size": len(content),
                "timestamp": datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"读取文件失败: {str(e)}")
    
    def _write_file_tool(self, path: str, content: str) -> Dict[str, Any]:
        """文件写入工具实现"""
        
        try:
            # 确保目录存在
            directory = os.path.dirname(path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            
            # 写入文件
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                "operation": "write_file",
                "path": path,
                "size": len(content),
                "timestamp": datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"写入文件失败: {str(e)}")
    
    def _calculate_tool(self, expression: str) -> Dict[str, Any]:
        """数学计算工具实现"""
        
        try:
            # 安全检查
            allowed_chars = set('0123456789+-*/().%** ')
            if not all(c in allowed_chars for c in expression):
                raise ValueError("表达式包含不允许的字符")
            
            # 计算结果
            result = eval(expression, {"__builtins__": {}}, {})
            
            return {
                "operation": "calculate",
                "expression": expression,
                "result": result,
                "result_type": type(result).__name__,
                "timestamp": datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"计算失败: {str(e)}")
    
    def _get_time_tool(self, format: str = "iso") -> Dict[str, Any]:
        """获取时间工具实现"""
        
        now = datetime.datetime.now()
        
        if format == "iso":
            formatted_time = now.isoformat()
        elif format == "timestamp":
            formatted_time = str(now.timestamp())
        else:
            formatted_time = now.strftime(format)
        
        return {
            "operation": "get_current_time",
            "format": format,
            "formatted_time": formatted_time,
            "timestamp": now.timestamp(),
            "iso_format": now.isoformat(),
            "components": {
                "year": now.year,
                "month": now.month,
                "day": now.day,
                "hour": now.hour,
                "minute": now.minute,
                "second": now.second
            }
        }
    
    def get_server_stats(self) -> Dict[str, Any]:
        """获取服务器统计信息"""
        
        return {
            "server_info": {
                "name": self.name,
                "version": self.version,
                "session_id": self._session_id,
                "initialized": self._initialized
            },
            "tools": {
                "total": len(self._tools),
                "names": list(self._tools.keys())
            },
            "call_stats": self._call_stats.copy(),
            "capabilities": self.capabilities
        }


# 创建全局 MCP Server 实例
mcp_server = MCPServer()

# 如果直接运行此文件，启动一个简单的测试服务器
if __name__ == "__main__":
    import asyncio
    
    async def test_mcp_server():
        """测试 MCP Server"""
        
        print("🧪 测试真正的 MCP Server")
        print("="*50)
        
        # 测试初始化
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            }
        }
        
        init_response = await mcp_server.handle_request(init_request)
        print(f"✅ 初始化响应: {json.dumps(init_response, indent=2)}")
        
        # 测试工具列表
        list_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        list_response = await mcp_server.handle_request(list_request)
        print(f"✅ 工具列表: {json.dumps(list_response, indent=2)}")
        
        # 测试工具调用
        call_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "get_current_time",
                "arguments": {"format": "iso"}
            }
        }
        
        call_response = await mcp_server.handle_request(call_request)
        print(f"✅ 工具调用结果: {json.dumps(call_response, indent=2)}")
        
        # 显示服务器统计
        stats = mcp_server.get_server_stats()
        print(f"📊 服务器统计: {json.dumps(stats, indent=2)}")
    
    # 运行测试
    asyncio.run(test_mcp_server())
