# SonettoExoskeleton-LLM-CTF-Web-Helper

## 项目概述

**SonettoExoskeleton-LLM-CTF-Web-Helper** 是一款基于DeepSeek等OpenAI接口大语言模型构建的智能CTF Web半自动解题助手。它专为CTF（Capture The Flag）Web安全竞赛设计，通过AI驱动的交互方式，为安全爱好者和参赛者提供全方位的解题支持。

Sonetto**没有网页访问和工具使用能力**。她的定位是Exoskeleton“外骨骼”，辅助用户完成解题任务，而不是替代用户。

### 开发背景
随着网络安全竞赛的普及和Web安全漏洞的多样化，CTF参赛者需要快速分析题目、识别漏洞并找到解决方案。传统的解题过程往往依赖于个人经验和工具使用能力，而SonettoExoskeleton通过结合大语言模型的推理能力，为用户提供智能的解题指导，显著提升解题效率和学习效果。

### 适用场景
- CTF比赛训练和实战
- Web安全学习与教学
- 渗透测试技能提升
- 安全研究辅助工具

## 核心特性

### 基于大语言模型构建
- **OpenAI兼容API**：支持DeepSeek等主流大语言模型
- **上下文理解**：保持对话连贯性，理解解题过程的上下文
- **智能推理**：基于题目信息和工具输出进行分析推理

### 半自动辅助解题
- **实时指导**：提供专业的解题思路和步骤建议
- **漏洞分析**：识别Web安全漏洞，解释漏洞原理和利用方法
- **Flag定位**：引导用户逐步找到正确答案（flag）
- **自动Writeup生成**：会话结束后自动生成详细的解题报告

### Sonetto特有的解题模式
Sonetto采用"索取-提交-思考-再索取"的循环解题模式，具体流程如下：

1. **索取**：Sonetto根据当前状态，向用户索取必要的信息（如页面源码、工具输出等）
2. **提交**：用户按照Sonetto的要求提交相关信息
3. **思考**：Sonetto分析用户提交的信息，进行推理和分析
4. **再索取**：Sonetto基于分析结果，向用户索取更多信息或指导用户执行特定操作

这种模式模拟了真实的CTF解题过程，引导用户逐步深入分析，培养独立解题能力，同时提供必要的指导和支持。

## 工具链扩展功能

### 工具链集成
用户可以将自己已掌握的工具链集成到项目中，具体方法如下：

1. **编辑soul.md文件**：在文件中添加您的工具链信息，格式如下：

```markdown
**你可用的工具链（来自我的做题笔记）：**

- **工具名称** – 工具描述
- **工具名称**
  - 子工具1：功能描述
  - 子工具2：功能描述
```

2. **更新工具使用提示**：Sonetto会根据soul.md中的工具链信息，在需要时提供相应的使用提示和指导

### 陌生工具支持
当Sonetto遇到陌生工具时，它会：
1. 基于工具名称和描述理解工具的基本功能
2. 提供一般性的使用指导和最佳实践
3. 引导用户如何将工具输出与解题过程结合

## 安装与配置指南

### 环境要求
- Python 3.8+
- OpenAI Python 客户端库

### 安装步骤

1. **克隆项目到本地**：
   ```bash
   git clone https://github.com/yourusername/SonettoExoskeleton-CTF-Web-Helper.git
   cd SonettoExoskeleton-CTF-Web-Helper
   ```

2. **创建虚拟环境**：
   ```bash
   python -m venv venv
   ```

3. **激活虚拟环境**：
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **安装依赖**：
   ```bash
   pip install openai
   ```

### 配置

项目使用 `config.json` 文件存储 API 密钥和基础 URL 等敏感信息：

1. **复制配置文件模板**：
   ```bash
   cp config.json.example config.json
   ```

2. **编辑配置文件**：
   ```json
   {
     "api_key": "your_api_key_here",
     "base_url": "https://api.deepseek.com/v1"
   }
   ```

3. **安全提示**：`config.json` 文件包含敏感信息，请不要将其提交到版本控制系统中。建议在 `.gitignore` 文件中添加：
   ```
   config.json
   ```

