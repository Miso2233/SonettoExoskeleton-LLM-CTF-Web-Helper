"""
DeepSeek API客户端模块

该模块包含与DeepSeek大模型通信相关的类和方法，负责发送请求和处理响应。
"""

import json
from openai import OpenAI
from src.file_utils import generate_soul

class MODES:
    BOOST = "boost"
    COACH = "coach"
    COPILOT = "copilot"
    FULL_POWER = "full_power"

DEFAULT_MODE = json.load(open('config.json', 'r', encoding='utf-8'))['mode']

MAX_OUTPUT_TOKENS = 4096

MAX_INPUT_TOKENS = 64000

class Sonetto:
    """
    DeepSeek大模型客户端类
    
    封装了与DeepSeek大模型通信的所有功能，包括：
    - 上下文管理
    - 发送请求
    - 会话管理
    - Writeup生成
    """
    
    def __init__(self):
        """
        初始化Model类
        
        加载配置文件，创建OpenAI客户端，初始化会话历史
        """
        # 从配置文件读取API密钥和基础URL
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 配置DeepSeek API客户端
        self.client = OpenAI(
            api_key=config['api_key'],
            base_url=config['base_url']
        )
        
        # 初始化会话历史
        self.conversation_history = []

        self.mode = DEFAULT_MODE
    
    def get_response(self, prompt: str) -> str:
        """
        向大模型发送新消息和历史上下文，并阻塞地返回大模型结果
        
        Args:
            prompt: 用户输入的新消息
        
        Returns:
            大模型的回复
        """
        # 将新消息添加到上下文
        self.conversation_history.append({"role": "user", "content": prompt})
        
        # 调用DeepSeek API
        response = self.client.chat.completions.create(
            model="deepseek-chat",  # 使用DeepSeek的聊天模型
            messages=self.conversation_history,
            temperature=0.7,
            max_tokens=MAX_OUTPUT_TOKENS
        )
        
        # 提取回复内容
        assistant_response = response.choices[0].message.content
        
        # 将Sonetto回复添加到上下文
        self.conversation_history.append({"role": "assistant", "content": assistant_response})
        
        return assistant_response
    
    def clear_context(self) -> None:
        """
        清空当前保存的上下文
        """
        self.conversation_history = []
    
    def begin_session(self) -> str:
        """
        开始一个新会话，先清空上下文，再将soul.md发送给大模型并返回其结果
        
        Returns:
            大模型的回复
        """
        # 清空上下文
        self.clear_context()
        
        # 读取soul.md文件内容
        soul_content = generate_soul(self.mode)
        
        # 将soul.md内容发送给大模型并返回结果
        return self.get_response(soul_content)
    
    def generate_writeup(self) -> str:
        """
        根据上下文生成writeup

        Returns:
            生成的writeup内容
        """
        # 构建生成writeup的提示
        prompt = "请根据我们之前的对话内容，撰写一篇详细的CTF Web解题writeup。writeup应包括：\n" \
                 "1. 题目分析\n" \
                 "2. 解题思路\n" \
                 "3. 具体步骤\n" \
                 "4. 漏洞原理\n" \
                 "5. 解决方案\n" \
                 "请确保writeup内容详细、专业，并且逻辑清晰。"
        
        # 调用模型生成writeup
        writeup_content = self.get_response(prompt)
        
        return writeup_content
    
    def switch_mode(self, mode: str) -> None:
        """
        切换模型模式

        Args:
            mode: 新的模型模式
        """
        # 更新模式
        self.mode = mode
        
        # 生成新的灵魂
        soul_content = generate_soul(mode)
        
        # 替换最早一条用户信息（即灵魂信息）
        if self.conversation_history:
            # 查找第一条用户消息（通常是灵魂信息）
            for i, message in enumerate(self.conversation_history):
                if message.get('role') == 'user':
                    self.conversation_history[i]['content'] = soul_content
                    break
        else:
            # 如果没有历史记录，直接添加灵魂信息
            self.conversation_history.append({"role": "user", "content": soul_content})
    
    def estimate_context_tokens(self) -> float:
        """
        估算当前上下文的token数量占窗口最大值的比例

        Returns:
            估算的token占用比例
        """
        total_chars = 0
        
        # 遍历所有对话历史
        for message in self.conversation_history:
            if 'content' in message:
                total_chars += len(message['content'])
        
        # 简单估算：1个token约等于3个字符
        # 对于英文文本，通常1个token约等于4个字符
        # 对于中文文本，通常1个token约等于2个字符
        # 取平均值3个字符/token
        estimated_tokens = total_chars // 3
        
        # 为安全起见，添加一些额外的token用于系统消息和格式
        estimated_tokens += 100
        
        return estimated_tokens / MAX_INPUT_TOKENS
