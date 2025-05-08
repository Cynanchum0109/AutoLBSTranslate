import json
import os
from typing import Dict, List, Set

class TermExtractor:
    def __init__(self):
        self.terms = {
            "characters": [],  # 存储角色名称的原文译文对
            "positions": [],   # 存储职位的原文译文对
            "locations": [],    # 存储地点的原文译文对
            "content": []  # 存储content的原文译文对
        }
        self.seen_texts = {
            "characters": {},  # 存储已见过的文本及其ID
            "positions": {},   # 存储已见过的文本及其ID
            "locations": {},    # 存储已见过的文本及其ID
            "content": {}  # 存储已见过的文本及其ID
        }

    def process_text(self, category: str, text: str, item_id: int, is_source: bool = True):
        """处理文本，跳过重复条目"""
        if text in self.seen_texts[category]:
            print(f"跳过重复的{category}: {text}")
            return  # 跳过重复文本
        
        if is_source:
            self.seen_texts[category][text] = item_id
            self.terms[category].append({
                "original": text,
                "translated": "",
                "id": item_id  # 临时存储ID用于匹配
            })
            print(f"添加新的{category}: {text}")
        else:
            # 查找对应的原文条目
            for item in self.terms[category]:
                if item["id"] == item_id and item["translated"] == "":
                    item["translated"] = text
                    print(f"更新{category}翻译: {item['original']} -> {text}")
                    break

    def process_file_pair(self, source_path: str, translated_path: str):
        """处理对应的文件对"""
        print(f"\n处理文件对: {os.path.basename(source_path)} -> {os.path.basename(translated_path)}")
        
        # 读取原文文件
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                source_data = json.load(f)
                if "dataList" in source_data:
                    for item in source_data["dataList"]:
                        if "id" not in item:
                            continue
                        # 处理角色名称
                        
                        if "teller" in item:
                            self.process_text("characters", item["teller"], item["id"], True)
                        # 处理职位
                        if "title" in item:
                            self.process_text("positions", item["title"], item["id"], True)
                        # 处理地点
                        if "place" in item:
                            self.process_text("locations", item["place"], item["id"], True)
                        
                        # 处理content内容
                        if "content" in item:
                            self.process_text("content", item["content"], item["id"], True)
        except Exception as e:
            print(f"处理原文文件时出错: {str(e)}")
            return

        # 读取译文文件
        try:
            with open(translated_path, 'r', encoding='utf-8') as f:
                translated_data = json.load(f)
                if "dataList" in translated_data:
                    for item in translated_data["dataList"]:
                        if "id" not in item:
                            continue
                        
                        # 处理角色名称
                        if "teller" in item:
                            self.process_text("characters", item["teller"], item["id"], False)
                        # 处理职位
                        if "title" in item:
                            self.process_text("positions", item["title"], item["id"], False)
                        # 处理地点
                        if "place" in item:
                            self.process_text("locations", item["place"], item["id"], False)
                        # 处理content内容
                        
                        if "content" in item:
                            self.process_text("content", item["content"], item["id"], False)
        except Exception as e:
            print(f"处理译文文件时出错: {str(e)}")
            return

    def save_terms(self, output_path: str):
        """保存提取的术语"""
        print("\n保存结果...")
        # 移除未翻译的条目和临时ID字段
        output_terms = {}
        for category in self.terms:
            output_terms[category] = []
            for item in self.terms[category]:
                if item["translated"]:
                    output_terms[category].append({
                        "original": item["original"],
                        "translated": item["translated"]
                    })
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_terms, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到: {output_path}")

def main():
    # 设置输入输出路径
    source_dir = "data/training/source/StoryData"
    translated_dir = "data/training/translated/StoryData"
    output_path = "config/translatePrompt/terms.json"
    
    # 创建提取器实例
    extractor = TermExtractor()
    
    # 处理所有文件
    processed_count = 0
    skipped_count = 0
    print(f"\n开始处理文件...")
    
    for filename in os.listdir(source_dir):
        if not filename.startswith('EN_') or not filename.endswith('.json'):
            continue
            
        source_path = os.path.join(source_dir, filename)
        translated_filename = filename[3:]  # 移除'EN_'前缀
        translated_path = os.path.join(translated_dir, translated_filename)
        
        if os.path.exists(translated_path):
            extractor.process_file_pair(source_path, translated_path)
            processed_count += 1
        else:
            print(f"跳过: 找不到对应的翻译文件 {translated_filename}")
            skipped_count += 1
    
    # 保存结果
    extractor.save_terms(output_path)
    print(f"\n处理完成:")
    print(f"- 成功处理: {processed_count} 个文件")
    print(f"- 跳过: {skipped_count} 个文件")

if __name__ == "__main__":
    main() 