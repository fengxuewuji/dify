from flask import Blueprint, request, jsonify
from services.word_service import generate_word_file

word_routes = Blueprint('word_routes', __name__)

@word_routes.route('/generate-word', methods=['POST'])
def create_word():
    data = request.json
    if not data or 'content' not in data:
        return jsonify({"error": "Content is required"}), 400
    
    try:
        file_path = generate_word_file(data['content'])
        return jsonify({"message": "Word file created successfully", "file_path": file_path}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500