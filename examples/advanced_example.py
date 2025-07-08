"""
进阶示例：复杂工作流和错误处理

这个示例展示了更复杂的使用场景，包括：
1. 复杂的多步骤工作流
2. 错误处理和恢复
3. 批量操作
4. 自定义工具的使用

学习目标：
1. 理解复杂工作流的设计
2. 学会错误处理和恢复策略
3. 掌握批量操作的方法
4. 了解如何扩展系统功能
"""

import sys
import os
import json
import time
from typing import List, Dict, Any

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.config import config
from src.mcp_server import mcp_server
from src.langchain_client import langchain_client


class AdvancedWorkflow:
    """
    进阶工作流类
    
    这个类展示了如何构建复杂的工作流，包括错误处理和状态管理
    """
    
    def __init__(self):
        """初始化工作流"""
        self.workflow_state = {
            "current_step": 0,
            "completed_steps": [],
            "failed_steps": [],
            "results": {},
            "start_time": time.time()
        }
        
        print("🔄 初始化进阶工作流")
    
    def execute_step(self, step_name: str, message: str, required: bool = True) -> bool:
        """
        执行工作流步骤
        
        Args:
            step_name (str): 步骤名称
            message (str): 要发送给 AI 的消息
            required (bool): 是否为必需步骤
            
        Returns:
            bool: 步骤是否成功执行
        """
        
        print(f"\n🔸 执行步骤: {step_name}")
        print(f"📝 任务: {message}")
        
        try:
            # 执行步骤
            result = langchain_client.chat(message)
            
            if result["success"]:
                print(f"✅ 步骤 '{step_name}' 执行成功")
                
                # 记录成功步骤
                self.workflow_state["completed_steps"].append(step_name)
                self.workflow_state["results"][step_name] = result
                
                return True
            else:
                print(f"❌ 步骤 '{step_name}' 执行失败: {result['error']}")
                
                # 记录失败步骤
                self.workflow_state["failed_steps"].append({
                    "step": step_name,
                    "error": result["error"],
                    "required": required
                })
                
                # 如果是必需步骤，返回失败
                if required:
                    return False
                else:
                    print("⚠️ 非必需步骤失败，继续执行...")
                    return True
        
        except Exception as e:
            print(f"❌ 步骤 '{step_name}' 发生异常: {str(e)}")
            
            self.workflow_state["failed_steps"].append({
                "step": step_name,
                "error": str(e),
                "required": required
            })
            
            return not required
    
    def get_workflow_summary(self) -> Dict[str, Any]:
        """获取工作流摘要"""
        
        total_time = time.time() - self.workflow_state["start_time"]
        
        return {
            "total_steps": len(self.workflow_state["completed_steps"]) + len(self.workflow_state["failed_steps"]),
            "completed_steps": len(self.workflow_state["completed_steps"]),
            "failed_steps": len(self.workflow_state["failed_steps"]),
            "success_rate": len(self.workflow_state["completed_steps"]) / max(1, len(self.workflow_state["completed_steps"]) + len(self.workflow_state["failed_steps"])) * 100,
            "total_time": total_time,
            "state": self.workflow_state
        }


def workflow_1_data_analysis():
    """工作流 1：数据分析和报告生成"""
    
    print("\n" + "="*60)
    print("📊 工作流 1：数据分析和报告生成")
    print("="*60)
    print("🎯 目标：生成销售数据分析报告")
    
    workflow = AdvancedWorkflow()
    
    # 步骤 1：创建示例数据
    success = workflow.execute_step(
        "创建数据",
        "请创建一个名为 sales_data.txt 的文件，内容包含以下销售数据：\n"
        "产品A: 销量100, 价格50, 总收入5000\n"
        "产品B: 销量150, 价格30, 总收入4500\n"
        "产品C: 销量80, 价格75, 总收入6000"
    )
    
    if not success:
        print("❌ 数据创建失败，工作流终止")
        return
    
    # 步骤 2：计算总销量
    success = workflow.execute_step(
        "计算总销量",
        "请计算总销量：100 + 150 + 80"
    )
    
    # 步骤 3：计算总收入
    success = workflow.execute_step(
        "计算总收入",
        "请计算总收入：5000 + 4500 + 6000"
    )
    
    # 步骤 4：生成分析报告
    success = workflow.execute_step(
        "生成报告",
        "请创建一个名为 sales_report.txt 的文件，包含销售分析报告。"
        "报告应该包括：总销量330件，总收入15500元，平均价格约47元"
    )
    
    # 步骤 5：生成时间戳（可选步骤）
    workflow.execute_step(
        "添加时间戳",
        "请获取当前时间并将其添加到报告文件的末尾",
        required=False
    )
    
    # 显示工作流摘要
    summary = workflow.get_workflow_summary()
    print(f"\n📋 工作流摘要:")
    print(f"   总步骤: {summary['total_steps']}")
    print(f"   成功步骤: {summary['completed_steps']}")
    print(f"   失败步骤: {summary['failed_steps']}")
    print(f"   成功率: {summary['success_rate']:.1f}%")
    print(f"   总耗时: {summary['total_time']:.2f}秒")


