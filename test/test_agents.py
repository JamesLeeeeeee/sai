# test/test_agents.py
import asyncio
import sys
import os

# 프로젝트 루트(/workspaces/sai)를 Python 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

print(f"프로젝트 루트: {project_root}")  # 디버깅용

# 이제 정상적으로 import 가능
from app.agents.chemistry_agent import ChemistryAgent
from app.agents.mbti_analyzer_agent import MBTIAnalyzerAgent
from app.mcp_servers.mbti_data_server import MBTIDataClient

async def test_mcp_server():
    """MCP 서버 테스트"""
    print("=== 🔧 MCP 서버 테스트 ===")
    
    try:
        client = MBTIDataClient()
        
        # 캐릭터 정보 테스트
        print("\n1. 캐릭터 정보 테스트:")
        enfp_char = await client.get_character_info("ENFP")
        print(f"   ENFP: {enfp_char.get('animal', '정보없음')} - {enfp_char.get('type', '정보없음')}")
        
        intj_char = await client.get_character_info("INTJ")
        print(f"   INTJ: {intj_char.get('animal', '정보없음')} - {intj_char.get('type', '정보없음')}")
        
        # 케미 점수 테스트
        print("\n2. 케미 점수 테스트:")
        chemistry = await client.get_compatibility_score("ENFP", "INTJ")
        if chemistry:
            print(f"   ENFP-INTJ: {chemistry.get('base')}점")
            print(f"   설명: {chemistry.get('description')}")
        else:
            print("   ENFP-INTJ: 기본 케미 적용")
        
        print("✅ MCP 서버 테스트 성공!")
        
    except Exception as e:
        print(f"❌ MCP 서버 테스트 실패: {e}")
        import traceback
        traceback.print_exc()

async def test_chemistry_agent():
    """Chemistry Agent 테스트"""
    print("\n=== 💕 Chemistry Agent 테스트 ===")
    
    try:
        agent = ChemistryAgent()
        
        # 단일 케미 분석
        print("\n1. 단일 케미 분석:")
        result = await agent.analyze_chemistry(
            user_mbti="ENFP",
            partner_mbti="INTJ", 
            user_name="민수",
            partner_name="영희"
        )
        
        print(f"   점수: {result['chemistry_score']}")
        print(f"   설명: {result['chemistry_description']}")
        print(f"   요약: {result['score_summary']}")
        print(f"   위험신호: {result['warning_signal']}")
        
        print("✅ Chemistry Agent 테스트 성공!")
        
    except Exception as e:
        print(f"❌ Chemistry Agent 테스트 실패: {e}")
        import traceback
        traceback.print_exc()

async def test_integration():
    """통합 테스트 (OpenAI API 호출 없음)"""
    print("\n=== 🤖 통합 테스트 ===")
    
    try:
        # 가짜 GPT 결과 시뮬레이션
        fake_result = {
            "profile": {
                "user_name": "준호",
                "user_mbti": "ESTJ",
                "partner_name": "지민",
                "partner_mbti": ""  # 프로필에 없음
            },
            "mbti_prediction": {
                "predict": {
                    "type": "ESFJ",
                    "confidence": "80%"
                }
            }
        }
        
        # Chemistry Agent로 케미 분석 추가
        analyzer = MBTIAnalyzerAgent()
        result = await analyzer._add_chemistry_analysis_with_agent(fake_result)
        
        print("전체 분석 결과:")
        print(f"   사용자: {result['profile']['user_name']} ({result['profile']['user_mbti']})")
        print(f"   상대방: {result['profile']['partner_name']}")
        print(f"   예측 MBTI: {result['mbti_prediction']['predict']['type']}")
        
        if 'chemistry_analysis' in result:
            print(f"   케미 분석: {len(result['chemistry_analysis'])}개")
            for analysis in result['chemistry_analysis']:
                print(f"   - {analysis.get('title', 'Unknown')}: {analysis.get('chemistry_score')}점")
        
        print("✅ 통합 테스트 성공!")
        
    except Exception as e:
        print(f"❌ 통합 테스트 실패: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """모든 테스트 실행"""
    print("🚀 Agent + MCP 구조 테스트 시작!")
    print("=" * 50)
    
    await test_mcp_server()
    await test_chemistry_agent()
    await test_integration()
    
    print("\n" + "=" * 50)
    print("✅ 모든 테스트 완료!")

if __name__ == "__main__":
    asyncio.run(main())