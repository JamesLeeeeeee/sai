from flask import Blueprint, request, jsonify
from app.services.mbti_service import analyze_mbti_personality, analyze_mbti_from_file

mbti_bp = Blueprint('mbti', __name__)

@mbti_bp.route('/analyze-mbti', methods=['POST'])
def analyze_mbti():
    data = request.json
    profile = data.get("profile")
    content = data.get("content")
    
    result = analyze_mbti_personality(profile, content)
    return jsonify({"result": result})

@mbti_bp.route('/analyze-mbti-file', methods=['POST'])
def analyze_mbti_file():
    if 'profile' not in request.files or 'content' not in request.files:
        return jsonify({"error": "프로필 또는 대화 내용 파일이 없습니다"}), 400
        
    profile_file = request.files['profile']
    content_file = request.files['content']
    
    if profile_file.filename == '' or content_file.filename == '':
        return jsonify({"error": "파일이 선택되지 않았습니다"}), 400
    
    profile = profile_file.read().decode('utf-8')
    content = content_file.read().decode('utf-8')
    
    result = analyze_mbti_personality(profile, content)
    return jsonify({"result": result})