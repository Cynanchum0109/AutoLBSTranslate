import os
from config.config import *
from src.translator import Translator
from src.style_learner import StyleLearner

def main():
    # 初始化风格学习器
    style_learner = StyleLearner(OPENAI_API_KEY)
    
    # 加载训练数据并生成风格指南
    training_pairs = style_learner.load_training_data(
        TRAINING_SOURCE_DIR,
        TRAINING_TRANSLATED_DIR
    )
    style_learner.generate_style_guide(training_pairs, STYLE_GUIDE_PATH)
    
    # 初始化翻译器
    translator = Translator(OPENAI_API_KEY)
    translator.load_style_guide(STYLE_GUIDE_PATH)
    
    # 处理源文件
    translator.process_directory(SOURCE_DIR, TRANSLATED_DIR)

if __name__ == "__main__":
    main() 