import json
import os
from typing import Dict, List, Tuple
import openai

class StyleLearner:
    def __init__(self, api_key: str):
        """初始化风格学习器
        
        Args:
            api_key: OpenAI API 密钥
        """
        openai.api_key = api_key
        
    def load_training_data(self, source_dir: str, translated_dir: str) -> List[Tuple[str, str]]:
        """加载训练数据
        
        Args:
            source_dir: 原文目录
            translated_dir: 译文目录
            
        Returns:
            原文-译文对列表
        """
        pairs = []
        
        # 确保两个目录都存在
        if not os.path.exists(source_dir) or not os.path.exists(translated_dir):
            print("训练数据目录不存在")
            return pairs
            
        # 遍历文件
        for filename in os.listdir(source_dir):
            if not filename.endswith('.json'):
                continue
                
            source_path = os.path.join(source_dir, filename)
            translated_path = os.path.join(translated_dir, filename)
            
            if not os.path.exists(translated_path):
                continue
                
            try:
                # 读取原文
                with open(source_path, 'r', encoding='utf-8') as f:
                    source_data = json.load(f)
                    
                # 读取译文
                with open(translated_path, 'r', encoding='utf-8') as f:
                    translated_data = json.load(f)
                    
                # 提取需要翻译的字段
                for source_item, translated_item in zip(source_data, translated_data):
                    if 'content' in source_item and 'content' in translated_item:
                        pairs.append((source_item['content'], translated_item['content']))
                    if 'title' in source_item and 'title' in translated_item:
                        pairs.append((source_item['title'], translated_item['title']))
                    if 'teller' in source_item and 'teller' in translated_item:
                        pairs.append((source_item['teller'], translated_item['teller']))
                        
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {str(e)}")
                
        return pairs
    
    def generate_style_guide(self, pairs: List[Tuple[str, str]], output_path: str) -> None:
        """生成风格指南
        
        Args:
            pairs: 原文-译文对列表
            output_path: 输出文件路径
        """
        if not pairs:
            print("没有可用的训练数据")
            return
            
        try:
            # 构建提示词
            examples = "\n".join([f"原文：{source}\n译文：{translated}" for source, translated in pairs[:5]])
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的翻译风格分析专家。请根据提供的原文-译文对，总结出翻译风格指南。"},
                    {"role": "user", "content": f"请分析以下翻译对，总结出翻译风格指南：\n{examples}"}
                ]
            )
            
            style_guide = response.choices[0].message.content
            
            # 保存风格指南
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(style_guide)
                
        except Exception as e:
            print(f"生成风格指南时出错: {str(e)}") 