"""
MCP 客户端实现

这个模块实现了符合 Model Context Protocol 标准的客户端，
用于与 MCP Server 进行通信。
"""

import json
import asyncio
import logging
from typing import Dict, Any, List, Optional
import uuid
from dataclasses import dataclass

# 导入 MCP Server 以便进行本地测试
# 在实际部署中，这里应该是网络连接


class MCPClient:
    """
    MCP 客户端
    
    实现了完整的 Model Context Protocol 客户端功能
    """
    
    def __init__(self, server=None, client_name: str = "Langchain-MCP-Client"):
        """
        初始化 MCP 客户端
        
        Args:
            server: MCP 服务器实例（用于本地测试）
            client_name (str): 客户端名称
        """
        self.server = server
        self.client_name = client_name
        self.client_version = "1.0.0"
        self.session_id = str(uuid.uuid4())
        self.request_id = 0
        self.initialized = False
        self.server_capabilities = {}
        self.available_tools = []
        
        logging.info(f"🔌 MCP 客户端初始化: {self.client_name}")
    
    def _next_request_id(self) -> int:
        """生成下一个请求 ID"""
        self.request_id += 1
        return self.request_id
    
    async def initialize(self) -> bool:
        """
        初始化与 MCP Server 的连接
        
        Returns:
            bool: 初始化是否成功
        """
        
        try:
            # 创建初始化请求
            init_request = {
                "jsonrpc": "2.0",
                "id": self._next_request_id(),
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "roots": {"listChanged": True}
                    },
                    "clientInfo": {
                        "name": self.client_name,
                        "version": self.client_version
                    }
                }
            }
            
            # 发送初始化请求
            if not self.server:
                raise Exception("MCP Server 未连接")
            
            response = await self.server.handle_request(init_request)
            
            if "error" in response and response["error"] is not None:
                logging.error(f"MCP 初始化失败: {response['error']}")
                return False
            
            # 解析服务器信息
            result = response.get("result")
            if result is None:
                logging.error(f"MCP 初始化失败: result 为 None")
                return False
            self.server_capabilities = result.get("capabilities", {})
            server_info = result.get("serverInfo", {})
            
            self.initialized = True
            
            logging.info(f"✅ MCP 连接初始化成功")
            logging.info(f"服务器: {server_info.get('name')} v{server_info.get('version')}")
            
            # 获取可用工具列表
            await self._refresh_tools()
            
            return True
            
        except Exception as e:
            logging.error(f"MCP 初始化异常: {str(e)}")
            return False
    
    async def _refresh_tools(self) -> None:
        """刷新可用工具列表"""
        
        if not self.initialized:
            return
        
        try:
            # 请求工具列表
            list_request = {
                "jsonrpc": "2.0",
                "id": self._next_request_id(),
                "method": "tools/list"
            }
            
            response = await self.server.handle_request(list_request)
            
            if "error" in response and response["error"] is not None:
                logging.error(f"获取工具列表失败: {response['error']}")
                return
            
            result = response.get("result")
            if result is None:
                logging.error(f"获取工具列表失败: result 为 None")
                return
            self.available_tools = result.get("tools", [])
            
            logging.info(f"📋 获取到 {len(self.available_tools)} 个可用工具")
            
        except Exception as e:
            logging.error(f"刷新工具列表异常: {str(e)}")
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用 MCP 工具
        
        Args:
            tool_name (str): 工具名称
            arguments (Dict[str, Any]): 工具参数
            
        Returns:
            Dict[str, Any]: 工具执行结果
        """
        
        if not self.initialized:
            raise Exception("MCP 客户端未初始化")
        
        try:
            # 创建工具调用请求
            call_request = {
                "jsonrpc": "2.0",
                "id": self._next_request_id(),
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }
            
            # 发送请求
            response = await self.server.handle_request(call_request)
            
            if "error" in response and response["error"] is not None:
                return {
                    "success": False,
                    "error": response["error"]["message"] if isinstance(response["error"], dict) else str(response["error"]),
                    "tool_name": tool_name,
                    "arguments": arguments
                }
            
            # 解析结果
            result = response.get("result")
            if result is None:
                return {
                    "success": False,
                    "error": "服务器返回的 result 为 None",
                    "tool_name": tool_name,
                    "arguments": arguments
                }
            content = result.get("content", [])
            is_error = result.get("isError", False)
            
            if is_error:
                return {
                    "success": False,
                    "error": content[0].get("text", "Unknown error") if content else "Unknown error",
                    "tool_name": tool_name,
                    "arguments": arguments
                }
            else:
                # 解析工具返回的 JSON 数据
                tool_result = {}
                if content and content[0].get("type") == "text":
                    try:
                        tool_result = json.loads(content[0]["text"])
                    except json.JSONDecodeError:
                        tool_result = {"raw_text": content[0]["text"]}
                
                return {
                    "success": True,
                    "result": tool_result,
                    "tool_name": tool_name,
                    "arguments": arguments
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "tool_name": tool_name,
                "arguments": arguments
            }
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        获取可用工具列表
        
        Returns:
            List[Dict[str, Any]]: 工具信息列表
        """
        
        return self.available_tools.copy()
    
    def get_client_info(self) -> Dict[str, Any]:
        """
        获取客户端信息
        
        Returns:
            Dict[str, Any]: 客户端信息
        """
        
        return {
            "client_name": self.client_name,
            "client_version": self.client_version,
            "session_id": self.session_id,
            "initialized": self.initialized,
            "server_capabilities": self.server_capabilities,
            "available_tools_count": len(self.available_tools)
        }


# 如果直接运行此文件，进行测试
if __name__ == "__main__":
    import asyncio
    from mcp_server import MCPServer
    
    async def test_mcp_client():
        """测试 MCP 客户端"""
        
        print("🧪 测试 MCP 客户端")
        print("="*50)
        
        # 创建服务器和客户端
        server = MCPServer()
        client = MCPClient(server=server)
        
        # 初始化客户端
        success = await client.initialize()
        if not success:
            print("❌ 客户端初始化失败")
            return
        
        print("✅ 客户端初始化成功")
        
        # 显示客户端信息
        client_info = client.get_client_info()
        print(f"📋 客户端信息: {json.dumps(client_info, indent=2)}")
        
        # 显示可用工具
        tools = client.get_available_tools()
        print(f"🔧 可用工具 ({len(tools)} 个):")
        for tool in tools:
            print(f"   • {tool['name']}: {tool['description']}")
        
        # 测试工具调用
        print("\n🔍 测试工具调用:")
        
        # 测试获取时间
        time_result = await client.call_tool("get_current_time", {"format": "iso"})
        print(f"⏰ 获取时间: {json.dumps(time_result, indent=2, ensure_ascii=False)}")
        
        # 测试数学计算
        calc_result = await client.call_tool("calculate", {"expression": "2 + 3 * 4"})
        print(f"🧮 数学计算: {json.dumps(calc_result, indent=2, ensure_ascii=False)}")
        
        # 测试文件写入
        write_result = await client.call_tool(
            "write_file", 
            {"path": "workspace/mcp_test.txt", "content": "这是通过真正的 MCP 协议创建的文件！"}
        )
        print(f"💾 文件写入: {json.dumps(write_result, indent=2, ensure_ascii=False)}")
        
        # 测试文件读取
        read_result = await client.call_tool("read_file", {"path": "workspace/mcp_test.txt"})
        print(f"📖 文件读取: {json.dumps(read_result, indent=2, ensure_ascii=False)}")
    
    # 运行测试
    asyncio.run(test_mcp_client())
