"""
Sonetto CTF Web 解题助手

程序入口文件，负责初始化会话和处理前端交互。
"""

import os
import time
from src.deepseek_client import Sonetto
from src.file_utils import communication_manager
from src.websocket_server import WebSocketServer

def main():
    print("=== Sonetto CTF Web 解题助手 ===")
    print("我是 Sonetto，一名网安专家，主攻 CTF Web 方向。")
    print("让我帮助你解决 CTF Web 题目。")
    print("\n初始化会话中...")
    
    # 清空communication.md文件
    communication_manager.clear()
    
    # 实例化Sonetto类
    sonetto = Sonetto()
    
    # 初始化WebSocket服务器
    websocket_server = WebSocketServer(sonetto)
    # 在单独的线程中启动WebSocket服务器
    websocket_thread = websocket_server.run_in_thread()
    
    # 初始化会话
    session_response = sonetto.begin_session()
    print("\n会话初始化完成")
    
    # 将模型回复写入communication.md
    communication_manager.write(session_response)
    
    # 开始交互循环
    # 记录communication.md的初始修改时间
    last_modified = 0
    try:
        last_modified = os.path.getmtime('communication.md')
    except FileNotFoundError:
        pass
    
    while True:
        
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
                    writeup_content = sonetto.generate_writeup()
                    
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
                
                # 检查是否包含重新开始标记
                elif 'RESTART_SESSION' in full_content:
                    print("\n检测到重新开始指令...")
                    print("重新初始化会话中...")
                    # 清空communication.md文件
                    communication_manager.clear()
                    # 重新初始化会话
                    session_response = sonetto.begin_session()
                    print("\n会话重新初始化完成")
                    # 将模型回复写入communication.md
                    communication_manager.write(session_response)
                    # 更新最后修改时间
                    last_modified = os.path.getmtime('communication.md')
                    continue
                
                # 检查是否是WebSocket处理的内容（包含模型回复标记）
                elif '### 模型回复' in full_content:
                    print("检测到WebSocket处理的内容，跳过文件轮询处理")
                    # 更新最后修改时间，避免重复处理
                    last_modified = current_modified
                    continue
                
                # 正常处理通信内容
                communication_content = communication_manager.read()
                if communication_content:
                    print("发送communication.md内容给模型...")
                    response = sonetto.get_response(communication_content)
                    print("模型回复已写入communication.md")
                    # 将模型回复写入communication.md
                    communication_manager.write(response)
                    # 更新最后修改时间
                    last_modified = os.path.getmtime('communication.md')
                else:
                    print("communication.md文件中没有足够的内容")
        except FileNotFoundError:
            pass
        
        # 短暂休眠，避免CPU占用过高
        time.sleep(0.5)

if __name__ == "__main__":
    main()
