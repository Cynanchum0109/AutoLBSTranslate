import json
import os
from typing import Dict, List, Optional
import openai

class Translator:
    def __init__(self, api_key: str):
        """初始化翻译器
        
        Args:
            api_key: OpenAI API 密钥
        """
        openai.api_key = api_key
        self.style_guide = ""
        
    def load_style_guide(self, style_guide_path: str) -> None:
        """加载翻译风格指南
        
        Args:
            style_guide_path: 风格指南文件路径
        """
        if os.path.exists(style_guide_path):
            with open(style_guide_path, 'r', encoding='utf-8') as f:
                self.style_guide = f.read()
    
    def translate_text(self, text: str) -> str:
        """翻译单条文本
        
        Args:
            text: 待翻译文本
            
        Returns:
            翻译后的文本
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"你是一个专业的翻译助手。请遵循以下翻译风格指南：\n{self.style_guide}"},
                    {"role": "user", "content": f"请翻译以下文本：\n{text}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"翻译出错: {str(e)}")
            return text
    
    def process_json_file(self, file_path: str, output_path: str) -> None:
        """处理单个 JSON 文件
        
        Args:
            file_path: 输入文件路径
            output_path: 输出文件路径
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 处理需要翻译的字段
            for item in data:
                if 'content' in item:
                    item['content'] = self.translate_text(item['content'])
                if 'title' in item:
                    item['title'] = self.translate_text(item['title'])
                if 'teller' in item:
                    item['teller'] = self.translate_text(item['teller'])
            
            # 保存结果
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {str(e)}")
    
    def process_directory(self, input_dir: str, output_dir: str) -> None:
        """处理整个目录
        
        Args:
            input_dir: 输入目录
            output_dir: 输出目录
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        for filename in os.listdir(input_dir):
            if filename.endswith('.json'):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                print(f"处理文件: {filename}")
                self.process_json_file(input_path, output_path) 