"""
文档生成控制器
"""
from flask import Blueprint, request, jsonify, send_file
from ..services import WordGenerator, PDFGenerator
from ..config import config

# 创建蓝图
document_bp = Blueprint('document', __name__, url_prefix='/api/generate')


def init_document_routes():
    """初始化文档生成路由"""
    
    @document_bp.route('/word', methods=['POST'])
    def generate_word_document():
        """生成Word文档"""
        try:
            data = request.json or {}
            content = data.get('content', '')
            filename = data.get('filename', 'document.docx')
            options = data.get('options', {})
            
            # 创建Word生成器
            word_generator = WordGenerator()
            
            # 生成文档
            file_stream = word_generator.generate_document(content, filename, options)
            
            return send_file(
                file_stream,
                as_attachment=True,
                download_name=filename,
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @document_bp.route('/pdf', methods=['POST'])
    def generate_pdf_document():
        """生成PDF文档"""
        try:
            data = request.json or {}
            content = data.get('content', '')
            filename = data.get('filename', 'document.pdf')
            options = data.get('options', {})
            
            # 获取字体路径配置
            font_paths = config['default'].DEFAULT_FONT_PATHS
            
            # 创建PDF生成器
            pdf_generator = PDFGenerator(font_paths)
            
            # 生成文档
            file_stream = pdf_generator.generate_document(content, filename, options)
            
            return send_file(
                file_stream,
                as_attachment=True,
                download_name=filename,
                mimetype='application/pdf'
            )
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return document_bp
