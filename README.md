# Sonetto CTF Web 解题助手

本项目是一个与 DeepSeek 大语言模型通信的工程，专注于CTF Web解题场景，提供了便捷的交互方式和writeup生成功能。

## 项目结构

```
SonettoExoskeleton/
├── deepseek_client.py  # DeepSeek API客户端模块
├── file_utils.py       # 文件操作工具模块
├── main.py             # 程序入口文件
├── soul.md             # 会话初始化内容
├── communication.md    # 模型回复存储
├── wp/                 # writeup存储目录
├── example.py          # 示例文件
├── venv/               # 虚拟环境
└── README.md           # 项目说明
```

## 功能特点

- 封装了与 DeepSeek API 的通信逻辑
- 模块化设计，职责分明
- 支持上下文对话
- 自动生成CTF Web解题writeup
- 终端仅显示必要的日志信息，模型回复写入communication.md
- 退出时自动生成writeup并保存到wp文件夹

## 环境要求

- Python 3.8+
- OpenAI Python 客户端库

## 安装步骤

1. 克隆项目到本地
2. 创建虚拟环境：
   ```bash
   python -m venv venv
   ```
3. 激活虚拟环境：
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. 安装依赖：
   ```bash
   pip install openai
   ```

## 配置

项目使用 `config.json` 文件存储 API 密钥和基础 URL 等敏感信息。

1. 复制 `config.json.example` 文件并重命名为 `config.json`
2. 编辑 `config.json` 文件，填入您的 DeepSeek API 密钥：

```json
{
  "api_key": "your_api_key_here",
  "base_url": "https://api.deepseek.com/v1"
}
```

**注意**：`config.json` 文件包含敏感信息，请不要将其提交到版本控制系统中。

## 使用方法

### 运行主程序

```bash
python main.py
```

程序会自动初始化会话，并等待用户输入。您可以：
- 直接输入问题或信息
- 输入 `go` 发送 communication.md 文件内容给模型
- 输入 `退出`、`exit` 或 `quit` 退出程序并生成writeup

### 模块说明

#### deepseek_client.py
- **`get_response(prompt: str) -> str`**：向大模型发送新消息和历史上下文，并阻塞地返回大模型结果
- **`clear_context() -> None`**：清空当前保存的上下文
- **`begin_session() -> str`**：开始一个新会话，先清空上下文，再将soul.md发送给大模型并返回其结果
- **`generate_writeup() -> str`**：根据上下文生成详细的CTF Web解题writeup

#### file_utils.py
- **`read_communication_content() -> str`**：读取communication.md文件，返回第二个三级标题之后的所有内容
- **`write_to_communication(content, title="模型回复")`**：将内容写入communication.md文件，每次写入前先清空文件
- **`clear_communication_file()`**：清空communication.md文件
- **`read_soul_content() -> str`**：读取soul.md文件内容

## 工作流程

1. 程序启动后，自动初始化会话，读取soul.md内容并发送给模型
2. 模型回复写入communication.md文件，终端只显示必要的日志信息
3. 用户可以输入问题或信息，模型回复会更新到communication.md
4. 用户输入 `go` 时，程序会读取communication.md的内容并发送给模型
5. 用户输入 `退出` 等指令时，程序会生成writeup并保存到wp文件夹

## 注意事项

- 请确保您已经获取了 DeepSeek API 密钥
- 对话上下文会保存在内存中，重启程序后会丢失
- writeup会以时间戳命名，保存到wp文件夹中
- 如需更复杂的上下文管理，可以考虑使用数据库或文件存储
