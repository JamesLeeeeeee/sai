from flask import Blueprint, request, jsonify
from app.services.mbti_service import analyze_mbti_personality

mbti_bp = Blueprint('mbti', __name__)

@mbti_bp.route('/analyze-mbti', methods=['POST'])
def analyze_mbti():
    data = request.json
    target_name = data.get("target_name")
    content = data.get("content")
    
    result = analyze_mbti_personality(target_name, content)
    return jsonify({"result": result})