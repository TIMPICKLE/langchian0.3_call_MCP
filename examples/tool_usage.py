"""
工具使用示例：深入理解 MCP 工具

这个示例专门展示如何使用各种 MCP 工具，包括：
1. 每个工具的详细使用方法
2. 参数配置和选项
3. 最佳实践和注意事项
4. 工具组合使用技巧

学习目标：
1. 掌握每个工具的具体用法
2. 了解工具的参数和选项
3. 学会工具的最佳实践
4. 理解工具组合的威力
"""

import sys
import os
import json
import time
from datetime import datetime

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.config import config
from src.mcp_server import mcp_server
from src.langchain_client import langchain_client


def demo_file_tools():
    """演示文件操作工具"""
    
    print("\n" + "="*60)
    print("📁 文件操作工具演示")
    print("="*60)
    
    print("\n🔧 工具 1: write_file - 文件写入")
    print("-" * 40)
    
    # 基础文件写入
    print("🔸 基础用法：创建简单文本文件")
    result = langchain_client.chat(
        "请创建一个名为 demo_basic.txt 的文件，内容是 'Hello, MCP World!'"
    )
    print(f"执行结果: {result['output'][:100]}...")
    
    # 多行文件写入
    print("\n🔸 进阶用法：创建多行内容文件")
    multi_line_content = """请创建一个名为 demo_multiline.txt 的文件，内容如下：
第一行：项目标题
第二行：作者信息
第三行：创建日期
第四行：版本号 1.0"""
    
    result = langchain_client.chat(multi_line_content)
    print(f"执行结果: {result['output'][:100]}...")
    
    # JSON 文件写入
    print("\n🔸 特殊用法：创建 JSON 格式文件")
    json_content = """请创建一个名为 demo_config.json 的文件，内容为：
{
    "app_name": "MCP Demo",
    "version": "1.0.0",
    "debug": true,
    "features": ["file_ops", "calculations", "time_tools"]
}"""
    
    result = langchain_client.chat(json_content)
    print(f"执行结果: {result['output'][:100]}...")
    
    print("\n🔧 工具 2: read_file - 文件读取")
    print("-" * 40)
    
    # 读取刚创建的文件
    files_to_read = ["demo_basic.txt", "demo_multiline.txt", "demo_config.json"]
    
    for filename in files_to_read:
        print(f"\n🔸 读取文件: {filename}")
        result = langchain_client.chat(f"请读取 {filename} 文件的内容")
        print(f"执行结果: {result['output'][:150]}...")
    
    print("\n🔧 工具 3: list_files - 文件列表")
    print("-" * 40)
    
    print("🔸 列出当前目录所有文件")
    result = langchain_client.chat("请列出工作目录中的所有文件，并显示详细信息")
    print(f"执行结果: {result['output'][:200]}...")
    
    # 文件操作总结
    print("\n💡 文件工具使用要点：")
    print("   • write_file: 支持任何文本格式，自动创建目录")
    print("   • read_file: 自动处理编码，支持大部分文本文件")
    print("   • list_files: 提供详细文件信息，包括大小和时间")


