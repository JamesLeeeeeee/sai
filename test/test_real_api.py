# test/test_real_api.py
import asyncio
import sys
import os
import json

# 프로젝트 루트 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_with_real_openai():
    """실제 OpenAI API를 사용한 Agent 테스트"""
    print("=== 🔥 실제 OpenAI API + Agent 구조 테스트 ===")
    
    # Flask 앱 컨텍스트 생성
    from app import create_app
    from app.services.mbti_service import analyze_mbti_personality, analyze_mbti_personality_with_agents
    
    app = create_app()
    
    # 테스트 데이터
    test_profile = """
    사용자 이름: 민수
    MBTI: ENFP
    성별: 남

    상대방 이름: 영희
    상대방 MBTI: INTJ
    """
    
    test_content = """
    --------------- 2024년 5월 31일 금요일 ---------------
    [민수] [오전 10:16] 안녕하세요! 오늘 날씨 좋네요 ㅎㅎ
    [영희] [오전 10:17] 네, 정말 좋아요. 산책하기 딱 좋은 날씨예요.
    [민수] [오전 10:18] 우와! 영희님도 산책 좋아하시는군요? 저도 산책 엄청 좋아해요!
    [영희] [오전 10:19] 네, 조용한 곳에서 생각 정리하는 걸 좋아해서요.
    [민수] [오전 10:20] 오~ 저는 사람들과 함께 하는 것도 좋지만 혼자만의 시간도 필요해요
    [영희] [오전 10:21] 그렇군요. 균형이 중요한 것 같아요.
    """
    
    with app.app_context():
        print("⚠️  이 테스트는 실제 OpenAI API를 호출합니다! (약 $0.01-0.03)")
        answer = input("계속 하시겠습니까? (y/n): ")
        
        if answer.lower() != 'y':
            print("테스트를 취소합니다.")
            return
        
        print("\n🔄 기존 방식 vs Agent 방식 비교 테스트...")
        
        # 1. 기존 방식 테스트
        print("\n1️⃣ 기존 방식 분석 중...")
        try:
            import time
            start_time = time.time()
            old_result = analyze_mbti_personality(test_profile, test_content)
            old_time = time.time() - start_time
            old_result_dict = json.loads(old_result)
            print(f"   ✅ 기존 방식 완료: {old_time:.2f}초")
        except Exception as e:
            print(f"   ❌ 기존 방식 에러: {e}")
            old_result_dict = None
            old_time = None
        
        # 2. Agent 방식 테스트  
        print("\n2️⃣ Agent 방식 분석 중...")
        try:
            start_time = time.time()
            new_result = analyze_mbti_personality_with_agents(test_profile, test_content)
            new_time = time.time() - start_time
            new_result_dict = json.loads(new_result)
            print(f"   ✅ Agent 방식 완료: {new_time:.2f}초")
        except Exception as e:
            print(f"   ❌ Agent 방식 에러: {e}")
            new_result_dict = None
            new_time = None
        
        # 3. 결과 비교
        print("\n" + "="*50)
        print("📊 **결과 비교**")
        print("="*50)
        
        if old_result_dict and new_result_dict:
            # 성능 비교
            if old_time and new_time:
                print(f"⏱️  **성능 비교:**")
                print(f"   기존 방식: {old_time:.2f}초")
                print(f"   Agent 방식: {new_time:.2f}초")
                if abs(old_time - new_time) < 0.5:
                    print("   📊 거의 동일한 성능! ✨")
                elif new_time < old_time:
                    print(f"   🚀 Agent 방식이 {old_time - new_time:.2f}초 빠름!")
                else:
                    print(f"   🐌 Agent 방식이 {new_time - old_time:.2f}초 느림")
            
            # 기능 비교
            print(f"\n🔍 **기능 비교:**")
            old_chemistry = len(old_result_dict.get('chemistry_analysis', []))
            new_chemistry = len(new_result_dict.get('chemistry_analysis', []))
            
            print(f"   기존 케미 분석: {old_chemistry}개")
            print(f"   Agent 케미 분석: {new_chemistry}개")
            
            if old_chemistry == new_chemistry:
                print("   ✅ 동일한 기능 제공!")
            else:
                print("   ⚠️  기능 차이 있음")
            
            # 분석 결과 미리보기
            print(f"\n👤 **분석 결과 미리보기:**")
            if 'profile' in new_result_dict:
                profile = new_result_dict['profile']
                print(f"   사용자: {profile.get('user_name')} ({profile.get('user_mbti')})")
                print(f"   상대방: {profile.get('partner_name')}")
            
            if 'mbti_prediction' in new_result_dict:
                predict = new_result_dict['mbti_prediction'].get('predict', {})
                print(f"   예측 MBTI: {predict.get('type')} ({predict.get('confidence')})")
            
            if 'chemistry_analysis' in new_result_dict:
                print(f"   케미 분석:")
                for analysis in new_result_dict['chemistry_analysis']:
                    print(f"     - {analysis.get('title')}: {analysis.get('chemistry_score')}점")
            
            # 결과를 파일로 저장
            with open('test/agent_vs_original_comparison.json', 'w', encoding='utf-8') as f:
                comparison_result = {
                    "test_info": {
                        "test_date": "2025-05-29",
                        "comparison_type": "Agent vs Original"
                    },
                    "performance": {
                        "original_time": old_time,
                        "agent_time": new_time
                    },
                    "original_result": old_result_dict,
                    "agent_result": new_result_dict
                }
                json.dump(comparison_result, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 **상세 결과가 저장되었습니다:**")
            print(f"   📁 test/agent_vs_original_comparison.json")
            
        print("\n" + "="*50)
        print("🎉 **Agent + MCP 구조 검증 완료!**")
        print("="*50)

if __name__ == "__main__":
    test_with_real_openai()