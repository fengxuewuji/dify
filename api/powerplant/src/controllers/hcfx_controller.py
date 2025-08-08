"""
耗差分析控制器
"""
from flask import Blueprint, request, jsonify
from ..services import DataService
from ..config import HCFX_TAG_NAMES, LOSS_TAG_NAMES, XNJS_TAG_NAMES

# 创建蓝图
hcfx_bp = Blueprint('hcfx', __name__, url_prefix='/api/hcfx')


def init_hcfx_routes(data_service: DataService):
    """初始化耗差分析路由"""
    
    @hcfx_bp.route('/mock', methods=['GET'])
    def get_latest_hcfx():
        """获取最新的耗差分析数据（模拟数据）"""
        try:
            result = data_service.get_latest_hcfx_mock()
            if result:
                return jsonify(result)
            else:
                return jsonify({'error': 'No record found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @hcfx_bp.route('/real', methods=['GET'])
    def get_real_hcfx_data():
        """获取实时耗差分析数据"""
        try:
            real_data = data_service.get_real_hcfx_data(HCFX_TAG_NAMES)
            return jsonify(real_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @hcfx_bp.route('/top1', methods=['GET'])
    def get_top_hcfx():
        """获取实时耗差分析中数据的最大值"""
        try:
            max_values = data_service.get_top_hcfx_value(HCFX_TAG_NAMES)
            if not max_values:
                return jsonify({"error": "No data found"}), 404
            return jsonify(max_values)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @hcfx_bp.route('/history', methods=['POST'])
    def get_his_hcfx():
        """获取历史耗差分析数据"""
        try:
            tag_name = request.json.get('tagName')
            days = int(request.json.get('days', 3))
            
            if not tag_name:
                return jsonify({"error": "tagName is required"}), 400
            
            result = data_service.get_history_hcfx_data(tag_name, days)
            if not result:
                return jsonify({"error": "No data found for the given tag name"}), 404
            
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return hcfx_bp


# 创建其他数据类型的蓝图
loss_bp = Blueprint('loss', __name__, url_prefix='/api/loss')
xnjs_bp = Blueprint('xnjs', __name__, url_prefix='/api/xnjs')


def init_loss_routes(data_service: DataService):
    """初始化损失数据路由"""
    
    @loss_bp.route('/real', methods=['GET'])
    def get_real_loss_data():
        """获取实时损失数据"""
        try:
            real_data = data_service.get_real_hcfx_data(LOSS_TAG_NAMES)
            return jsonify(real_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return loss_bp


def init_xnjs_routes(data_service: DataService):
    """初始化性能指数路由"""
    
    @xnjs_bp.route('/real', methods=['GET'])
    def get_real_xnjs_data():
        """获取实时性能指数数据"""
        try:
            real_data = data_service.get_real_hcfx_data(XNJS_TAG_NAMES)
            return jsonify(real_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return xnjs_bp
