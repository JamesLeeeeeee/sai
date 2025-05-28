import requests, json

url = "http://localhost:5000/analyze-mbti-file"

# 파일 준비
files = {
    'profile': open('profile.txt', 'rb'),
    'content': open('content.txt', 'rb')
}

response = requests.post(url, files=files)
print("Status Code:", response.status_code)
print("Response:")
print(response.json())

if response.status_code == 200:
    # 응답에서 result 키의 값을 가져와서 JSON으로 파싱
    result_str = response.json()['result']
    result_json = json.loads(result_str)

    # sample.json 파일로 저장 (들여쓰기 적용)
    with open('sample2.json', 'w', encoding='utf-8') as f:
        json.dump(result_json, f, ensure_ascii=False, indent=2)

    print("✅ 결과가 sample.json 파일에 저장되었습니다!")
    print(f"📊 케미 분석 개수: {len(result_json.get('chemistry_analysis', []))}")
    print(f"🎯 예측된 MBTI: {result_json.get('mbti_prediction', {}).get('predict', {}).get('type', 'N/A')}")

else:
    print(f"❌ 오류 발생: {response.status_code}")
    print(response.text)