"""
Langchain + MCP 集成客户端

这个模块展示了如何将 Model Context Protocol 集成到 Langchain 中，
实现 AI 代理通过标准 MCP 协议调用外部工具。
"""

import json
import asyncio
from typing import Dict, Any, List, Optional
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain.tools import Tool

# 使用绝对导入
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import config
from mcp_client import MCPClient
from mcp_server import MCPServer
import requests

# 创建全局 MCP 实例 保持1对1的链接
mcp_server = MCPServer()
mcp_client = MCPClient(server=mcp_server)


class CustomLLM(LLM):
    """
    自定义 LLM 类
    """
    
    def __init__(self):
        super().__init__()
        # 将属性存储为内部变量，避免与pydantic冲突
        self._api_url = f"{config.api_base_url}/chat/completions"
        self._headers = config.get_api_headers()
        self._model_name = config.model_name
        
        print(f"🤖 初始化 LLM: {self._model_name}")
    
    @property
    def _llm_type(self) -> str:
        return "custom_api"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        
        request_data = {
            "model": self._model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 1000),
        }
        
        if stop:
            request_data["stop"] = stop
        
        try:
            response = requests.post(
                self._api_url,
                headers=self._headers,
                json=request_data,
                timeout=config.api_timeout
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            if "choices" in response_data and len(response_data["choices"]) > 0:
                return response_data["choices"][0]["message"]["content"]
            else:
                raise ValueError("API 响应格式错误")
                
        except Exception as e:
            raise Exception(f"LLM 调用失败: {str(e)}")


class MCPToolWrapper:
    """
    MCP 工具包装器
    
    这个包装器通过标准 MCP 协议与 MCP Server 通信
    """
    
    def __init__(self, tool_name: str, tool_info: Dict[str, Any]):
        """
        初始化真正的 MCP 工具包装器
        
        Args:
            tool_name (str): 工具名称
            tool_info (Dict[str, Any]): 工具信息
        """
        self.tool_name = tool_name
        self.tool_info = tool_info
    
    def __call__(self, **kwargs) -> str:
        """
        通过 MCP 协议调用工具
        
        Args:
            **kwargs: 工具参数
            
        Returns:
            str: 工具执行结果
        """
        try:
            # 🔑 关键：这里使用真正的 MCP 协议进行通信
            # 检查是否已有事件循环在运行
            try:
                loop = asyncio.get_running_loop()
                # 如果有运行中的循环，使用 asyncio.create_task
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, mcp_client.call_tool(self.tool_name, kwargs))
                    result = future.result()
            except RuntimeError:
                # 没有运行中的循环，创建新的
                result = asyncio.run(mcp_client.call_tool(self.tool_name, kwargs))
            
            if result["success"]:
                output = f"✅ MCP 工具 '{self.tool_name}' 执行成功\n"
                output += f"📡 通过 JSON-RPC 2.0 协议调用\n"
                output += f"结果: {json.dumps(result['result'], ensure_ascii=False, indent=2)}"
                return output
            else:
                output = f"❌ MCP 工具 '{self.tool_name}' 执行失败\n"
                output += f"错误: {result['error']}"
                return output
                
        except Exception as e:
            return f"❌ MCP 工具调用异常: {str(e)}"


