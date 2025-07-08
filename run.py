"""
快速启动脚本

这个脚本提供了快速启动和测试项目的方法。
适合初学者快速体验系统功能。
"""

import sys
import os

# 确保项目根目录在 Python 路径中
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def quick_test():
    """快速功能测试"""
    
    print("🧪 正在进行快速功能测试...")
    
    try:
        # 测试配置模块
        from src.config import config
        print("✅ 配置模块加载成功")
        
        # 测试 MCP Server
        from src.mcp_server import mcp_server
        print(f"✅ MCP Server 初始化成功，注册了 {len(mcp_server.tools)} 个工具")
        
        # 测试 Langchain 客户端
        from src.langchain_client import langchain_client
        print(f"✅ Langchain 客户端初始化成功，集成了 {len(langchain_client.tools)} 个工具")
        
        # 简单功能测试
        print("\n🔍 执行简单功能测试...")
        
        # 测试时间工具
        result = mcp_server.execute_tool("get_current_time", {})
        if result["success"]:
            print("✅ 时间工具测试通过")
        else:
            print(f"❌ 时间工具测试失败: {result['error']}")
        
        # 测试计算工具
        result = mcp_server.execute_tool("calculate", {"expression": "2 + 2"})
        if result["success"]:
            print("✅ 计算工具测试通过")
        else:
            print(f"❌ 计算工具测试失败: {result['error']}")
        
        print("\n🎉 快速测试完成！系统运行正常。")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False


def show_menu():
    """显示菜单"""
    
    print("\n" + "="*50)
    print("🎯 Langchain + MCP Server 项目启动器")
    print("="*50)
    print("请选择要执行的操作：")
    print()
    print("1. 🧪 快速功能测试")
    print("2. 📝 运行基础示例")
    print("3. 🚀 运行进阶示例") 
    print("4. 🔧 运行工具使用示例")
    print("5. 💬 启动交互式对话")
    print("6. 📊 查看系统状态")
    print("7. ❓ 查看帮助信息")
    print("8. 🚪 退出程序")
    print("="*50)


def run_examples():
    """运行示例程序"""
    
    print("\n📚 选择要运行的示例：")
    print("1. 基础示例 (basic_example.py)")
    print("2. 进阶示例 (advanced_example.py)")
    print("3. 工具使用示例 (tool_usage.py)")
    
    choice = input("\n请输入选择 (1-3): ").strip()
    
    if choice == "1":
        print("\n🚀 运行基础示例...")
        try:
            import examples.basic_example
            examples.basic_example.main()
        except Exception as e:
            print(f"❌ 运行失败: {str(e)}")
    
    elif choice == "2":
        print("\n🚀 运行进阶示例...")
        try:
            import examples.advanced_example
            examples.advanced_example.main()
        except Exception as e:
            print(f"❌ 运行失败: {str(e)}")
    
    elif choice == "3":
        print("\n🚀 运行工具使用示例...")
        try:
            import examples.tool_usage
            examples.tool_usage.main()
        except Exception as e:
            print(f"❌ 运行失败: {str(e)}")
    
    else:
        print("❌ 无效选择")


def start_interactive():
    """启动交互式对话"""
    
    print("\n💬 启动交互式对话模式...")
    try:
        import src.main
        src.main.main()
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")


def show_system_status():
    """显示系统状态"""
    
    print("\n📊 系统状态信息")
    print("="*40)
    
    try:
        from src.config import config
        from src.mcp_server import mcp_server
        from src.langchain_client import langchain_client
        
        # 配置信息
        print(f"🌐 API 地址: {config.api_base_url}")
        print(f"🤖 模型名称: {config.model_name}")
        print(f"📁 工作目录: {config.work_directory}")
        print(f"📊 日志级别: {config.log_level}")
        
        # 工具信息
        print(f"\n🔧 MCP Server 工具: {len(mcp_server.tools)} 个")
        for tool_name in mcp_server.tools.keys():
            print(f"   • {tool_name}")
        
        # 使用统计
        stats = mcp_server.get_usage_stats()
        print(f"\n📈 使用统计:")
        print(f"   总调用次数: {stats['total_calls']}")
        print(f"   最常用工具: {stats.get('most_used_tool', '无')}")
        
        # 检查文件系统
        workspace_files = os.listdir(config.work_directory)
        print(f"\n📁 工作目录文件: {len(workspace_files)} 个")
        for filename in workspace_files[:5]:  # 只显示前5个
            print(f"   • {filename}")
        if len(workspace_files) > 5:
            print(f"   ... 还有 {len(workspace_files) - 5} 个文件")
        
    except Exception as e:
        print(f"❌ 获取状态失败: {str(e)}")


def show_help():
    """显示帮助信息"""
    
    print("\n❓ 帮助信息")
    print("="*40)
    print("📚 项目结构:")
    print("   • src/          - 源代码目录")
    print("   • examples/     - 示例代码目录")
    print("   • workspace/    - 工作文件目录")
    print("   • README.md     - 项目说明")
    print("   • tutorial.md   - 详细教程")
    print()
    print("🚀 快速开始:")
    print("   1. 先运行快速测试确保系统正常")
    print("   2. 查看基础示例了解基本功能")
    print("   3. 尝试交互式对话体验完整功能")
    print("   4. 阅读教程了解更多详情")
    print()
    print("🔧 配置文件:")
    print("   • .env          - 环境变量配置")
    print("   • .env.example  - 配置模板")
    print()
    print("📖 更多信息:")
    print("   • 查看 README.md 了解项目概述")
    print("   • 查看 tutorial.md 学习详细教程")
    print("   • 查看示例代码了解具体用法")


def main():
    """主函数"""
    
    print("🎉 欢迎使用 Langchain + MCP Server 教学项目！")
    
    while True:
        try:
            show_menu()
            choice = input("\n请输入你的选择 (1-8): ").strip()
            
            if choice == "1":
                quick_test()
            
            elif choice == "2":
                run_examples()
            
            elif choice == "3":
                run_examples()  # 复用示例选择逻辑
            
            elif choice == "4":
                run_examples()  # 复用示例选择逻辑
            
            elif choice == "5":
                start_interactive()
            
            elif choice == "6":
                show_system_status()
            
            elif choice == "7":
                show_help()
            
            elif choice == "8":
                print("\n👋 谢谢使用，再见！")
                break
            
            else:
                print("❌ 无效选择，请输入 1-8 之间的数字")
            
            # 等待用户确认后继续
            if choice in ["1", "2", "3", "4", "6", "7"]:
                input("\n按回车键继续...")
        
        except KeyboardInterrupt:
            print("\n\n👋 检测到 Ctrl+C，正在退出...")
            break
        
        except Exception as e:
            print(f"\n❌ 发生错误: {str(e)}")
            input("按回车键继续...")


if __name__ == "__main__":
    main()
