from app.utils.openai_utils import get_openai_client

def analyze_mbti_personality(target_name, content):
    client = get_openai_client()
    
    prompt = f"""
            다음은 사용자와 {target_name} 간의 카카오톡 대화입니다.
            {target_name}의 성격을 분석하고, MBTI 성격유형을 추정해 주세요.

            요구사항:
            1. MBTI 각 항목(E/I, S/N, T/F, J/P)의 확률 (%)을 추정해 주세요.
            2. 최종 조합(예: ENFP 가능성 70%)을 제시해 주세요.
            3. 상대방의 대화 스타일을 요약해 주세요.
            4. 감정 표현 Top 3를 추출하고 설명해 주세요.
            5. 대화 주제 및 공통 관심사를 정리해 주세요.
            6. 상대방과 더 나은 대화를 위한 조언을 제시해 주세요.

            추가 요청사항:
            - 모든 설명은 너무 딱딱하거나 로봇처럼 들리지 않게 해 주세요.
            - 말투는 가볍고 친근하면서도 분석적이어야 합니다. (예: 친구에게 설명하듯)
            - 예: "상대방이 자주 웃는 표현을 쓰고, 대화를 긍정적으로 받아줘요. 이건 꽤 호감의 신호일 수 있어요."
                "'같이 가자', '나중에 또 보자' 같은 표현이 자주 보이네요. 친밀감을 표현하는 성향이 뚜렷해요!"
            - 대화 조언도 실제 대화에 쓸 수 있는 말투로 써 주세요.

            출력은 다음 JSON 형식으로 제공해 주세요:

            {{
            "mbti_prediction": {{
                "E": "60%", "I": "40%",
                "S": "70%", "N": "30%",
                "T": "80%", "F": "20%",
                "J": "65%", "P": "35%",
                "final": {{
                "type": "ESTJ",
                "confidence": "75%",
                "mbti_commemts": "이재관 님은 상대방의 말에 따뜻하게 반응하고, 관심을 지속적으로 표현하는 성격의 ENFP 유형일 가능성이 높아요. 감정에 진심을 담아 소통하려는 태도가 돋보여요!"
                }}
            }},
            "personality_summary": "...",
            "emotion_keywords_top3": ["...", "...", "..."],
            "topic_analysis": {{
                "personal_topics": [...],
                "shared_topics": [...],
                "frequency_ranking": [...],
                "topic_comments": [...]
            }},
            "conversation_advice": [
                "...",
                "...",
                "..."
            ]
            }}

            분석 대상 대화:
            \"\"\"{content}\"\"\"
            """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 사용 중인 모델명에 맞게 수정
        messages=[
            {"role": "system", "content": "너는 MBTI 성격 분석 전문가야. 그리고 대화 내용을 기반으로 상대방의 성격을 추론해."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
    )

    return response.choices[0].message.content