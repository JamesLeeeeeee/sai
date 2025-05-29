# app/routes/mbti_routes.py
from flask import Blueprint, request, jsonify
import json
from app.services.mbti_service import analyze_mbti_personality_with_agents  # Agent 방식만 import

mbti_bp = Blueprint('mbti', __name__)

@mbti_bp.route('/analyze-mbti', methods=['POST'])
def analyze_mbti():
    """텍스트 기반 MBTI 분석"""
    try:
        data = request.get_json()
        profile = data.get('profile', '')
        content = data.get('content', '')
        
        if not profile or not content:
            return jsonify({"error": "프로필과 대화 내용이 모두 필요합니다."}), 400
        
        # Agent 방식 사용
        result = analyze_mbti_personality_with_agents(profile, content)
        
        if isinstance(result, str):
            try:
                result_dict = json.loads(result)
                return jsonify(result_dict)
            except json.JSONDecodeError:
                return jsonify({"raw_response": result})
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@mbti_bp.route('/analyze-mbti-file', methods=['POST'])
def analyze_mbti_file():
    """파일 업로드 MBTI 분석 - Agent 방식으로 통일"""
    try:
        if 'profile' not in request.files or 'content' not in request.files:
            return jsonify({"error": "프로필 또는 대화 내용 파일이 없습니다"}), 400
            
        profile_file = request.files['profile']
        content_file = request.files['content']
        
        if profile_file.filename == '' or content_file.filename == '':
            return jsonify({"error": "파일이 선택되지 않았습니다"}), 400
        
        profile = profile_file.read().decode('utf-8')
        content = content_file.read().decode('utf-8')
        
        # ✅ Agent 방식으로 변경
        result = analyze_mbti_personality_with_agents(profile, content)
        
        if isinstance(result, str):
            try:
                result_dict = json.loads(result)
                return jsonify(result_dict)
            except json.JSONDecodeError:
                return jsonify({"raw_response": result})
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500