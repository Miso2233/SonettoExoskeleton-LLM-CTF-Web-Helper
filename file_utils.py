"""
文件操作工具模块

该模块包含与文件操作相关的函数，主要用于处理communication.md和soul.md文件的读写操作。
"""

def read_communication_content():
    """
    读取communication.md文件，返回第二个三级标题之后的所有内容
    
    Returns:
        第二个三级标题之后的内容
    """
    try:
        with open('communication.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 分割内容，找到所有三级标题
        sections = content.split('### ')
        
        # 如果有至少三个部分（包括空字符串），则返回第二个三级标题之后的内容
        if len(sections) >= 3:
            # 重新组合内容，从第二个三级标题开始
            result = '### '.join(sections[2:])
            return result
        else:
            return ""
    except FileNotFoundError:
        return ""

def write_to_communication(content, title="模型回复"):
    """
    将内容写入communication.md文件，每次写入前先清空文件
    
    Args:
        content: 要写入的内容
        title: 内容的标题
    """
    # 先清空文件
    with open('communication.md', 'w', encoding='utf-8') as f:
        f.write(f"### {title}\n{content}\n\n")

def clear_communication_file():
    """
    清空communication.md文件
    """
    with open('communication.md', 'w', encoding='utf-8') as f:
        f.write('')

def read_soul_content():
    """
    读取soul.md文件内容
    
    Returns:
        soul.md文件的内容
    """
    with open('soul.md', 'r', encoding='utf-8') as f:
        return f.read()