## 使用示例

### 基本使用流程

1. **启动程序**：
   ```bash
   python main.py
   ```

2. **初始化会话**：程序会自动读取soul.md内容并初始化会话

3. **交互过程**：
   - **步骤1**：Sonetto会向您索取题目标题、注释和首页HTML源码
   - **步骤2**：您提供相关信息，Sonetto分析后给出下一步操作建议
   - **步骤3**：您执行Sonetto建议的操作并编辑communication.md，输入`go`提交结果
   - **步骤4**：Sonetto分析结果并给出新的建议，重复此过程直到找到flag

4. **生成Writeup**：输入 `退出`、`exit` 或 `quit` 退出程序并生成writeup

### 外骨骼辅助解题流程示例

**场景**：解决一个SQL注入题目

1. **Sonetto的索取**：
   > 请提供题目标题、题目注释和首页HTML源码

2. **用户提交-编辑communication.md并保存-输入go**：
   > 题目标题：SQL Injection Challenge
   > 题目注释：找到后台管理员密码
   > 首页HTML源码：`<form action="login.php" method="post"><input type="text" name="username"><input type="password" name="password"><input type="submit" value="Login"></form>`

3. **Sonetto的分析**：
   > 我发现这是一个可能存在SQL注入的登录表单。建议使用Burp Suite的Intruder工具测试SQL注入漏洞。

4. **用户执行操作并提交结果**：
   > 使用Burp Suite Intruder测试了' OR 1=1 -- 注入，成功登录，获得管理员密码：admin123

5. **Sonetto的总结**：
   > 很好！你成功利用SQL注入漏洞获取了管理员密码。现在可以使用这个密码登录后台获取flag。

6. **退出并生成Writeup**：
   > 输入 `退出` 后，程序会生成详细的解题writeup并保存到wp文件夹

## 技术架构

### 项目结构

```
SonettoExoskeleton-CTF-Web-Helper/
├── deepseek_client.py  # DeepSeek API客户端模块
├── file_utils.py       # 文件操作工具模块
├── main.py             # 程序入口文件
├── soul.md             # 会话初始化内容（包含工具链信息）
├── communication.md    # 模型回复存储
├── wp/                 # writeup存储目录
├── config.json         # 配置文件（API密钥等）
├── config.json.example # 配置文件模板
└── README.md           # 项目说明
```

### 核心组件

1. **deepseek_client.py**：
   - 负责与DeepSeek API的通信
   - 管理对话上下文
   - 生成writeup

2. **file_utils.py**：
   - 处理文件读写操作
   - 管理communication.md和soul.md文件

3. **main.py**：
   - 程序入口
   - 处理用户交互
   - 协调各模块工作

4. **soul.md**：
   - 定义Sonetto的角色和行为
   - 包含工具链信息

## 贡献指南

### 如何参与贡献

1. **Fork项目**：在GitHub上fork本项目到您的账号

2. **创建分支**：
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **提交更改**：
   ```bash
   git commit -m "Add your feature description"
   ```

4. **推送分支**：
   ```bash
   git push origin feature/your-feature-name
   ```

5. **创建Pull Request**：在GitHub上提交Pull Request，描述您的更改

### 代码规范

- 遵循PEP 8代码风格
- 为新功能添加文档字符串
- 确保代码通过基本测试

### Issue报告

如果您发现bug或有功能建议，请在GitHub上创建Issue，包括：
- 问题描述
- 复现步骤
- 预期行为
- 实际行为
- 环境信息

## 许可证信息

本项目采用 **MIT License** 开源许可证。详情请查看 [LICENSE](LICENSE) 文件。

## 致谢

- 感谢DeepSeek团队提供的大语言模型API
- 感谢所有为项目做出贡献的开发者
- 感谢CTF社区的支持和反馈

---

**SonettoExoskeleton-LLM-CTF-Web-Helper** - 让CTF解题更智能、更高效！

Miso. 于26年3.15创建工程。