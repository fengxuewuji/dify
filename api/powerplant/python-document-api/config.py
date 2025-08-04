import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
    WORD_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'word_files')
    PDF_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'pdf_files')
    
    @staticmethod
    def init_app(app):
        pass  # 可以在这里添加其他初始化代码，例如加载环境变量等