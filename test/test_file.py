import requests

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