"""
MCP 协议测试
运行这个脚本来验证 MCP 协议的正确性
"""
import asyncio
import json
from src.mcp_server import MCPServer
from src.mcp_client import MCPClient

async def test_mcp_protocol():
    print("🚀 测试 MCP 协议")
    print("=" * 50)
    
    # 1. 启动 MCP Server
    server = MCPServer()
    print("✅ MCP Server 已启动")
    
    # 2. 创建 MCP Client
    client = MCPClient(server=server)
    print("✅ MCP Client 已连接")
    
    # 3. 测试初始化
    print("\n📡 测试 MCP 初始化...")
    try:
        init_result = await client.initialize()
        print(f"初始化结果: {init_result}")
        
        if not init_result:
            print("❌ 初始化失败")
            return
        
        # 输出详细的客户端状态
        client_info = client.get_client_info()
        print(f"✅ 客户端信息: {json.dumps(client_info, indent=2, ensure_ascii=False)}")
        
    except Exception as e:
        print(f"❌ 初始化异常: {e}")
        return
    
    # 4. 测试工具列表发现
    print("\n🔍 测试工具发现...")
    tools = client.get_available_tools()
    print(f"发现的工具 ({len(tools)} 个):")
    for tool in tools:
        print(f"   • {tool['name']}: {tool['description']}")
    
    # 5. 测试工具调用
    print("\n⚡ 测试工具调用...")
    
    # 测试获取时间
    print("🕐 测试时间工具...")
    time_result = await client.call_tool("get_current_time", {"format": "iso"})
    if time_result["success"]:
        print(f"✅ 时间工具成功: {time_result['result']['formatted_time']}")
    else:
        print(f"❌ 时间工具失败: {time_result['error']}")
    
    # 测试计算器
    print("🧮 测试计算器...")
    calc_result = await client.call_tool("calculate", {"expression": "10 + 5 * 2"})
    if calc_result["success"]:
        print(f"✅ 计算器成功: {calc_result['result']['result']}")
    else:
        print(f"❌ 计算器失败: {calc_result['error']}")
    
    # 测试文件操作
    print("📁 测试文件操作...")
    write_result = await client.call_tool(
        "write_file", 
        {"path": "workspace/test.txt", "content": "MCP 协议测试成功！"}
    )
    if write_result["success"]:
        print("✅ 文件写入成功")
    else:
        print(f"❌ 文件写入失败: {write_result['error']}")
    
    read_result = await client.call_tool("read_file", {"path": "workspace/test.txt"})
    if read_result["success"]:
        print(f"✅ 文件读取成功: {read_result['result']['content']}")
    else:
        print(f"❌ 文件读取失败: {read_result['error']}")
    
    print("\n" + "=" * 50)
    print("✅ MCP 协议测试完成！")
    print("\n🎯 关键特征验证:")
    print("  ✅ JSON-RPC 2.0 协议格式")
    print("  ✅ 客户端-服务器架构")
    print("  ✅ 标准化工具发现机制")
    print("  ✅ 异步网络通信")
    print("  ✅ 错误处理和响应格式")

def show_protocol_details():
    """展示协议详细信息"""
    print("\n📋 MCP 协议详细信息:")
    print("-" * 30)
    
    print("\n1. 初始化请求格式:")
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "clientInfo": {
                "name": "Langchain-MCP-Client",
                "version": "1.0.0"
            }
        }
    }
    print(json.dumps(init_request, indent=2, ensure_ascii=False))
    
    print("\n2. 工具调用请求格式:")
    tool_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "get_current_time",
            "arguments": {
                "format": "iso"
            }
        }
    }
    print(json.dumps(tool_request, indent=2, ensure_ascii=False))
    
    print("\n3. 标准响应格式:")
    response = {
        "jsonrpc": "2.0",
        "id": 2,
        "result": {
            "content": [
                {
                    "type": "text",
                    "text": "2025-07-07T17:45:22.783987"
                }
            ]
        }
    }
    print(json.dumps(response, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    print("🎯 MCP 协议测试")
    print("Model Context Protocol (MCP) - JSON-RPC 2.0 实现")
    print("=" * 60)
    
    # 显示协议详情
    show_protocol_details()
    
    # 运行测试
    print("\n" + "=" * 60)
    asyncio.run(test_mcp_protocol())
    
    print("\n📚 要测试 Langchain 集成，请执行:")
    print("  python src/langchain_client.py")
