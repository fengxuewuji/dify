"""
通用数据控制器
"""
from flask import Blueprint, request, jsonify
from ..services import DataService
from ..utils import TagSearchUtil

# 创建蓝图
common_bp = Blueprint('common', __name__, url_prefix='/api/common')


def init_common_routes(data_service: DataService, tag_search_util: TagSearchUtil):
    """初始化通用数据路由"""
    
    @common_bp.route('/real', methods=['POST'])
    def get_history_value():
        """获取历史数据"""
        try:
            tag_name = request.json.get('tagName')
            end_time_str = request.json.get('endTimeStr')
            time_span = int(request.json.get('timeSpan'))
            data_num = int(request.json.get('dataNum', 12))
            
            if not tag_name or not end_time_str:
                return jsonify({"error": "tagName and endTimeStr are required"}), 400
            
            if data_num < 1 or data_num > 100:
                return jsonify({"error": "dataNum must be between 1 and 100"}), 400
            
            result = data_service.get_common_history_data(
                tag_name, end_time_str, time_span, data_num
            )
            
            if not result:
                return jsonify({"error": "No data found for the given tag name"}), 404
            
            return jsonify(result)
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @common_bp.route('/getReason', methods=['GET'])
    def get_reason():
        """获取耗差计算公式，及各参数数据"""
        try:
            hc = request.args.get('hc')
            time_param = request.args.get('time')
            
            # TODO: 实现获取耗差计算公式的逻辑
            return jsonify({"message": "This endpoint is not implemented yet"}), 501
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @common_bp.route('/getTagNames', methods=['POST'])
    def get_tag_names():
        """根据关键词搜索标签名称"""
        try:
            keywords = request.json.get('keywords')
            if not keywords:
                return jsonify({"error": "keywords is required"}), 400
            
            result = tag_search_util.search_tag_names(keywords)
            return jsonify(result)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return common_bp
