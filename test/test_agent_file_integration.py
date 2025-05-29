# test/test_agent_file_integration.py
import json
import sys
import os

# 프로젝트 루트 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_agent_with_existing_files():
    """기존 테스트 파일로 Agent 구조 검증"""
    print("=== 📁 기존 파일로 Agent 구조 테스트 ===")
    
    from app import create_app
    from app.services.mbti_service import analyze_mbti_from_file
    
    app = create_app()
    
    profile_path = 'test/profile.txt'
    content_path = 'test/content.txt'
    
    with app.app_context():
        try:
            # Agent 방식으로 파일 분석
            result = analyze_mbti_from_file(profile_path, content_path)
            
            print("✅ Agent 파일 분석 성공!")
            
            # JSON 파싱
            if isinstance(result, str):
                result_dict = json.loads(result)
            else:
                result_dict = result
            
            # 결과 분석
            profile = result_dict.get('profile', {})
            chemistry = result_dict.get('chemistry_analysis', [])
            prediction = result_dict.get('mbti_prediction', {})
            
            print(f"\n📊 분석 결과:")
            print(f"   사용자: {profile.get('user_name')} ({profile.get('user_mbti')})")
            print(f"   상대방: {profile.get('partner_name')}")
            print(f"   예측 MBTI: {prediction.get('predict', {}).get('type', 'N/A')}")
            print(f"   케미 분석: {len(chemistry)}개")
            
            for i, chem in enumerate(chemistry, 1):
                print(f"     {i}. {chem.get('title')}: {chem.get('chemistry_score')}점")
            
            # Agent 테스트 결과 저장
            with open('test/agent_file_test_result.json', 'w', encoding='utf-8') as f:
                json.dump(result_dict, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 Agent 테스트 결과 저장: test/agent_file_test_result.json")
            
            return True
            
        except Exception as e:
            print(f"❌ Agent 파일 테스트 실패: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = test_agent_with_existing_files()
    if success:
        print("\n🎉 Agent + 파일 업로드 완벽 작동!")
    else:
        print("\n💥 Agent 파일 테스트 실패")