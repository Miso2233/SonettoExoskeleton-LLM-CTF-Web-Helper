"""
大模型API客户端模块

该模块包含与LLM通信相关的类和方法，负责发送请求和处理响应。
"""

import json
from openai import OpenAI
from src.Module_02_Files import generate_soul

class MODES:
    COACH = "coach"
    COPILOT = "copilot"
    BOOST = "boost"
    FULL_POWER = "full_power"

DEFAULT_MODE = json.load(open('config.json', 'r', encoding='utf-8'))['mode']

MAX_OUTPUT_TOKENS = 4096
MAX_INPUT_TOKENS = 64000

TEMPERATURE_OF_MODE = {
    MODES.COACH : 0.2,
    MODES.COPILOT : 0.15,
    MODES.BOOST : 0.1,
    MODES.FULL_POWER : 0.05
}

class Sonetto:
    """
    Sonetto类
    
    封装了与大模型通信的所有功能，包括：
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
        
        # 模型选择相关 - 使用可用模型列表的第一项作为默认值
        available_models = self.get_available_models()
        self.current_model = available_models[0] if available_models else 'deepseek-chat'
    
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
            model=self.current_model,
            messages=self.conversation_history,
            temperature=TEMPERATURE_OF_MODE[self.mode],
            max_tokens=MAX_OUTPUT_TOKENS
        )
        
        # 提取回复内容
        assistant_response = response.choices[0].message.content
        
        # 将Sonetto回复添加到上下文
        self.conversation_history.append({"role": "assistant", "content": assistant_response})

        # 增加备注输入框
        assistant_response += "\n\n---\n### 备注"
        
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
    
    def get_available_models(self) -> list:
        """
        获取所有可用模型的名称列表（筛选后的）
        
        Returns:
            可用模型名称的列表
        """
        try:
            models = self.client.models.list()
            print(f"API返回的模型列表: {models}")
            
            if hasattr(models, 'data'):
                model_names = [model.id for model in models.data]
                # print(f"解析后的模型名称: {model_names}")
                if model_names:
                    filtered_models = self._filter_models(model_names)
                    # print(f"筛选后的模型名称: {filtered_models}")
                    if filtered_models:
                        return filtered_models
        except Exception as e:
            print(f"获取模型列表时出错: {type(e).__name__}: {e}")
            raise e
    
    @staticmethod
    def _filter_models(model_names: list) -> list:
        """
        筛选模型名称，只保留符合条件的模型，并进行排序
        
        Args:
            model_names: 原始模型名称列表
            
        Returns:
            筛选后的模型名称列表
        """
        allowed_keywords = ['MiMo', 'MiniMax', 'DeepSeek', 'Qwen', 'GLM']
        
        filtered = []
        for model in model_names:
            model_lower: str = model.lower()
            for keyword in allowed_keywords:
                if model_lower.startswith(keyword.lower()):
                    filtered.append(model)
                    break
        
        # 如果筛选后没有结果，返回备选列表
        if not filtered:
            print("筛选后无模型，使用备选列表")
            raise Exception("筛选后无模型")
        
        return sorted(filtered)
    
    def switch_model(self, model_name: str) -> bool:
        """
        切换到指定的模型
        
        Args:
            model_name: 要切换到的模型名称
            
        Returns:
            是否切换成功
        """
        try:
            if not model_name:
                print("模型名称不能为空")
                return False
            
            # 更新当前模型
            self.current_model = model_name
            
            print(f"模型已切换为: {model_name}")
            return True
        except Exception as e:
            print(f"切换模型时出错: {e}")
            return False
