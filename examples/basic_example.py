"""
基础示例：Langchain + MCP Server 入门

这个示例展示了最基本的 Langchain 与 MCP Server 集成使用方法。
适合初学者理解整个系统的工作原理。

学习目标：
1. 了解如何初始化系统组件
2. 学会基本的工具调用
3. 理解 Agent 的工作流程
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.config import config
from src.mcp_server import mcp_server
from src.langchain_client import langchain_client


def example_1_basic_chat():
    """示例 1：基础对话"""
    
    print("\n" + "="*50)
    print("📝 示例 1：基础对话")
    print("="*50)
    
    # 简单的问候
    message = "你好，请介绍一下你自己"
    print(f"👤 用户: {message}")
    
    result = langchain_client.chat(message)
    if result["success"]:
        print(f"🤖 助手: {result['output']}")
    else:
        print(f"❌ 错误: {result['error']}")
    
    print("\n💡 这个例子展示了最基本的对话功能")


def example_2_file_operations():
    """示例 2：文件操作"""
    
    print("\n" + "="*50)
    print("📁 示例 2：文件操作")
    print("="*50)
    
    # 创建文件
    print("\n🔸 创建文件")
    message = "请创建一个名为 demo.txt 的文件，内容是 '这是一个演示文件'"
    print(f"👤 用户: {message}")
    
    result = langchain_client.chat(message)
    if result["success"]:
        print(f"🤖 助手: {result['output']}")
    else:
        print(f"❌ 错误: {result['error']}")
    
    # 读取文件
    print("\n🔸 读取文件")
    message = "请读取 demo.txt 文件的内容"
    print(f"👤 用户: {message}")
    
    result = langchain_client.chat(message)
    if result["success"]:
        print(f"🤖 助手: {result['output']}")
    else:
        print(f"❌ 错误: {result['error']}")
    
    # 列出文件
    print("\n🔸 列出文件")
    message = "请列出当前工作目录中的所有文件"
    print(f"👤 用户: {message}")
    
    result = langchain_client.chat(message)
    if result["success"]:
        print(f"🤖 助手: {result['output']}")
    else:
        print(f"❌ 错误: {result['error']}")
    
    print("\n💡 这个例子展示了文件操作功能：创建、读取、列出文件")


def example_3_calculations():
    """示例 3：数学计算"""
    
    print("\n" + "="*50)
    print("🧮 示例 3：数学计算")
    print("="*50)
    
    # 基础计算
    print("\n🔸 基础数学运算")
    message = "请计算 (25 + 75) * 2 的结果"
    print(f"👤 用户: {message}")
    
    result = langchain_client.chat(message)
    if result["success"]:
        print(f"🤖 助手: {result['output']}")
    else:
        print(f"❌ 错误: {result['error']}")
    
    # 复杂计算
    print("\n🔸 复杂数学运算")
    message = "请计算 2**10 + 3**5 的结果"
    print(f"👤 用户: {message}")
    
    result = langchain_client.chat(message)
    if result["success"]:
        print(f"🤖 助手: {result['output']}")
    else:
        print(f"❌ 错误: {result['error']}")
    
    # 随机数生成
    print("\n🔸 生成随机数")
    message = "请生成一个 1 到 100 之间的随机数"
    print(f"👤 用户: {message}")
    
    result = langchain_client.chat(message)
    if result["success"]:
        print(f"🤖 助手: {result['output']}")
    else:
        print(f"❌ 错误: {result['error']}")
    
    print("\n💡 这个例子展示了数学计算功能：基础运算、复杂计算、随机数生成")


def example_4_time_operations():
    """示例 4：时间操作"""
    
    print("\n" + "="*50)
    print("⏰ 示例 4：时间操作")
    print("="*50)
    
    # 获取当前时间
    print("\n🔸 获取当前时间")
    message = "请告诉我现在的时间"
    print(f"👤 用户: {message}")
    
    result = langchain_client.chat(message)
    if result["success"]:
        print(f"🤖 助手: {result['output']}")
    else:
        print(f"❌ 错误: {result['error']}")
    
    # 格式化时间戳
    print("\n🔸 格式化时间戳")
    message = "请将时间戳 1640995200 格式化为可读的时间"
    print(f"👤 用户: {message}")
    
    result = langchain_client.chat(message)
    if result["success"]:
        print(f"🤖 助手: {result['output']}")
    else:
        print(f"❌ 错误: {result['error']}")
    
    print("\n💡 这个例子展示了时间操作功能：获取当前时间、格式化时间戳")


def example_5_combined_operations():
    """示例 5：组合操作"""
    
    print("\n" + "="*50)
    print("🔗 示例 5：组合操作")
    print("="*50)
    
    # 组合操作：计算结果并保存到文件
    print("\n🔸 计算并保存结果")
    message = "请计算 123 * 456 的结果，然后将计算过程和结果保存到 calculation.txt 文件中"
    print(f"👤 用户: {message}")
    
    result = langchain_client.chat(message)
    if result["success"]:
        print(f"🤖 助手: {result['output']}")
    else:
        print(f"❌ 错误: {result['error']}")
    
    # 组合操作：获取时间并保存
    print("\n🔸 获取时间并保存")
    message = "请获取当前时间，并将其保存到 current_time.txt 文件中"
    print(f"👤 用户: {message}")
    
    result = langchain_client.chat(message)
    if result["success"]:
        print(f"🤖 助手: {result['output']}")
    else:
        print(f"❌ 错误: {result['error']}")
    
    # 验证文件创建
    print("\n🔸 验证创建的文件")
    message = "请列出工作目录中的所有文件，特别是刚刚创建的文件"
    print(f"👤 用户: {message}")
    
    result = langchain_client.chat(message)
    if result["success"]:
        print(f"🤖 助手: {result['output']}")
    else:
        print(f"❌ 错误: {result['error']}")
    
    print("\n💡 这个例子展示了组合操作：多个工具的连续使用")


def display_system_info():
    """显示系统信息"""
    
    print("\n" + "="*50)
    print("📋 系统信息")
    print("="*50)
    
    # 显示配置信息
    print(f"🌐 API 地址: {config.api_base_url}")
    print(f"🤖 模型名称: {config.model_name}")
    print(f"📁 工作目录: {config.work_directory}")
    
    # 显示工具信息
    tools_info = langchain_client.get_tools_info()
    print(f"\n🔧 可用工具 ({len(tools_info)} 个):")
    for tool in tools_info:
        print(f"   • {tool['name']}: {tool['description'][:60]}...")
    
    # 显示使用统计
    stats = langchain_client.get_usage_stats()
    print(f"\n📊 使用统计:")
    print(f"   • 总调用次数: {stats['total_calls']}")
    print(f"   • 最常用工具: {stats.get('most_used_tool', '无')}")


def main():
    """主函数：运行所有基础示例"""
    
    print("🚀 Langchain + MCP Server 基础示例")
    print("="*60)
    print("📚 这个示例将演示系统的基本功能")
    print("💡 请观察每个操作的输入输出，理解工作原理")
    print("="*60)
    
    try:
        # 显示系统信息
        display_system_info()
        
        # 运行示例
        example_1_basic_chat()
        example_2_file_operations()
        example_3_calculations()
        example_4_time_operations()
        example_5_combined_operations()
        
        # 最终统计
        print("\n" + "="*50)
        print("📊 运行完成统计")
        print("="*50)
        
        final_stats = langchain_client.get_usage_stats()
        print(f"本次运行工具调用总数: {final_stats['total_calls']}")
        print("各工具使用次数:")
        for tool_name, count in final_stats['tool_usage'].items():
            print(f"   • {tool_name}: {count} 次")
        
        print("\n✅ 所有基础示例运行完成！")
        print("💡 接下来你可以：")
        print("   1. 查看其他示例文件")
        print("   2. 运行 src/main.py 进行交互式对话")
        print("   3. 阅读 tutorial.md 了解更多细节")
        
    except Exception as e:
        print(f"\n❌ 示例运行失败: {str(e)}")
        print("💡 请检查配置和依赖是否正确")


if __name__ == "__main__":
    main()
