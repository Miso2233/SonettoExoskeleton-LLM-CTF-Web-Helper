# SonettoExoskeleton-LLM-CTF-Web-Helper

## 项目概述

**SonettoExoskeleton-LLM-CTF-Web-Helper** 是一款基于DeepSeek等OpenAI接口大语言模型构建的智能CTF Web半自动解题助手。它专为CTF（Capture The Flag）Web安全竞赛设计，通过AI驱动的交互方式，为安全爱好者和参赛者提供全方位的解题支持。

Sonetto**没有网页访问和工具使用能力**。她的定位是Exoskeleton"外骨骼"，辅助用户完成解题任务，而不是替代用户。

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
   git clone https://github.com/yourusername/SonettoExoskeleton-LLM-CTF-Web-Helper.git
   cd SonettoExoskeleton-LLM-CTF-Web-Helper
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

## 使用指南

### 基本使用流程

1. **启动程序**：
   ```bash
   python main.py
   ```

2. **启动本地服务器**：
   ```bash
   python start_server.py
   ```

3. **访问前端页面**：在浏览器中打开 `http://localhost:8001/app.html`

4. **交互过程**：
   - **左侧栏**：显示Sonetto的指导内容
   - **右侧栏**：根据需要输入相关信息
   - **底部按钮**：
     - "下一步"：提交输入内容，系统会自动处理并获取Sonetto的回复
     - "结束"：结束会话并生成writeup

5. **自动文件管理**：
   - 系统会自动创建和管理 `communication.md` 文件
   - 页面会智能检测文件变化，只在需要时更新内容

### 前端界面功能

#### 界面布局
- **左侧栏**：显示Sonetto的指导内容，来自 `communication.md` 的"### 下一步"部分
- **右侧栏**：根据 `communication.md` 中的三级标题自动生成对应的输入框
- **底部按钮**：提供"下一步"和"结束"操作

#### 智能特性
- **自动文件创建**：如果 `communication.md` 文件不存在，系统会自动创建并初始化
- **智能更新检测**：页面每5秒检查一次文件变化，只在文件真正变化时更新
- **用户输入保持**：页面更新时会自动保存和恢复用户输入的内容
- **响应式设计**：适配不同屏幕尺寸，提供良好的移动端体验

### 解题流程示例

**场景**：解决一个SQL注入题目

1. **Sonetto的指导**：
   > 请提供题目标题、题目注释和首页HTML源码

2. **用户输入**：在右侧栏的对应输入框中填写信息
   > 题目标题：SQL Injection Challenge
   > 题目注释：找到后台管理员密码
   > 首页HTML源码：`<form action="login.php" method="post"><input type="text" name="username"><input type="password" name="password"><input type="submit" value="Login"></form>`

3. **提交信息**：点击"下一步"按钮

4. **Sonetto的分析**：
   > 我发现这是一个可能存在SQL注入的登录表单。建议使用Burp Suite的Intruder工具测试SQL注入漏洞。

5. **执行操作**：使用Burp Suite测试SQL注入，获得结果

6. **提交结果**：在右侧栏输入测试结果，点击"下一步"
   > 使用Burp Suite Intruder测试了' OR 1=1 -- 注入，成功登录，获得管理员密码：admin123

7. **Sonetto的指导**：
   > 很好！你成功利用SQL注入漏洞获取了管理员密码。现在可以使用这个密码登录后台获取flag。

8. **完成解题**：找到flag后，点击"结束"按钮生成writeup

## 技术架构

### 项目结构

```
SonettoExoskeleton-CTF-Web-Helper/
├── deepseek_client.py  # DeepSeek API客户端模块
├── file_utils.py       # 文件操作工具模块
├── main.py             # 程序入口文件
├── start_server.py     # 本地HTTP服务器
├── app.html            # 前端界面
├── style.css           # 前端样式
├── soul.md             # 会话初始化内容（包含工具链信息）
├── communication.md    # 模型回复存储（自动生成）
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
   - 处理与模型的交互
   - 协调各模块工作

4. **start_server.py**：
   - 提供本地HTTP服务器
   - 处理前端文件请求
   - 支持文件读写操作

5. **前端界面**：
   - app.html：前端页面结构
   - style.css：样式设计（支持响应式布局）

6. **soul.md**：
   - 定义Sonetto的角色和行为
   - 包含工具链信息

## 技术特色

### 前端技术
- **响应式设计**：适配不同屏幕尺寸
- **毛玻璃效果**：现代化的视觉设计
- **实时更新**：智能检测文件变化
- **用户友好**：直观的界面布局和交互

### 后端技术
- **模块化设计**：清晰的代码结构和职责分离
- **安全配置**：敏感信息分离存储
- **智能文件管理**：自动创建和更新文件
- **高效通信**：与大语言模型的优化交互

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
