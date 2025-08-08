"""
应用工厂函数
"""
import os
from flask import Flask
from .config import config
from .models import DatabaseManager
from .services import ExternalAPIService, DataService
from .utils import TagSearchUtil
from .controllers import (
    init_database_routes,
    init_hcfx_routes,
    init_loss_routes,
    init_xnjs_routes,
    init_common_routes,
    init_document_routes
)


def create_app(config_name=None):
    """创建Flask应用实例"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 初始化数据库管理器
    db_manager = DatabaseManager(app.config['DATABASE_URI'])
    if not db_manager.initialize():
        app.logger.error("Failed to initialize database connection")
    
    # 初始化外部API服务
    external_api = ExternalAPIService(
        base_url=app.config['EXTERNAL_API_BASE_URL'],
        db_name=app.config['EXTERNAL_DB_NAME'],
        username=app.config['EXTERNAL_USERNAME'],
        password=app.config['EXTERNAL_PASSWORD']
    )
    
    # 初始化数据服务
    data_service = DataService(db_manager, external_api)
    
    # 初始化标签搜索工具
    tag_search_util = TagSearchUtil(app.config['TAG_NAMES_FILE'])
    
    # 注册蓝图
    app.register_blueprint(init_database_routes(data_service))
    app.register_blueprint(init_hcfx_routes(data_service))
    app.register_blueprint(init_loss_routes(data_service))
    app.register_blueprint(init_xnjs_routes(data_service))
    app.register_blueprint(init_common_routes(data_service, tag_search_util))
    app.register_blueprint(init_document_routes())
    
    # 添加健康检查路由
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    return app
