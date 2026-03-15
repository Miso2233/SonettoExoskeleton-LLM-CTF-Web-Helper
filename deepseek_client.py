"""
DeepSeek API客户端模块

该模块包含与DeepSeek大模型通信相关的函数，负责发送请求和处理响应。
"""

import json
from openai import OpenAI
from file_utils import read_soul_content

# 全局变量用于存储上下文
conversation_history = []

# 从配置文件读取API密钥和基础URL
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 配置DeepSeek API客户端
client = OpenAI(
    api_key=config['api_key'],
    base_url=config['base_url']
)

def get_response(prompt: str) -> str:
    """
    向大模型发送新消息和历史上下文，并阻塞地返回大模型结果
    
    Args:
        prompt: 用户输入的新消息
    
    Returns:
        大模型的回复
    """
    # 将新消息添加到上下文
    conversation_history.append({"role": "user", "content": prompt})
    
    # 调用DeepSeek API
    response = client.chat.completions.create(
        model="deepseek-chat",  # 使用DeepSeek的聊天模型
        messages=conversation_history,
        temperature=0.7,
        max_tokens=1024
    )
    
    # 提取回复内容
    assistant_response = response.choices[0].message.content
    
    # 将助手回复添加到上下文
    conversation_history.append({"role": "assistant", "content": assistant_response})
    
    return assistant_response

def clear_context() -> None:
    """
    清空当前保存的上下文
    """
    global conversation_history
    conversation_history = []

def begin_session() -> str:
    """
    开始一个新会话，先清空上下文，再将soul.md发送给大模型并返回其结果
    
    Returns:
        大模型的回复
    """
    # 清空上下文
    clear_context()
    
    # 读取soul.md文件内容
    soul_content = read_soul_content()
    
    # 将soul.md内容发送给大模型并返回结果
    return get_response(soul_content)

def generate_writeup() -> str:
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
    writeup_content = get_response(prompt)
    
    return writeup_content
