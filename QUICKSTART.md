# 快速开始指南

## 🚀 5分钟快速上手

### 第一步：检查环境

```bash
# 检查 Python 版本（需要 3.8+）
python --version

# 检查 pip
pip --version
```

### 第二步：安装依赖

```bash
# 进入项目目录
cd Langchain-MCP

# 安装依赖包
pip install -r requirements.txt
```

### 第三步：配置环境

```bash
# 复制配置文件
copy .env.example .env

# 编辑 .env 文件，确保 API 配置正确
# API_BASE_URL=http://xx.xx.xx.xxx:xxxx/v1
# MODEL_NAME=DeepSeek-V3-0324-HSW
```

### 第四步：快速测试

```bash
# 运行快速测试
python run.py
# 选择选项 1 进行快速功能测试
```

### 第五步：体验功能

```bash
# 运行基础示例
python examples/basic_example.py

# 或者启动交互式对话
python src/main.py
```

## 🎯 主要功能

- **📁 文件操作**: 创建、读取、列出文件
- **🧮 数学计算**: 基础运算、随机数生成
- **⏰ 时间处理**: 获取时间、格式化时间戳
- **🤖 智能对话**: 自然语言工具调用

## 📚 学习路径

1. **运行 `python run.py`** - 快速体验所有功能
2. **阅读 `tutorial.md`** - 深入了解技术细节
3. **查看示例代码** - 学习具体实现方法
4. **尝试修改代码** - 添加自己的功能

## 🔧 故障排除

### 依赖安装失败
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### API 连接失败
- 检查 `.env` 文件中的 API 地址
- 确认网络连接正常
- 验证 API 服务状态

### 模块导入错误
```bash
# 确保在项目根目录运行
cd Langchain-MCP
python run.py
```

## 💡 使用技巧

- 使用清晰具体的指令
- 组合多个工具完成复杂任务
- 查看执行日志了解工具调用过程
- 定期清理工作目录中的临时文件

## 🎓 进阶学习

- 学习添加自定义 MCP 工具
- 探索更复杂的 Langchain 功能
- 了解 Model Context Protocol 标准
- 参与开源项目贡献

---

🎉 **恭喜！你已经成功搭建了 Langchain + MCP Server 系统！**
