from app.utils.openai_utils import get_openai_client
import re
import json
import random

# 분할된 데이터 파일들에서 import
from app.data.mbti_characters import MBTI_CHARACTERS
from app.data.compatibility_matrix import COMPATIBILITY_MATRIX
from app.data.warning_patterns import WARNING_PATTERNS, SPECIAL_WARNINGS
from app.templates.prompts import PROMPT, SYSTEM_MESSAGE
from app.utils.json_utils import result2json

def get_chemistry_score(mbti1, mbti2):
    """초안 기반 케미 점수 계산"""
    key1 = f"{mbti1}-{mbti2}"
    key2 = f"{mbti2}-{mbti1}"
    
    compatibility_info = COMPATIBILITY_MATRIX.get(key1) or COMPATIBILITY_MATRIX.get(key2)
    
    if compatibility_info:
        return compatibility_info['base'], compatibility_info['description']
    else:
        return 75, f"{MBTI_CHARACTERS[mbti1]['animal']}과 {MBTI_CHARACTERS[mbti2]['animal']}의 독특한 케미"

def get_score_description(score):
    """점수 기반 설명 생성"""
    descriptions = {
        90: ['완벽한 밸런스 조합! ✨', '환상의 케미! 🔥', '운명적 만남! 💫'],
        80: ['훌륭한 파트너십! 🤝', '서로를 완성하는 케미! 🌟', '최고의 조합! 💝'],
        70: ['좋은 케미! 😊', '균형잡힌 관계! ⚖️', '서로 다른 매력! 🎭'],
        60: ['성장하는 케미! 🌱', '흥미로운 조합! 🎪', '도전적인 케미! 💪'],
        50: ['새로운 경험! 🚀', '배움의 기회! 📚', '특별한 만남! ⭐']
    }
    
    for threshold in sorted(descriptions.keys(), reverse=True):
        if score >= threshold:
            return random.choice(descriptions[threshold])
    return '새로운 경험! 🚀'

def generate_warning_signal(mbti1, mbti2, score):
    """위험 신호 생성"""
    key1 = f"{mbti1}-{mbti2}"
    key2 = f"{mbti2}-{mbti1}"
    
    if key1 in SPECIAL_WARNINGS:
        return SPECIAL_WARNINGS[key1]
    if key2 in SPECIAL_WARNINGS:
        return SPECIAL_WARNINGS[key2]
    
    if score >= 85:
        category = 'high_score'
    elif score >= 70:
        category = 'medium_score'
    else:
        category = 'low_score'
    
    return random.choice(WARNING_PATTERNS[category])

def generate_chemistry_analysis(user_mbti, partner_mbti, user_name="OO", partner_name="OO", analysis_type="predicted"):
    """초안 기반 케미 분석 생성"""
    score, description = get_chemistry_score(user_mbti, partner_mbti)
    score_desc = get_score_description(score)
    warning = generate_warning_signal(user_mbti, partner_mbti, score)
    
    user_animal = MBTI_CHARACTERS[user_mbti]['animal']
    partner_animal = MBTI_CHARACTERS[partner_mbti]['animal']
    
    type_description = "실제 MBTI 기반" if analysis_type == 'original' else "대화 분석 기반 예측"
    
    return {
        "analysis_type": analysis_type,
        "partner_mbti": partner_mbti,
        "chemistry_score": score,
        "chemistry_description": f"**{user_name}과 {partner_name}은 {user_animal}와 {partner_animal} – {description}**",
        "score_summary": f"**우리의 케미 점수: {score}점! ({score_desc}) [{type_description}]**",
        "warning_signal": f"⚠️ **위험 신호:** {warning}",
        "character_info": {
            "user": MBTI_CHARACTERS[user_mbti],
            "partner": MBTI_CHARACTERS[partner_mbti]
        }
    }


def analyze_mbti_personality(profile, content):
    """MBTI 성격 분석 메인 함수"""
    client = get_openai_client()
    
    # 프롬프트 템플릿 사용
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
            # 프로필에서 상대방 MBTI 확인 후 original 섹션 제거 로직
            profile_data = result.get('profile', {})
            partner_mbti_from_profile = profile_data.get('partner_mbti', '').strip()
            
            if not partner_mbti_from_profile:
                mbti_prediction = result.get('mbti_prediction', {})
                if 'original' in mbti_prediction:
                    print("⚠️ 상대방 MBTI가 프로필에 없으므로 original 섹션을 제거합니다.")
                    del mbti_prediction['original']
            
            # 케미 분석 추가
            result = _add_chemistry_analysis(result)
            return json.dumps(result, ensure_ascii=False, indent=2)
        
        return gpt_result
    except Exception as e:
        print(f"Error processing result: {e}")
        return gpt_result

def _add_chemistry_analysis(result):
    """케미 분석 추가"""
    profile_data = result.get('profile', {})
    mbti_prediction = result.get('mbti_prediction', {})
    
    user_mbti = profile_data.get('user_mbti')
    user_name = profile_data.get('user_name', 'OO')
    partner_name = profile_data.get('partner_name', '상대방')
    partner_mbti_from_profile = profile_data.get('partner_mbti', '').strip()
    
    chemistry_analyses = []
    
    # Original 케미 분석
    if (partner_mbti_from_profile and 
        mbti_prediction.get('original') and 
        mbti_prediction['original'].get('type')):
        
        original_mbti = mbti_prediction['original']['type']
        if user_mbti and original_mbti:
            original_chemistry = generate_chemistry_analysis(
                user_mbti, original_mbti, user_name, partner_name, 'original'
            )
            original_chemistry['title'] = f"원래 MBTI ({original_mbti})와의 케미"
            chemistry_analyses.append(original_chemistry)
    
    # Predicted 케미 분석
    if (mbti_prediction.get('predict') and 
        mbti_prediction['predict'].get('type')):
        
        predicted_mbti = mbti_prediction['predict']['type']
        if user_mbti and predicted_mbti:
            predicted_chemistry = generate_chemistry_analysis(
                user_mbti, predicted_mbti, user_name, partner_name, 'predicted'
            )
            predicted_chemistry['title'] = f"예측 MBTI ({predicted_mbti})와의 케미"
            chemistry_analyses.append(predicted_chemistry)
    
    if chemistry_analyses:
        result['chemistry_analysis'] = chemistry_analyses
    
    return result

def analyze_mbti_from_file(profile_path, content_path):
    """파일에서 MBTI 분석"""
    try:
        with open(profile_path, 'r', encoding='utf-8') as profile_file:
            profile = profile_file.read()
            
        with open(content_path, 'r', encoding='utf-8') as content_file:
            content = content_file.read()
            
        return analyze_mbti_personality(profile, content)
        
    except Exception as e:
        print(f"파일 처리 중 오류 발생: {e}")
        return {"error": str(e)}