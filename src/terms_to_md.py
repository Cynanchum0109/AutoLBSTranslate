import json
import os

def convert_terms_to_md():
    # 读取terms.json文件
    terms_path = "config/translatePrompt/terms.json"
    output_path = "config/translatePrompt/terms.md"
    
    try:
        with open(terms_path, 'r', encoding='utf-8') as f:
            terms = json.load(f)
    except Exception as e:
        print(f"读取terms.json失败: {str(e)}")
        return
    
    md_content = ""
    item_count = 0
    
    # 处理所有类别
    categories = ["characters", "positions", "locations", "content"]
    for category in categories:
        for item in terms[category]:
            original = str(item["original"])
            translated = str(item["translated"])
            
            if "？？？" in translated:
                continue
                
            item_count += 1
            original = original.replace("|", "\\|").replace("\n", " ")
            translated = translated.replace("|", "\\|").replace("\n", " ")
            md_content += f"| {item_count} | {original} | {translated} |\n"
    
    # 保存markdown文件
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"已生成markdown文件: {output_path}")
    except Exception as e:
        print(f"保存markdown文件失败: {str(e)}")

if __name__ == "__main__":
    convert_terms_to_md() 