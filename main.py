"""
Sonetto CTF Web 解题助手

程序入口文件，负责初始化会话和处理用户交互。
"""

import os
import time
from deepseek_client import begin_session, get_response, clear_context, generate_writeup
from file_utils import read_communication_content, write_to_communication, clear_communication_file

def main():
    print("=== Sonetto CTF Web 解题助手 ===")
    print("我是 Sonetto，一名网安专家，主攻 CTF Web 方向。")
    print("让我帮助你解决 CTF Web 题目。")
    print("\n初始化会话中...")
    
    # 清空communication.md文件
    clear_communication_file()
    
    # 初始化会话
    session_response = begin_session()
    print("\n会话初始化完成")
    
    # 将模型回复写入communication.md
    write_to_communication(session_response)
    
    # 开始交互循环
    # 记录communication.md的初始修改时间
    last_modified = 0
    try:
        last_modified = os.path.getmtime('communication.md')
    except FileNotFoundError:
        pass
    
    while True:
        print("\n等待输入...")
        print("（输入'退出'、'exit'或'quit'结束会话）")
        
        # 检查communication.md文件是否被修改
        try:
            current_modified = os.path.getmtime('communication.md')
            if current_modified > last_modified:
                print("\n检测到communication.md文件更新...")
                
                # 读取整个文件内容，检查是否包含退出标记
                with open('communication.md', 'r', encoding='utf-8') as f:
                    full_content = f.read()
                
                # 检查是否包含退出标记
                if 'EXIT_SESSION' in full_content:
                    print("\n检测到退出指令...")
                    print("生成writeup中...")
                    # 生成writeup
                    writeup_content = generate_writeup()
                    
                    # 创建wp文件夹（如果不存在）
                    os.makedirs('wp', exist_ok=True)
                    
                    # 生成时间戳文件名
                    timestamp = time.strftime('%Y%m%d_%H%M%S')
                    writeup_filename = f'wp/{timestamp}_writeup.md'
                    
                    # 保存writeup到文件
                    with open(writeup_filename, 'w', encoding='utf-8') as f:
                        f.write(writeup_content)
                    
                    print(f"\nwriteup已保存到: {writeup_filename}")
                    print("会话结束，再见！")
                    break
                
                # 正常处理通信内容
                communication_content = read_communication_content()
                if communication_content:
                    print("发送communication.md内容给模型...")
                    response = get_response(communication_content)
                    print("模型回复已写入communication.md")
                    # 将模型回复写入communication.md
                    write_to_communication(response)
                    # 更新最后修改时间
                    last_modified = os.path.getmtime('communication.md')
                else:
                    print("communication.md文件中没有足够的内容")
        except FileNotFoundError:
            pass
        
        # 检查用户输入
        import sys
        
        # 在Windows上使用msvcrt模块来检查键盘输入
        try:
            import msvcrt
            if msvcrt.kbhit():
                user_input = input("你: ")
                
                # 检查是否退出
                if user_input.lower() in ["退出", "exit", "quit"]:
                    print("\n生成writeup中...")
                    # 生成writeup
                    writeup_content = generate_writeup()
                    
                    # 创建wp文件夹（如果不存在）
                    os.makedirs('wp', exist_ok=True)
                    
                    # 生成时间戳文件名
                    timestamp = time.strftime('%Y%m%d_%H%M%S')
                    writeup_filename = f'wp/{timestamp}_writeup.md'
                    
                    # 保存writeup到文件
                    with open(writeup_filename, 'w', encoding='utf-8') as f:
                        f.write(writeup_content)
                    
                    print(f"\nwriteup已保存到: {writeup_filename}")
                    print("会话结束，再见！")
                    break
                
                # 发送用户输入给大模型并获取回复
                response = get_response(user_input)
                print("模型回复已写入communication.md")
                # 将模型回复写入communication.md
                write_to_communication(response)
                # 更新最后修改时间
                last_modified = os.path.getmtime('communication.md')
        except ImportError:
            # 在非Windows系统上使用select
            import select
            if select.select([sys.stdin], [], [], 0.1)[0]:
                user_input = input("你: ")
                
                # 检查是否退出
                if user_input.lower() in ["退出", "exit", "quit"]:
                    print("\n生成writeup中...")
                    # 生成writeup
                    writeup_content = generate_writeup()
                    
                    # 创建wp文件夹（如果不存在）
                    os.makedirs('wp', exist_ok=True)
                    
                    # 生成时间戳文件名
                    timestamp = time.strftime('%Y%m%d_%H%M%S')
                    writeup_filename = f'wp/{timestamp}_writeup.md'
                    
                    # 保存writeup到文件
                    with open(writeup_filename, 'w', encoding='utf-8') as f:
                        f.write(writeup_content)
                    
                    print(f"\nwriteup已保存到: {writeup_filename}")
                    print("会话结束，再见！")
                    break
                
                # 发送用户输入给大模型并获取回复
                response = get_response(user_input)
                print("模型回复已写入communication.md")
                # 将模型回复写入communication.md
                write_to_communication(response)
                # 更新最后修改时间
                last_modified = os.path.getmtime('communication.md')
        
        # 短暂休眠，避免CPU占用过高
        time.sleep(0.5)

if __name__ == "__main__":
    main()
