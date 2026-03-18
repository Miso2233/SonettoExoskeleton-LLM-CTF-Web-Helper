"""
WebSocket服务器模块

该模块实现了WebSocket服务器功能，用于处理前端的实时通信请求，包括：
- 按钮点击事件处理
- 自定义函数调用
- 客户端连接管理
"""
import asyncio
import websockets
import json
import threading
import time
from src.file_utils import communication_manager, save_writeup
from src.deepseek_client import Sonetto

class WebSocketServer:
    """
    WebSocket服务器类
    
    负责处理前端的实时通信请求
    """
    
    def __init__(self, sonetto_instance):
        """
        初始化WebSocket服务器
        
        Args:
            sonetto_instance: Sonetto类的实例
        """
        self.sonetto = sonetto_instance
        self.clients = set()
        self.server = None
        self.loop = None
    
    async def handle_connection(self, websocket):
        """
        处理新的WebSocket连接
        
        Args:
            websocket: WebSocket连接对象
        """
        # 添加客户端到集合
        self.clients.add(websocket)
        print(f"新的客户端连接: {websocket.remote_address}")
        
        try:
            # 处理消息循环
            async for message in websocket:
                await self.process_message(websocket, message)
        except websockets.exceptions.ConnectionClosedError:
            print(f"客户端连接关闭: {websocket.remote_address}")
        finally:
            # 从集合中移除客户端
            self.clients.remove(websocket)
    
    async def process_message(self, websocket, message):
        """
        处理收到的消息
        
        Args:
            websocket: WebSocket连接对象
            message: 收到的消息
        """
        try:
            # 解析JSON消息
            data = json.loads(message)
            message_type = data.get('type')
            
            print(f"收到消息类型: {message_type}")
            
            # 根据消息类型处理
            if message_type == 'next_step':
                await self.handle_next_step(websocket, data)
            elif message_type == 'restart':
                await self.handle_restart(websocket)
            elif message_type == 'exit':
                await self.handle_exit(websocket)
            elif message_type == 'custom_function':
                await self.handle_custom_function(websocket, data)
            elif message_type == 'switch_mode':
                await self.handle_switch_mode(websocket, data)
            else:
                await self.send_response(websocket, 'error', {'message': '未知的消息类型'})
        except json.JSONDecodeError:
            await self.send_response(websocket, 'error', {'message': '无效的JSON格式'})
        except Exception as e:
            print(f"处理消息时出错: {e}")
            await self.send_response(websocket, 'error', {'message': str(e)})
    
    async def handle_next_step(self, websocket, data):
        """
        处理下一步按钮点击
        
        Args:
            websocket: WebSocket连接对象
            data: 消息数据
        """
        try:
            # 获取输入内容
            inputs = data.get('inputs', {})
            
            # 构建输入内容
            input_content = ''
            for label, value in inputs.items():
                input_content += f"### {label}\n{value}\n\n"
            
            # 发送到模型处理
            response = self.sonetto.get_response(input_content)
            
            # 写入communication.md文件
            communication_manager.write(response)
            
            # 发送响应给客户端
            await self.send_response(websocket, 'next_step', {'response': response})
            print("下一步处理完成")
        except Exception as e:
            print(f"处理下一步时出错: {e}")
            await self.send_response(websocket, 'error', {'message': str(e)})
    
    async def handle_restart(self, websocket):
        """
        处理重新开始按钮点击
        
        Args:
            websocket: WebSocket连接对象
        """
        try:
            # 清空communication.md文件
            communication_manager.clear()
            
            # 重新初始化会话
            session_response = self.sonetto.begin_session()
            
            # 将模型回复写入communication.md
            communication_manager.write(session_response)
            
            # 发送响应给客户端
            await self.send_response(websocket, 'restart', {'response': session_response})
            print("会话重新初始化完成")
        except Exception as e:
            print(f"处理重新开始时出错: {e}")
            await self.send_response(websocket, 'error', {'message': str(e)})
    
    async def handle_exit(self, websocket):
        """
        处理结束按钮点击
        
        Args:
            websocket: WebSocket连接对象
        """
        try:
            # 生成writeup
            writeup_content = self.sonetto.generate_writeup()
            
            # 保存writeup到文件
            save_writeup(writeup_content)
            
            # 生成时间戳文件名（用于返回给客户端）
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            writeup_filename = f'wp/{timestamp}_writeup.md'
            
            # 发送响应给客户端
            await self.send_response(websocket, 'exit', {'writeup': writeup_content, 'filename': writeup_filename})
            print("会话结束，writeup生成完成")
        except Exception as e:
            print(f"处理结束时出错: {e}")
            await self.send_response(websocket, 'error', {'message': str(e)})
    
    async def handle_custom_function(self, websocket, data):
        """
        处理自定义函数调用
        
        Args:
            websocket: WebSocket连接对象
            data: 消息数据
        """
        try:
            function_name = data.get('function_name')
            params = data.get('params', {})
            
            print(f"调用自定义函数: {function_name}")
            
            # 直接处理自定义函数逻辑
            if function_name == 'analyze_target':
                target = params.get('target', '')
                result = {
                    'target': target,
                    'analysis': f"分析目标: {target}\n这是一个示例分析结果。"
                }
            elif function_name == 'scan_vulnerabilities':
                target = params.get('target', '')
                result = {
                    'target': target,
                    'vulnerabilities': [
                        {'type': 'XSS', 'severity': 'high', 'description': '可能存在跨站脚本漏洞'},
                        {'type': 'SQL注入', 'severity': 'critical', 'description': '可能存在SQL注入漏洞'}
                    ]
                }
            elif function_name == 'generate_payload':
                vulnerability_type = params.get('vulnerability_type', 'XSS')
                result = {
                    'vulnerability_type': vulnerability_type,
                    'payload': f"示例{ vulnerability_type } payload: <script>alert('XSS')</script>"
                }
            else:
                result = {'error': '未知的函数名称'}
            
            # 发送响应给客户端
            await self.send_response(websocket, 'custom_function', {'result': result})
        except Exception as e:
            print(f"处理自定义函数时出错: {e}")
            await self.send_response(websocket, 'error', {'message': str(e)})
    
    async def handle_switch_mode(self, websocket, data):
        """
        处理模型模式切换

        Args:
            websocket: WebSocket连接对象
            data: 消息数据
        """
        try:
            # 获取新的模式
            mode = data.get('mode')
            
            if not mode:
                await self.send_response(websocket, 'error', {'message': '缺少模式参数'})
                return
            
            # 调用Sonetto的switch_mode方法
            self.sonetto.switch_mode(mode)
            
            # 更新config.json文件
            import json
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            config['mode'] = mode
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            # 发送响应给客户端
            await self.send_response(websocket, 'switch_mode', {'mode': mode, 'message': '模型模式切换成功'})
            print(f"模型模式切换为: {mode}")
        except Exception as e:
            print(f"处理模式切换时出错: {e}")
            await self.send_response(websocket, 'error', {'message': str(e)})
    
    async def send_response(self, websocket, message_type, data):
        """
        发送响应给客户端
        
        Args:
            websocket: WebSocket连接对象
            message_type: 消息类型
            data: 响应数据
        """
        # 添加token占用比例
        try:
            token_ratio = self.sonetto.estimate_context_tokens()
            data['token_ratio'] = token_ratio
        except Exception as e:
            print(f"获取token比例时出错: {e}")
        
        response = {
            'type': message_type,
            'data': data
        }
        await websocket.send(json.dumps(response))
    
    async def start_server(self):
        """
        启动WebSocket服务器
        """
        print("启动WebSocket服务器...")
        self.server = await websockets.serve(
            self.handle_connection, 
            "localhost", 
            8766
        )
        print("WebSocket服务器已启动，监听地址: ws://localhost:8766")
        await self.server.serve_forever()
    
    def run_in_thread(self):
        """
        在单独的线程中运行WebSocket服务器
        """
        def run_server():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            try:
                self.loop.run_until_complete(self.start_server())
            except KeyboardInterrupt:
                pass
            finally:
                self.loop.close()
        
        # 创建并启动线程
        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
        return thread