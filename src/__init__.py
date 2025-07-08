# src 包的初始化文件
# 这个文件让 Python 将 src 目录识别为一个包

__version__ = "1.0.0"
__author__ = "Langchain MCP Tutorial Team"
__description__ = "一个简单的 Langchain 0.3 + MCP Server 入门教程项目"

# 模块可以在需要时导入，这里不做预导入以避免循环依赖
# 使用方式：
# from src.config import config
# from src.mcp_server import mcp_server
# from src.langchain_client import langchain_client

__all__ = [
    "__version__",
    "__author__", 
    "__description__"
]