def demo_calculation_tools():
    """演示计算工具"""
    
    print("\n" + "="*60)
    print("🧮 计算工具演示")
    print("="*60)
    
    print("\n🔧 工具 1: calculate - 数学计算")
    print("-" * 40)
    
    # 基础四则运算
    basic_calculations = [
        "2 + 3",
        "10 - 4",
        "6 * 7",
        "15 / 3",
        "10 % 3"  # 取余
    ]
    
    print("🔸 基础四则运算：")
    for expr in basic_calculations:
        result = langchain_client.chat(f"请计算：{expr}")
        print(f"   {expr} = {result['output'].split('=')[-1].strip() if '=' in result['output'] else '计算中...'}")
    
    # 复杂数学运算
    complex_calculations = [
        "2**10",  # 幂运算
        "(25 + 75) * 2",  # 括号运算
        "100 / (5 + 5)",  # 分式运算
        "3**2 + 4**2",  # 勾股定理
        "((1 + 5**0.5) / 2)**2"  # 黄金比例的平方
    ]
    
    print("\n🔸 复杂数学运算：")
    for expr in complex_calculations:
        result = langchain_client.chat(f"请计算：{expr}")
        print(f"   {expr} 的结果在计算中...")
    
    # 数学常数和函数（受限）
    print("\n🔸 数学应用示例：")
    math_examples = [
        ("面积计算", "计算半径为5的圆的面积：3.14159 * 5**2"),
        ("体积计算", "计算边长为3的立方体体积：3**3"),
        ("平均值", "计算这些数的平均值：(85 + 92 + 78 + 88 + 95) / 5")
    ]
    
    for name, expr in math_examples:
        print(f"\n   {name}:")
        result = langchain_client.chat(f"请{expr}")
        print(f"   执行结果: {result['output'][:100]}...")
    
    print("\n🔧 工具 2: get_random_number - 随机数生成")
    print("-" * 40)
    
    # 不同范围的随机数
    random_examples = [
        ("标准随机数", "生成一个 1 到 100 之间的随机数"),
        ("小范围随机数", "生成一个 1 到 10 之间的随机数"),
        ("大范围随机数", "生成一个 1000 到 9999 之间的随机数"),
        ("骰子模拟", "生成一个 1 到 6 之间的随机数（模拟骰子）"),
        ("抽奖号码", "生成一个 1 到 1000 之间的随机数（模拟抽奖）")
    ]
    
    for name, description in random_examples:
        print(f"\n🔸 {name}")
        result = langchain_client.chat(description)
        print(f"   结果: {result['output'][:100]}...")
    
    # 计算工具总结
    print("\n💡 计算工具使用要点：")
    print("   • calculate: 支持基础数学运算，注意安全限制")
    print("   • get_random_number: 可指定范围，适合模拟和抽样")
    print("   • 组合使用: 可以先生成随机数，再进行计算")


def demo_time_tools():
    """演示时间工具"""
    
    print("\n" + "="*60)
    print("⏰ 时间工具演示")
    print("="*60)
    
    print("\n🔧 工具 1: get_current_time - 获取当前时间")
    print("-" * 40)
    
    # 不同格式的时间获取
    time_formats = [
        ("默认格式", "获取当前时间"),
        ("日期格式", "获取当前时间，格式为 年-月-日"),
        ("时间格式", "获取当前时间，格式为 时:分:秒"),
        ("完整格式", "获取当前时间，包含年月日时分秒"),
        ("中文格式", "获取当前时间，使用中文格式")
    ]
    
    for name, description in time_formats:
        print(f"\n🔸 {name}")
        result = langchain_client.chat(description)
        print(f"   结果: {result['output'][:150]}...")
    
    print("\n🔧 工具 2: format_timestamp - 时间戳格式化")
    print("-" * 40)
    
    # 不同时间戳的格式化
    timestamps = [
        (1640995200, "2022年新年时间戳"),
        (1672531200, "2023年新年时间戳"),
        (1704067200, "2024年新年时间戳"),
        (int(time.time()), "当前时间戳")
    ]
    
    for timestamp, description in timestamps:
        print(f"\n🔸 格式化 {description}")
        result = langchain_client.chat(
            f"请将时间戳 {timestamp} 格式化为可读的时间"
        )
        print(f"   结果: {result['output'][:150]}...")
    
    # 时间计算示例
    print("\n🔸 时间应用示例")
    time_applications = [
        "获取当前时间，并计算距离2024年1月1日已经过去多少天",
        "获取当前时间，并说明现在是星期几",
        "获取当前时间，并判断现在是上午还是下午"
    ]
    
    for i, application in enumerate(time_applications, 1):
        print(f"\n   应用 {i}:")
        result = langchain_client.chat(application)
        print(f"   结果: {result['output'][:150]}...")
    
    # 时间工具总结
    print("\n💡 时间工具使用要点：")
    print("   • get_current_time: 支持多种格式，包含详细时间信息")
    print("   • format_timestamp: 将时间戳转换为人类可读格式")
    print("   • 组合应用: 可与其他工具结合做时间相关计算")


