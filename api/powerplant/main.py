"""
主应用文件
"""
from src.app_factory import create_app
from src.config import config
import os

# 创建应用实例
app = create_app()

if __name__ == '__main__':
    # 从配置中获取运行参数
    config_name = os.getenv('FLASK_ENV', 'default')
    config_obj = config[config_name]
    
    app.run(
        debug=config_obj.DEBUG,
        host=config_obj.HOST,
        port=config_obj.PORT
    )
