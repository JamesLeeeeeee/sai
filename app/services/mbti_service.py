# app/services/mbti_service.py
import json
from app.utils.openai_utils import get_openai_client
from app.templates.prompts import PROMPT, SYSTEM_MESSAGE
from app.utils.json_utils import result2json
from app.agents.mbti_analyzer_agent import analyze_mbti_personality_with_agent

def analyze_mbti_personality_with_agents(profile, content):
    """Agent 구조를 사용한 새로운 분석 함수 (메인)"""
    return analyze_mbti_personality_with_agent(profile, content)

def analyze_mbti_personality(profile, content):
    """기존 방식 - 호환성을 위해 유지 (케미 분석 없음)"""
    client = get_openai_client()
    
    prompt = PROMPT.format(profile=profile, content=content)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
    )

    gpt_result = response.choices[0].message.content
    
    try:
        result = result2json(gpt_result)
        
        if isinstance(result, dict):
            # Original 섹션 제거 로직
            profile_data = result.get('profile', {})
            partner_mbti_from_profile = profile_data.get('partner_mbti', '').strip()
            
            if not partner_mbti_from_profile:
                mbti_prediction = result.get('mbti_prediction', {})
                if 'original' in mbti_prediction:
                    print("⚠️ 상대방 MBTI가 프로필에 없으므로 original 섹션을 제거합니다.")
                    del mbti_prediction['original']
            
            # ⚠️ 기존 방식에서는 케미 분석 없음 (Agent 방식만 케미 분석 포함)
            return json.dumps(result, ensure_ascii=False, indent=2)
        
        return gpt_result
    except Exception as e:
        print(f"Error processing result: {e}")
        return gpt_result

def analyze_mbti_from_file(profile_path, content_path):
    """파일에서 MBTI 분석 - Agent 방식 사용"""
    try:
        with open(profile_path, 'r', encoding='utf-8') as profile_file:
            profile = profile_file.read()
            
        with open(content_path, 'r', encoding='utf-8') as content_file:
            content = content_file.read()
            
        # ✅ Agent 방식으로 변경 (케미 분석 포함)
        return analyze_mbti_personality_with_agents(profile, content)
        
    except Exception as e:
        print(f"파일 처리 중 오류 발생: {e}")
        return {"error": str(e)}