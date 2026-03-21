"""
文件操作工具模块

该模块包含与文件操作相关的类和函数，主要用于处理：
- communication.md文件的读写操作（通过CommunicationManager类）
- soul.md系列文件的拼接和生成（通过generate_soul函数）
- 模式定义（通过MODES类）
"""
import json
import os
import time

class MODES:
    BOOST = "boost"
    COACH = "coach"
    COPILOT = "copilot"
    FULL_POWER = "full_power"

DEFAULT_MODE = json.load(open('config.json', 'r', encoding='utf-8'))['mode']

class CommunicationManager:
    """
    通信文件管理类
    
    负责处理communication.md文件的读写操作
    """
    
    def read(self):
        """
        读取communication.md文件，返回整个文件的内容
        
        Returns:
            整个文件的内容
        """
        try:
            with open('communication.md', 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except FileNotFoundError:
            return ""
    
    def write(self, content, title="下一步"):
        """
        将内容写入communication.md文件，每次写入前先清空文件
        
        Args:
            content: 要写入的内容
            title: 内容的标题
        """
        # 先清空文件
        with open('communication.md', 'w', encoding='utf-8') as f:
            f.write(f"### {title}\n{content}\n\n")
    
    def clear(self):
        """
        清空communication.md文件
        如果文件不存在，自动创建
        """
        # 无论文件是否存在，使用'w'模式都会创建或截断文件
        with open('communication.md', 'w', encoding='utf-8') as f:
            f.write('')

# 创建全局实例
communication_manager = CommunicationManager()

def save_writeup(content: str) -> None:
    """
    保存writeup到文件
    
    Args:
        content: writeup内容
    """
    # 创建wp文件夹（如果不存在）
    os.makedirs('wp', exist_ok=True)
    
    # 生成时间戳文件名
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    writeup_filename = f'wp/{timestamp}_writeup.md'
    
    # 保存writeup到文件
    with open(writeup_filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\nwriteup已保存到: {writeup_filename}")

def generate_soul(mode):
    """
    根据mode建立soul

    Args:
        mode: 模式，可选值：boost、coach、copilot、full_power

    Returns:
        根据选定的模式建立好的soul文本
    """
    out = ""
    with open('soul/soul.md', 'r', encoding='utf-8') as f:
        out += f.read()
    match mode:
        case MODES.BOOST:
            out += open('soul/boost.md', 'r', encoding='utf-8').read()
        case MODES.COACH:
            out += open('soul/coach.md', 'r', encoding='utf-8').read()
        case MODES.COPILOT:
            out += open('soul/copilot.md', 'r', encoding='utf-8').read()
        case MODES.FULL_POWER:
            out += open('soul/full_power.md', 'r', encoding='utf-8').read()
        case _:
            raise ValueError(f"Invalid mode: {mode}")
    out += open('soul/format.md', 'r', encoding='utf-8').read()
    return out