class MCPLangchainClient:
    """
    集成 MCP 协议的 Langchain 客户端
    
    这个类展示了如何将标准的 MCP 协议集成到 Langchain 中
    """
    
    def __init__(self):
        """初始化 MCP Langchain 客户端"""
        
        self.llm = CustomLLM()
        self.mcp_initialized = False
        self.tools = []
        
        print(f"🔗 真正的 MCP Langchain 客户端初始化中...")
    
    async def initialize(self) -> bool:
        """
        初始化 MCP 连接
        
        Returns:
            bool: 初始化是否成功
        """
        
        try:
            # 初始化 MCP 客户端
            success = await mcp_client.initialize()
            
            if not success:
                print("❌ MCP 客户端初始化失败")
                return False
            
            self.mcp_initialized = True
            
            # 创建 Langchain 工具
            await self._create_tools()
            
            print(f"✅ 真正的 MCP Langchain 客户端初始化完成，集成了 {len(self.tools)} 个工具")
            return True
            
        except Exception as e:
            print(f"❌ MCP Langchain 客户端初始化失败: {str(e)}")
            return False
    
    async def _create_tools(self) -> None:
        """创建 Langchain 工具（基于真正的 MCP 协议）"""
        
        self.tools = []
        
        # 从 MCP 客户端获取可用工具
        available_tools = mcp_client.get_available_tools()
        
        for tool_info in available_tools:
            tool_name = tool_info["name"]
            
            # 创建真正的 MCP 工具包装器
            wrapper = MCPToolWrapper(tool_name, tool_info)
            
            # 创建 Langchain Tool
            langchain_tool = Tool(
                name=tool_name,
                description=tool_info["description"],
                func=wrapper
            )
            
            self.tools.append(langchain_tool)
            print(f"🔧 集成真正的 MCP 工具: {tool_name}")
    
    async def chat(self, message: str) -> Dict[str, Any]:
        """
        与集成了真正 MCP 的 Agent 对话
        
        Args:
            message (str): 用户消息
            
        Returns:
            Dict[str, Any]: 回复结果
        """
        
        if not self.mcp_initialized:
            return {
                "success": False,
                "error": "MCP 客户端未初始化",
                "output": "请先初始化 MCP 连接"
            }
        
        try:
            print(f"👤 用户: {message}")
            print("🤖 通过真正的 MCP 协议处理...")
            
            result = await self._process_with_mcp(message)
            
            print(f"🤖 助手: {result['output']}")
            
            return result
            
        except Exception as e:
            error_msg = f"MCP 对话处理失败: {str(e)}"
            print(f"❌ {error_msg}")
            
            return {
                "success": False,
                "error": error_msg,
                "output": "抱歉，处理您的请求时遇到了问题。"
            }
    
    async def _process_with_mcp(self, message: str) -> Dict[str, Any]:
        """使用真正的 MCP 协议处理消息"""
        
        # 构建工具描述（包含参数信息）
        tools_desc = []
        for tool in self.tools:
            if tool.name == "write_file":
                tools_desc.append(f"- {tool.name}: {tool.description} (参数: path=文件路径, content=文件内容)")
            elif tool.name == "read_file":
                tools_desc.append(f"- {tool.name}: {tool.description} (参数: path=文件路径)")
            elif tool.name == "calculate":
                tools_desc.append(f"- {tool.name}: {tool.description} (参数: expression=数学表达式)")
            elif tool.name == "get_current_time":
                tools_desc.append(f"- {tool.name}: {tool.description} (无参数)")
            else:
                tools_desc.append(f"- {tool.name}: {tool.description}")
        tools_desc = "\n".join(tools_desc)
        
        # 构建提示
        prompt = f"""用户请求: {message}

这是一个使用真正 Model Context Protocol (MCP) 的系统！

🔧 可用的 MCP 工具:
{tools_desc}

💡 MCP 协议特点:
- 基于 JSON-RPC 2.0 标准
- Client-Server 架构通信
- 标准化工具发现和调用
- 安全的网络协议

请分析用户需求：
1. 如果需要使用工具，请说明要使用的 MCP 工具及原因
2. 然后按照以下格式输出：
   MCP_TOOL: [工具名称]
   MCP_PARAMS: {{"参数名": "参数值"}}
3. 如果不需要工具，直接回复用户

请开始分析并处理用户请求："""

        # 调用 LLM
        response = self.llm(prompt)
        
        intermediate_steps = []
        
        # 检查是否需要 MCP 工具调用
        if "MCP_TOOL:" in response and "MCP_PARAMS:" in response:
            try:
                # 解析 MCP 工具调用
                lines = response.split('\n')
                tool_name = None
                params = {}
                
                for line in lines:
                    if line.startswith("MCP_TOOL:"):
                        tool_name = line.replace("MCP_TOOL:", "").strip()
                    elif line.startswith("MCP_PARAMS:"):
                        try:
                            params_str = line.replace("MCP_PARAMS:", "").strip()
                            params = json.loads(params_str)
                        except:
                            params = {}
                
                # 执行 MCP 工具
                if tool_name:
                    tool_names = [tool.name for tool in self.tools]
                    if tool_name in tool_names:
                        tool = next(tool for tool in self.tools if tool.name == tool_name)
                        
                        print(f"📡 通过 MCP 协议执行工具: {tool_name}")
                        print(f"📥 MCP 参数: {params}")
                        
                        # 🔑 关键：这里通过真正的 MCP 协议调用工具
                        tool_result = tool.func(**params)
                        
                        intermediate_steps.append({
                            "mcp_tool": tool_name,
                            "mcp_params": params,
                            "mcp_result": tool_result,
                            "protocol": "JSON-RPC 2.0"
                        })
                        
                        # 生成最终回复
                        final_prompt = f"""MCP 工具执行结果：
{tool_result}

原始用户请求：{message}

这个结果是通过真正的 Model Context Protocol (MCP) 获得的：
- 使用了 JSON-RPC 2.0 协议
- Client-Server 架构通信
- 标准化的工具调用接口

请根据 MCP 工具执行结果，生成一个友好、有用的回复给用户："""
                        
                        final_response = self.llm(final_prompt)
                        
                        return {
                            "success": True,
                            "output": final_response,
                            "mcp_steps": intermediate_steps,
                            "protocol_used": "Model Context Protocol (JSON-RPC 2.0)"
                        }
            
            except Exception as e:
                print(f"⚠️ MCP 工具调用解析失败: {str(e)}")
        
        # 直接回复
        return {
            "success": True,
            "output": response,
            "mcp_steps": intermediate_steps,
            "protocol_used": "Direct LLM Response"
        }
    
    def get_mcp_info(self) -> Dict[str, Any]:
        """获取 MCP 协议信息"""
        
        client_info = mcp_client.get_client_info()
        
        return {
            "mcp_protocol": "Model Context Protocol (JSON-RPC 2.0)",
            "mcp_version": "2024-11-05",
            "client_info": client_info,
            "tools_count": len(self.tools),
            "initialized": self.mcp_initialized,
            "standards_compliance": {
                "json_rpc": "2.0",
                "client_server_architecture": True,
                "standardized_tool_discovery": True,
                "secure_communication": True
            }
        }


