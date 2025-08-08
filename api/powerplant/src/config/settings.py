"""
应用配置文件
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """基础配置类"""
    # 数据库配置
    DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://root:MS_zyp1121@localhost:3306/dify_db')
    
    # 外部API配置
    EXTERNAL_API_BASE_URL = os.getenv('EXTERNAL_API_BASE_URL', 'http://168.168.10.82:20001')
    EXTERNAL_DB_NAME = os.getenv('EXTERNAL_DB_NAME', 'db102')
    EXTERNAL_USERNAME = os.getenv('EXTERNAL_USERNAME', 'user1')
    EXTERNAL_PASSWORD = os.getenv('EXTERNAL_PASSWORD', 'luculent1!')
    
    # Flask配置
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 6002))
    
    # 文件路径配置
    TAG_NAMES_FILE = os.getenv('TAG_NAMES_FILE', '/home/zyp/codes/dify/api/powerplant/tag_names.yaml')
    
    # 文档生成配置
    DEFAULT_FONT_PATHS = [
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/System/Library/Fonts/PingFang.ttc',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
    ]

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False

class TestingConfig(Config):
    """测试环境配置"""
    DEBUG = True
    TESTING = True

# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
