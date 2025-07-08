"""
配置管理模块

这个模块负责管理整个应用程序的配置信息，包括：
- 从环境变量读取配置
- 提供默认值
- 验证配置的有效性
"""

import os
from typing import List, Optional
from dotenv import load_dotenv

# 加载环境变量文件
load_dotenv()


class Config:
    """
    配置类：管理所有应用程序配置
    
    这个类将所有配置集中管理，便于维护和修改
    """
    
    def __init__(self):
        """初始化配置，从环境变量读取设置"""
        
        # ===========================================
        # LLM API 相关配置
        # ===========================================
        
        # API 基础 URL
        self.api_base_url: str = os.getenv(
            "API_BASE_URL", 
            "http://xx.xx.xx.xxx:xxxx/v1"
        )
        
        # 使用的模型名称
        self.model_name: str = os.getenv(
            "MODEL_NAME", 
            "DeepSeek-V3-0324-HSW"
        )
        
        # API 请求超时时间（秒）
        self.api_timeout: int = int(os.getenv("API_TIMEOUT", "30"))
        
        # API 密钥（可选）
        self.api_key: Optional[str] = os.getenv("API_KEY")
        
        # ===========================================
        # MCP Server 相关配置
        # ===========================================
        
        # MCP Server 监听地址
        self.mcp_server_host: str = os.getenv("MCP_SERVER_HOST", "localhost")
        
        # MCP Server 监听端口
        self.mcp_server_port: int = int(os.getenv("MCP_SERVER_PORT", "8080"))
        
        # MCP Server 日志级别
        self.mcp_log_level: str = os.getenv("MCP_LOG_LEVEL", "INFO")
        
        # ===========================================
        # 应用程序配置
        # ===========================================
        
        # 应用日志级别
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        
        # 工作目录（用于文件操作）
        self.work_directory: str = os.getenv("WORK_DIRECTORY", "./workspace")
        
        # 最大文件大小（字节）
        self.max_file_size: int = int(os.getenv("MAX_FILE_SIZE", "1048576"))  # 1MB
        
        # ===========================================
        # 安全配置
        # ===========================================
        
        # 允许的文件扩展名
        allowed_extensions = os.getenv(
            "ALLOWED_FILE_EXTENSIONS", 
            ".txt,.md,.json,.csv,.log"
        )
        self.allowed_file_extensions: List[str] = [
            ext.strip() for ext in allowed_extensions.split(",")
        ]
        
        # 禁止访问的目录
        forbidden_dirs = os.getenv(
            "FORBIDDEN_DIRECTORIES", 
            "./,../,/etc,/var,C:\\Windows"
        )
        self.forbidden_directories: List[str] = [
            dir.strip() for dir in forbidden_dirs.split(",")
        ]
        
        # ===========================================
        # 性能配置
        # ===========================================
        
        # 连接池大小
        self.connection_pool_size: int = int(os.getenv("CONNECTION_POOL_SIZE", "10"))
        
        # 最大重试次数
        self.max_retries: int = int(os.getenv("MAX_RETRIES", "3"))
        
        # 缓存过期时间（秒）
        self.cache_expiry: int = int(os.getenv("CACHE_EXPIRY", "300"))
        
        # 初始化后验证配置
        self._validate_config()
        
        # 确保工作目录存在
        self._ensure_work_directory()
    
    def _validate_config(self) -> None:
        """
        验证配置的有效性
        
        检查重要配置是否正确设置，如果有问题会抛出异常
        """
        
        # 检查 API URL 格式
        if not self.api_base_url.startswith(("http://", "https://")):
            raise ValueError(f"API_BASE_URL 格式不正确: {self.api_base_url}")
        
        # 检查端口范围
        if not (1 <= self.mcp_server_port <= 65535):
            raise ValueError(f"MCP_SERVER_PORT 端口号无效: {self.mcp_server_port}")
        
        # 检查超时时间
        if self.api_timeout <= 0:
            raise ValueError(f"API_TIMEOUT 必须大于 0: {self.api_timeout}")
        
        # 检查日志级别
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.log_level.upper() not in valid_log_levels:
            raise ValueError(f"LOG_LEVEL 无效: {self.log_level}")
        
        print(f"✅ 配置验证通过")
    
    def _ensure_work_directory(self) -> None:
        """
        确保工作目录存在
        
        如果工作目录不存在，则创建它
        """
        if not os.path.exists(self.work_directory):
            os.makedirs(self.work_directory, exist_ok=True)
            print(f"📁 创建工作目录: {self.work_directory}")
        else:
            print(f"📁 工作目录已存在: {self.work_directory}")
    
    def get_api_headers(self) -> dict:
        """
        获取 API 请求头
        
        Returns:
            dict: 包含必要请求头的字典
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        # 如果有 API 密钥，添加到请求头
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        return headers
    
    def is_file_allowed(self, filename: str) -> bool:
        """
        检查文件是否允许访问
        
        Args:
            filename (str): 要检查的文件名
            
        Returns:
            bool: 如果文件允许访问返回 True，否则返回 False
        """
        # 检查文件扩展名
        _, ext = os.path.splitext(filename.lower())
        if ext not in self.allowed_file_extensions:
            return False
        
        # 检查是否在禁止目录中
        abs_path = os.path.abspath(filename)
        for forbidden_dir in self.forbidden_directories:
            if abs_path.startswith(os.path.abspath(forbidden_dir)):
                return False
        
        return True
    
    def print_config_summary(self) -> None:
        """
        打印配置摘要
        
        用于调试和确认配置是否正确
        """
        print("\n" + "="*50)
        print("📋 配置摘要")
        print("="*50)
        print(f"🌐 API 地址: {self.api_base_url}")
        print(f"🤖 模型名称: {self.model_name}")
        print(f"⏱️  API 超时: {self.api_timeout}秒")
        print(f"🏠 MCP 服务: {self.mcp_server_host}:{self.mcp_server_port}")
        print(f"📁 工作目录: {self.work_directory}")
        print(f"📊 日志级别: {self.log_level}")
        print(f"🔒 允许扩展名: {', '.join(self.allowed_file_extensions)}")
        print("="*50 + "\n")


# 创建全局配置实例
# 这样其他模块可以直接导入使用：from src.config import config
config = Config()

# 如果直接运行此文件，显示配置摘要
if __name__ == "__main__":
    config.print_config_summary()
