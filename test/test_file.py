import requests
import json

url = "http://localhost:5000/analyze-mbti-file"

try:
    # 파일 준비
    files = {
        'profile': open('profile.txt', 'rb'),
        'content': open('content.txt', 'rb')
    }

    response = requests.post(url, files=files)
    print("Status Code:", response.status_code)
    
    if response.status_code == 200:
        # 🔧 수정: 이제 response.json()이 바로 결과 JSON입니다
        result_json = response.json()
        
        print("✅ API 호출 성공!")
        print(f"📊 케미 분석 개수: {len(result_json.get('chemistry_analysis', []))}")
        print(f"🎯 예측된 MBTI: {result_json.get('mbti_prediction', {}).get('predict', {}).get('type', 'N/A')}")
        print(f"👤 사용자: {result_json.get('profile', {}).get('user_name', 'N/A')}")
        print(f"💕 호감도: 사용자 {result_json.get('likability_score', {}).get('user', 'N/A')}, 상대방 {result_json.get('likability_score', {}).get('partner', 'N/A')}")
        
        # sample.json 파일로 저장 (들여쓰기 적용)
        with open('sample.json', 'w', encoding='utf-8') as f:
            json.dump(result_json, f, ensure_ascii=False, indent=2)
        
        print("📁 결과가 sample.json 파일에 저장되었습니다!")
        
    else:
        print(f"❌ 오류 발생: {response.status_code}")
        print("Response:", response.text)
        
except FileNotFoundError as e:
    print(f"📁 파일을 찾을 수 없습니다: {e}")
    print("현재 디렉토리에 profile.txt와 content.txt 파일이 있는지 확인해주세요.")
except Exception as e:
    print(f"❌ 예상치 못한 오류: {e}")
finally:
    # 파일 핸들 정리
    if 'files' in locals():
        for f in files.values():
            f.close()