def workflow_2_file_management():
    """工作流 2：文件管理和整理"""
    
    print("\n" + "="*60)
    print("📁 工作流 2：文件管理和整理")
    print("="*60)
    print("🎯 目标：创建和整理多个测试文件")
    
    workflow = AdvancedWorkflow()
    
    # 要创建的文件列表
    files_to_create = [
        ("note1.txt", "这是第一个笔记文件"),
        ("note2.txt", "这是第二个笔记文件"),
        ("data.txt", "这是数据文件"),
        ("config.txt", "这是配置文件"),
        ("log.txt", "这是日志文件")
    ]
    
    # 批量创建文件
    for i, (filename, content) in enumerate(files_to_create, 1):
        success = workflow.execute_step(
            f"创建文件{i}",
            f"请创建文件 {filename}，内容为：{content}",
            required=False  # 单个文件创建失败不影响整体流程
        )
    
    # 列出所有文件
    workflow.execute_step(
        "列出文件",
        "请列出工作目录中的所有文件，并统计文件数量"
    )
    
    # 创建文件清单
    workflow.execute_step(
        "创建清单",
        "请创建一个名为 file_inventory.txt 的文件，"
        "列出所有刚才创建的文件及其用途"
    )
    
    # 计算文件统计
    workflow.execute_step(
        "统计分析",
        "请计算创建的文件总数（应该是5个文件加上清单文件）"
    )
    
    # 显示工作流摘要
    summary = workflow.get_workflow_summary()
    print(f"\n📋 工作流摘要:")
    print(f"   成功创建文件: {summary['completed_steps'] - 1}")  # 减去列表步骤
    print(f"   成功率: {summary['success_rate']:.1f}%")


def workflow_3_mathematical_sequence():
    """工作流 3：数学序列计算"""
    
    print("\n" + "="*60)
    print("🧮 工作流 3：数学序列计算")
    print("="*60)
    print("🎯 目标：计算斐波那契数列并分析")
    
    workflow = AdvancedWorkflow()
    
    # 计算斐波那契数列的前几项
    fib_calculations = [
        ("第1项", "计算斐波那契数列第1项：1"),
        ("第2项", "计算斐波那契数列第2项：1"),
        ("第3项", "计算：1 + 1"),
        ("第4项", "计算：1 + 2"),
        ("第5项", "计算：2 + 3"),
        ("第6项", "计算：3 + 5"),
        ("第7项", "计算：5 + 8"),
        ("第8项", "计算：8 + 13")
    ]
    
    results = []
    for step_name, calculation in fib_calculations:
        success = workflow.execute_step(
            step_name,
            f"请{calculation}",
            required=False
        )
        
        if success:
            # 这里可以提取计算结果，但为了简化，我们只记录成功
            results.append(step_name)
    
    # 生成序列分析
    workflow.execute_step(
        "序列分析",
        "请创建一个名为 fibonacci_analysis.txt 的文件，"
        "包含斐波那契数列的前8项：1, 1, 2, 3, 5, 8, 13, 21，"
        "并说明这个数列的特点"
    )
    
    # 计算黄金比例近似值
    workflow.execute_step(
        "黄金比例",
        "请计算 21/13 的值，这是斐波那契数列相邻项比值的近似黄金比例"
    )
    
    # 显示摘要
    summary = workflow.get_workflow_summary()
    print(f"\n📋 数学工作流摘要:")
    print(f"   计算步骤: {len(fib_calculations)}")
    print(f"   成功计算: {len(results)}")
    print(f"   计算成功率: {len(results)/len(fib_calculations)*100:.1f}%")


