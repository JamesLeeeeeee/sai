import requests
import json

def save_sample_result():
    """샘플 분석 결과를 JSON 파일로 저장"""
    
    url = "http://localhost:5000/analyze-mbti-file"
    
    files = {
        'profile': open('profile.txt', 'rb'),
        'content': open('content.txt', 'rb')
    }
    
    try:
        response = requests.post(url, files=files)
        
        if response.status_code == 200:
            result = response.json()
            
            # JSON 문자열을 파싱
            if isinstance(result, str):
                result_dict = json.loads(result)
            else:
                result_dict = result
            
            # sample.json으로 저장
            with open('sample.json', 'w', encoding='utf-8') as f:
                json.dump(result_dict, f, ensure_ascii=False, indent=2)
            
            print("✅ 샘플 결과가 test/sample.json에 저장되었습니다!")
            print(f"📊 케미 분석: {len(result_dict.get('chemistry_analysis', []))}개")
            
        else:
            print(f"❌ 요청 실패: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        files['profile'].close()
        files['content'].close()

if __name__ == "__main__":
    print("=== 📁 샘플 결과 저장 ===")
    save_sample_result()