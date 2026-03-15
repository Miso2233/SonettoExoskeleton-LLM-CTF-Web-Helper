#!/usr/bin/env python3
"""
启动本地HTTP服务器，用于运行Sonetto CTF Web解题助手前端页面
"""

import http.server
import socketserver
import os

PORT = 8001

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def do_PUT(self):
        """处理PUT请求，用于写入文件"""
        # 获取文件路径
        file_path = self.path.lstrip('/')
        
        # 读取请求体
        content_length = int(self.headers['Content-Length'])
        content = self.rfile.read(content_length)
        
        try:
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content.decode('utf-8'))
            
            # 发送成功响应
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'File written successfully')
        except Exception as e:
            # 发送错误响应
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode('utf-8'))

if __name__ == "__main__":
    print(f"启动本地服务器，端口: {PORT}")
    print(f"请在浏览器中访问: http://localhost:{PORT}/app.html")
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")