def demo_tool_combinations():
    """演示工具组合使用"""
    
    print("\n" + "="*60)
    print("🔗 工具组合使用演示")
    print("="*60)
    
    print("\n🎯 组合场景 1：数据记录和分析")
    print("-" * 50)
    
    # 场景：记录实验数据并分析
    print("🔸 步骤 1：生成实验数据")
    result = langchain_client.chat(
        "生成3个1-100之间的随机数，代表三次实验的结果"
    )
    print(f"实验数据生成: {result['output'][:100]}...")
    
    print("\n🔸 步骤 2：计算数据统计")
    # 假设生成的随机数是 45, 67, 89（实际会不同）
    result = langchain_client.chat(
        "计算三个数 45, 67, 89 的平均值：(45 + 67 + 89) / 3"
    )
    print(f"统计计算: {result['output'][:100]}...")
    
    print("\n🔸 步骤 3：记录分析结果")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = langchain_client.chat(
        f"创建文件 experiment_log.txt，内容包含：\n"
        f"实验时间：{current_time}\n"
        f"实验数据：三次测量结果\n"
        f"统计分析：平均值计算\n"
        f"实验结论：数据分析完成"
    )
    print(f"结果记录: {result['output'][:100]}...")
    
    print("\n🎯 组合场景 2：自动化报告生成")
    print("-" * 50)
    
    # 场景：生成每日工作报告
    print("🔸 步骤 1：获取当前时间")
    result = langchain_client.chat("获取当前日期和时间")
    print(f"时间获取: {result['output'][:100]}...")
    
    print("\n🔸 步骤 2：计算工作统计")
    result = langchain_client.chat(
        "计算今日工作统计：完成任务8个，剩余任务2个，完成率为 8/(8+2)*100"
    )
    print(f"统计计算: {result['output'][:100]}...")
    
    print("\n🔸 步骤 3：生成报告文件")
    result = langchain_client.chat(
        "创建每日报告文件 daily_report.txt，包含：\n"
        "- 报告日期\n"
        "- 完成任务数量\n"
        "- 剩余任务数量\n"
        "- 完成率统计\n"
        "- 明日计划"
    )
    print(f"报告生成: {result['output'][:100]}...")
    
    print("\n🎯 组合场景 3：配置文件管理")
    print("-" * 50)
    
    # 场景：动态生成配置文件
    print("🔸 步骤 1：生成随机端口号")
    result = langchain_client.chat(
        "生成一个8000到9999之间的随机数，作为服务器端口号"
    )
    print(f"端口生成: {result['output'][:100]}...")
    
    print("\n🔸 步骤 2：创建配置文件")
    result = langchain_client.chat(
        "创建配置文件 server_config.json，包含随机生成的端口号和当前时间戳"
    )
    print(f"配置创建: {result['output'][:100]}...")
    
    print("\n🔸 步骤 3：验证配置文件")
    result = langchain_client.chat(
        "读取 server_config.json 文件内容，验证配置是否正确"
    )
    print(f"配置验证: {result['output'][:100]}...")
    
    # 组合使用总结
    print("\n💡 工具组合使用要点：")
    print("   • 数据流: 一个工具的输出可以作为另一个工具的输入")
    print("   • 状态保持: 在对话中保持上下文，引用之前的结果")
    print("   • 错误处理: 当一个步骤失败时，可以调整后续步骤")
    print("   • 自动化: 可以构建复杂的自动化工作流")


