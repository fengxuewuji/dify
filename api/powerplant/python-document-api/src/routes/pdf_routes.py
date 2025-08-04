from flask import Blueprint, request, jsonify
from services.pdf_service import generate_pdf

pdf_routes = Blueprint('pdf_routes', __name__)

@pdf_routes.route('/generate-pdf', methods=['POST'])
def create_pdf():
    data = request.json
    if not data or 'content' not in data:
        return jsonify({"error": "Content is required"}), 400
    
    pdf_file_path = generate_pdf(data['content'])
    return jsonify({"message": "PDF generated successfully", "file_path": pdf_file_path}), 201