"""
主程序入口

这是整个项目的主入口文件，提供了一个简单的命令行界面来演示
Langchain 0.3 + MCP Server 的集成功能。

功能：
1. 初始化所有组件
2. 提供交互式命令行界面
3. 展示系统能力
4. 处理用户输入和工具调用
"""

import sys
import os
from typing import Dict, Any

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.config import config
from src.mcp_server import mcp_server
from src.langchain_client import langchain_client


def print_welcome_message():
    """打印欢迎信息"""
    
    print("\n" + "="*60)
    print("🎉 欢迎使用 Langchain 0.3 + MCP Server 演示系统")
    print("="*60)
    print("🤖 这是一个教学项目，展示如何集成 Langchain 和 MCP Server")
    print("💡 你可以使用自然语言与 AI 助手对话，它会自动调用合适的工具")
    print()
    print("🔧 可用功能：")
    
    # 显示可用工具
    tools_info = langchain_client.get_tools_info()
    for tool in tools_info:
        print(f"   📌 {tool['name']}: {tool['description'][:50]}...")
    
    print()
    print("💬 使用方法：")
    print("   - 直接输入你的问题或需求")
    print("   - 输入 'help' 查看帮助")
    print("   - 输入 'stats' 查看使用统计")
    print("   - 输入 'quit' 或 'exit' 退出程序")
    print("="*60 + "\n")


def print_help():
    """打印帮助信息"""
    
    print("\n📚 帮助信息")
    print("-"*40)
    print("🎯 示例用法：")
    print()
    print("📁 文件操作：")
    print("   • '创建一个文件 hello.txt，内容是 Hello World'")
    print("   • '读取 hello.txt 文件的内容'")
    print("   • '列出当前目录的所有文件'")
    print()
    print("🧮 数学计算：")
    print("   • '计算 25 + 75 * 2 的结果'")
    print("   • '生成一个 1 到 100 之间的随机数'")
    print()
    print("⏰ 时间操作：")
    print("   • '获取当前时间'")
    print("   • '将时间戳 1640995200 格式化为可读时间'")
    print()
    print("🔗 组合操作：")
    print("   • '获取当前时间并保存到 time.txt 文件中'")
    print("   • '计算 100 的平方根，然后保存结果到文件'")
    print()
    print("💡 提示：尽量用自然语言描述你的需求，AI 会自动选择合适的工具！")
    print("-"*40 + "\n")


def print_stats():
    """打印使用统计"""
    
    print("\n📊 使用统计")
    print("-"*40)
    
    # 获取统计信息
    stats = langchain_client.get_usage_stats()
    
    print(f"🔧 工具总数: {stats['total_tools']}")
    print(f"📞 总调用次数: {stats['total_calls']}")
    
    if stats['most_used_tool']:
        print(f"🏆 最常用工具: {stats['most_used_tool']}")
    
    print("\n📈 各工具使用次数:")
    for tool_name, count in stats['tool_usage'].items():
        print(f"   • {tool_name}: {count} 次")
    
    print("-"*40 + "\n")


def handle_user_input(user_input: str) -> bool:
    """
    处理用户输入
    
    Args:
        user_input (str): 用户输入
        
    Returns:
        bool: 如果需要退出返回 False，否则返回 True
    """
    
    # 清理输入
    user_input = user_input.strip()
    
    if not user_input:
        return True
    
    # 处理特殊命令
    if user_input.lower() in ['quit', 'exit', 'q']:
        print("👋 谢谢使用，再见！")
        return False
    
    elif user_input.lower() in ['help', 'h', '帮助']:
        print_help()
        return True
    
    elif user_input.lower() in ['stats', 'statistics', '统计']:
        print_stats()
        return True
    
    elif user_input.lower() in ['clear', 'cls']:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_welcome_message()
        return True
    
    # 处理正常对话
    try:
        print(f"\n👤 你: {user_input}")
        print("🤖 正在思考...")
        
        # 调用 Langchain 客户端处理
        result = langchain_client.chat(user_input)
        
        if result["success"]:
            print(f"🤖 助手: {result['output']}")
            
            # 如果有中间步骤，显示详细信息
            if result.get("intermediate_steps"):
                print("\n🔍 执行详情:")
                for i, step in enumerate(result["intermediate_steps"], 1):
                    print(f"   {i}. 使用工具: {step['action']}")
                    if step.get('input'):
                        print(f"      参数: {step['input']}")
        else:
            print(f"❌ 处理失败: {result['error']}")
            print(f"🤖 助手: {result['output']}")
    
    except KeyboardInterrupt:
        print("\n\n⚠️ 操作被用户中断")
        return True
    
    except Exception as e:
        print(f"\n❌ 系统错误: {str(e)}")
        print("💡 请尝试重新输入或输入 'help' 查看帮助")
    
    return True


def check_system_status():
    """检查系统状态"""
    
    print("🔍 正在检查系统状态...")
    
    try:
        # 检查配置
        config.print_config_summary()
        
        # 检查 MCP Server
        tools_count = len(mcp_server.tools)
        print(f"✅ MCP Server 运行正常，已注册 {tools_count} 个工具")
        
        # 检查 Langchain 客户端
        client_tools_count = len(langchain_client.tools)
        print(f"✅ Langchain 客户端运行正常，已集成 {client_tools_count} 个工具")
        
        # 简单测试
        print("🧪 正在进行系统测试...")
        test_result = mcp_server.execute_tool("get_current_time", {})
        if test_result["success"]:
            print("✅ 系统测试通过")
        else:
            print(f"⚠️ 系统测试警告: {test_result['error']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 系统检查失败: {str(e)}")
        print("💡 请检查配置文件和依赖是否正确安装")
        return False


def main():
    """主函数"""
    
    try:
        print("🚀 正在启动 Langchain + MCP Server 演示系统...")
        
        # 检查系统状态
        if not check_system_status():
            print("❌ 系统初始化失败，无法继续运行")
            return
        
        # 显示欢迎信息
        print_welcome_message()
        
        # 主循环
        while True:
            try:
                # 获取用户输入
                user_input = input("💬 请输入: ").strip()
                
                # 处理用户输入
                if not handle_user_input(user_input):
                    break
                
                print()  # 添加空行分隔
                
            except KeyboardInterrupt:
                print("\n\n👋 检测到 Ctrl+C，正在退出...")
                break
            
            except EOFError:
                print("\n\n👋 检测到 EOF，正在退出...")
                break
    
    except Exception as e:
        print(f"\n❌ 程序运行出现错误: {str(e)}")
        print("💡 请检查日志或联系开发者")
    
    finally:
        print("\n🛑 程序已退出")


if __name__ == "__main__":
    main()