def demo_best_practices():
    """演示最佳实践"""
    
    print("\n" + "="*60)
    print("⭐ 工具使用最佳实践")
    print("="*60)
    
    print("\n📋 最佳实践 1：清晰的指令")
    print("-" * 40)
    
    # 对比好的和不好的指令
    examples = [
        {
            "类型": "文件操作",
            "不好的": "创建文件",
            "好的": "请创建一个名为 example.txt 的文件，内容是 'Hello World'",
            "说明": "明确指定文件名和内容"
        },
        {
            "类型": "计算",
            "不好的": "算一下", 
            "好的": "请计算 25 + 30 * 2 的结果",
            "说明": "提供完整的数学表达式"
        },
        {
            "类型": "时间",
            "不好的": "现在几点",
            "好的": "请获取当前时间，格式为 年-月-日 时:分:秒",
            "说明": "指定需要的时间格式"
        }
    ]
    
    for example in examples:
        print(f"\n🔸 {example['类型']}操作:")
        print(f"   ❌ 不好的指令: {example['不好的']}")
        print(f"   ✅ 好的指令: {example['好的']}")
        print(f"   💡 说明: {example['说明']}")
    
    print("\n📋 最佳实践 2：错误处理")
    print("-" * 40)
    
    # 演示错误处理策略
    print("🔸 策略 1：预检查")
    result = langchain_client.chat(
        "在创建文件之前，先列出目录内容，检查是否有同名文件"
    )
    print(f"预检查结果: {result['output'][:100]}...")
    
    print("\n🔸 策略 2：备选方案")
    print("如果主要操作失败，提供备选方案")
    result = langchain_client.chat(
        "如果无法创建 test.txt 文件，那么创建 backup.txt 文件作为替代"
    )
    print(f"备选方案: {result['output'][:100]}...")
    
    print("\n📋 最佳实践 3：性能优化")
    print("-" * 40)
    
    optimization_tips = [
        "批量操作：一次性处理多个相似任务",
        "结果缓存：避免重复计算相同的表达式",
        "简化请求：使用简洁明确的指令",
        "分步执行：将复杂任务分解为简单步骤"
    ]
    
    for i, tip in enumerate(optimization_tips, 1):
        print(f"   {i}. {tip}")
    
    print("\n📋 最佳实践 4：安全考虑")
    print("-" * 40)
    
    security_notes = [
        "文件操作：只在指定的工作目录内操作",
        "计算安全：避免使用危险的数学表达式",
        "数据验证：检查输入数据的合理性",
        "权限控制：理解工具的权限限制"
    ]
    
    for i, note in enumerate(security_notes, 1):
        print(f"   {i}. {note}")
    
    # 最佳实践总结
    print("\n💡 总结:")
    print("   • 清晰指令 = 更好结果")
    print("   • 错误处理 = 更稳定系统")
    print("   • 性能优化 = 更快响应")
    print("   • 安全意识 = 更可靠运行")


def main():
    """主函数：运行所有工具使用示例"""
    
    print("🚀 MCP 工具使用详细示例")
    print("="*60)
    print("🎯 这个示例将详细展示每个工具的使用方法")
    print("📚 包括基础用法、进阶技巧和最佳实践")
    print("="*60)
    
    try:
        # 演示各类工具
        demo_file_tools()
        demo_calculation_tools()
        demo_time_tools()
        
        # 演示工具组合
        demo_tool_combinations()
        
        # 演示最佳实践
        demo_best_practices()
        
        # 最终统计和建议
        print("\n" + "="*60)
        print("📊 工具使用示例总结")
        print("="*60)
        
        final_stats = langchain_client.get_usage_stats()
        print(f"本次演示工具调用总数: {final_stats['total_calls']}")
        
        print("\n🎓 学习成果:")
        print("   ✅ 掌握了所有基础工具的使用方法")
        print("   ✅ 了解了工具参数和配置选项")
        print("   ✅ 学会了工具组合使用技巧")
        print("   ✅ 理解了最佳实践和安全考虑")
        
        print("\n🔄 下一步建议:")
        print("   • 尝试创建自己的工具组合")
        print("   • 探索更复杂的工作流场景")
        print("   • 学习添加自定义工具")
        print("   • 参与项目开发和改进")
        
        print("\n📁 创建的演示文件:")
        result = langchain_client.chat("列出所有以 demo_ 开头的文件")
        print("请查看工作目录中的演示文件以了解具体效果")
        
    except Exception as e:
        print(f"\n❌ 工具演示失败: {str(e)}")
        print("💡 请检查系统配置和网络连接")


if __name__ == "__main__":
    main()
