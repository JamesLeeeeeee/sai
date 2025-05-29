import requests
import json

def test_simple_mbti_analysis():
    """간단한 텍스트 기반 MBTI 분석 테스트"""
    
    url = "http://localhost:5000/analyze-mbti"
    
    payload = {
        "profile": """
        사용자 이름: 김철수
        MBTI: ENFP
        성별: 남
        
        상대방 이름: 이영희
        """,
        "content": """
        [김철수] 안녕하세요! 오늘 날씨 좋네요 ㅎㅎ
        [이영희] 네, 정말 좋아요. 산책하기 딱 좋은 날씨예요.
        [김철수] 우와! 영희님도 산책 좋아하시는군요? 저도 산책 엄청 좋아해요!
        [이영희] 네, 조용한 곳에서 생각 정리하는 걸 좋아해서요.
        """
    }
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 간단 테스트 성공!")
            print(f"예측 MBTI: {result.get('mbti_prediction', {}).get('predict', {}).get('type', 'N/A')}")
            print(f"케미 분석: {len(result.get('chemistry_analysis', []))}개")
            return True
        else:
            print(f"❌ 테스트 실패: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 연결 실패: {e}")
        print("서버가 실행 중인지 확인하세요: python run.py")
        return False

if __name__ == "__main__":
    print("=== 🚀 간단한 MBTI 분석 테스트 ===")
    test_simple_mbti_analysis()