def demonstrate_error_handling():
    """演示错误处理"""
    
    print("\n" + "="*60)
    print("🚨 错误处理演示")
    print("="*60)
    print("🎯 目标：演示系统如何处理各种错误情况")
    
    # 测试文件访问错误
    print("\n🔸 测试文件访问错误")
    result = langchain_client.chat("请读取一个不存在的文件：nonexistent.txt")
    print(f"结果: {'成功' if result['success'] else '失败（预期）'}")
    
    # 测试计算错误
    print("\n🔸 测试计算错误")
    result = langchain_client.chat("请计算一个无效的表达式：abc + def")
    print(f"结果: {'成功' if result['success'] else '失败（预期）'}")
    
    # 测试恢复策略
    print("\n🔸 测试错误恢复")
    result = langchain_client.chat("上一个计算失败了，请改为计算简单的加法：2 + 3")
    print(f"恢复结果: {'成功' if result['success'] else '失败'}")
    
    print("\n💡 错误处理演示完成。系统能够：")
    print("   • 优雅地处理文件不存在错误")
    print("   • 识别并报告无效的计算表达式")
    print("   • 在错误后继续正常工作")


def performance_benchmark():
    """性能基准测试"""
    
    print("\n" + "="*60)
    print("⚡ 性能基准测试")
    print("="*60)
    
    # 测试不同类型操作的性能
    operations = [
        ("简单计算", "计算 2 + 2"),
        ("复杂计算", "计算 2**10 + 3**5 - 4*7"),
        ("文件创建", "创建文件 perf_test.txt，内容为 'performance test'"),
        ("文件读取", "读取 perf_test.txt 文件内容"),
        ("时间获取", "获取当前时间"),
        ("随机数生成", "生成一个 1-100 的随机数")
    ]
    
    performance_results = []
    
    for op_name, message in operations:
        print(f"\n🔸 测试: {op_name}")
        
        start_time = time.time()
        result = langchain_client.chat(message)
        end_time = time.time()
        
        execution_time = end_time - start_time
        performance_results.append({
            "operation": op_name,
            "success": result["success"],
            "time": execution_time
        })
        
        print(f"   耗时: {execution_time:.3f}秒")
        print(f"   状态: {'成功' if result['success'] else '失败'}")
    
    # 分析性能结果
    print(f"\n📊 性能分析:")
    successful_ops = [r for r in performance_results if r["success"]]
    if successful_ops:
        avg_time = sum(r["time"] for r in successful_ops) / len(successful_ops)
        fastest = min(successful_ops, key=lambda x: x["time"])
        slowest = max(successful_ops, key=lambda x: x["time"])
        
        print(f"   平均响应时间: {avg_time:.3f}秒")
        print(f"   最快操作: {fastest['operation']} ({fastest['time']:.3f}秒)")
        print(f"   最慢操作: {slowest['operation']} ({slowest['time']:.3f}秒)")
        print(f"   成功率: {len(successful_ops)}/{len(performance_results)} ({len(successful_ops)/len(performance_results)*100:.1f}%)")


def main():
    """主函数：运行所有进阶示例"""
    
    print("🚀 Langchain + MCP Server 进阶示例")
    print("="*60)
    print("📚 这个示例展示复杂工作流、错误处理和性能测试")
    print("💡 观察系统如何处理复杂任务和错误情况")
    print("="*60)
    
    try:
        # 运行复杂工作流
        workflow_1_data_analysis()
        workflow_2_file_management()
        workflow_3_mathematical_sequence()
        
        # 演示错误处理
        demonstrate_error_handling()
        
        # 性能基准测试
        performance_benchmark()
        
        # 最终统计
        print("\n" + "="*60)
        print("📊 进阶示例总结")
        print("="*60)
        
        final_stats = langchain_client.get_usage_stats()
        print(f"本次运行工具调用总数: {final_stats['total_calls']}")
        print(f"最常用工具: {final_stats.get('most_used_tool', '无')}")
        
        print("\n✅ 所有进阶示例运行完成！")
        print("💡 从这些示例中你应该学到：")
        print("   • 如何设计复杂的多步骤工作流")
        print("   • 系统的错误处理和恢复能力")
        print("   • 不同操作的性能特征")
        print("   • 批量操作和状态管理的方法")
        
    except Exception as e:
        print(f"\n❌ 进阶示例运行失败: {str(e)}")
        print("💡 请检查系统状态和配置")


if __name__ == "__main__":
    main()