# 创建真正的 MCP Langchain 客户端实例
mcp_langchain_client = MCPLangchainClient()

# 如果直接运行此文件，进行测试
if __name__ == "__main__":
    import asyncio
    
    async def test_mcp_langchain():
        """测试真正的 MCP Langchain 集成"""
        
        print("🧪 测试真正的 MCP + Langchain 集成")
        print("="*60)
        
        # 初始化
        success = await mcp_langchain_client.initialize()
        if not success:
            print("❌ 初始化失败")
            return
        
        # 显示 MCP 信息
        mcp_info = mcp_langchain_client.get_mcp_info()
        print(f"📋 MCP 协议信息:")
        print(f"   协议: {mcp_info['mcp_protocol']}")
        print(f"   版本: {mcp_info['mcp_version']}")
        print(f"   工具数量: {mcp_info['tools_count']}")
        print(f"   标准合规: JSON-RPC 2.0 ✅")
        
        # 测试对话
        test_messages = [
            "你好，请介绍一下你使用的 MCP 协议",
            "请获取当前时间",
            "请计算 25 * 4 + 10 的结果",
            "请创建一个文件 mcp_demo.txt，内容是'这是通过真正的 MCP 协议创建的！'"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n🔍 测试 {i}: {message}")
            print("-" * 50)
            
            result = await mcp_langchain_client.chat(message)
            
            if result["success"]:
                print(f"✅ 成功")
                if "mcp_steps" in result and result["mcp_steps"]:
                    print(f"📡 使用了 MCP 协议: {result['protocol_used']}")
                    for step in result["mcp_steps"]:
                        print(f"   MCP 工具: {step['mcp_tool']}")
                        print(f"   协议: {step['protocol']}")
            else:
                print(f"❌ 失败: {result['error']}")
    
    # 运行测试
    asyncio.run(test_mcp_langchain())
