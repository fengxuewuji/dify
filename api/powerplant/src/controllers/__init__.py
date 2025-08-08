"""
控制器模块初始化文件
"""
from .database_controller import init_database_routes
from .hcfx_controller import init_hcfx_routes, init_loss_routes, init_xnjs_routes
from .common_controller import init_common_routes
from .document_controller import init_document_routes

__all__ = [
    'init_database_routes',
    'init_hcfx_routes',
    'init_loss_routes', 
    'init_xnjs_routes',
    'init_common_routes',
    'init_document_routes'
]
