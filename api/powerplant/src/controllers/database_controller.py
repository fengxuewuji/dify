"""
数据库查询控制器
"""
from flask import Blueprint, request, jsonify
from ..services import DataService

# 创建蓝图
database_bp = Blueprint('database', __name__, url_prefix='/api/database')


def init_database_routes(data_service: DataService):
    """初始化数据库路由"""
    
    @database_bp.route('/query', methods=['POST'])
    def query_database():
        """执行SQL查询"""
        try:
            sql_query = request.json.get('sql')
            if not sql_query:
                return jsonify({"error": "SQL query is required"}), 400
            
            result = data_service.execute_sql_query(sql_query)
            return jsonify(result)
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return database_bp
