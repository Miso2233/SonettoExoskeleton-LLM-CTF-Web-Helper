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
    while True:
        print("\n请输入你的响应（输入'go'发送communication.md内容）：")
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
        
        # 检查是否输入'go'
        if user_input.lower() == "go":
            print("\n读取communication.md文件内容...")
            communication_content = read_communication_content()
            if communication_content:
                print("发送communication.md内容给模型...")
                response = get_response(communication_content)
                print("模型回复已写入communication.md")
                # 将模型回复写入communication.md
                write_to_communication(response)
            else:
                print("communication.md文件中没有足够的内容")
        else:
            # 发送用户输入给大模型并获取回复
            response = get_response(user_input)
            print("模型回复已写入communication.md")
            # 将模型回复写入communication.md
            write_to_communication(response)

if __name__ == "__main__":
    main()
