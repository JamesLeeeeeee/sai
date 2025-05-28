# MBTI 분석 API

## 프로젝트 소개
이 프로젝트는 카카오톡 대화 내용을 기반으로 상대방의 MBTI 성격유형을 분석하는 REST API를 제공합니다. OpenAI의 GPT 모델을 활용하여 대화 내용을 분석하고 상대방의 성격, 대화 스타일, 호감도, MBTI 케미 분석 등을 제공합니다.

## 주요 기능
- 📊 **MBTI 성격유형 추정**: 대화 분석 기반 예측 (신뢰도 포함)
- 💕 **호감도 분석**: 상호 호감도 점수 및 인사이트 제공
- 🎭 **대화 스타일 분석**: 톤과 패턴 분석
- 🔥 **MBTI 케미 분석**: 사용자와 상대방의 궁합 점수
- 🎯 **맞춤형 조언**: 대화 개선 조언 및 액션 플랜
- 🐾 **동물 캐릭터**: 각 MBTI를 귀여운 동물로 표현

## 새로운 기능 (v2.0)
- **Original vs Predict**: 프로필의 실제 MBTI와 대화 기반 예측 MBTI 비교
- **케미 점수**: 16가지 MBTI 조합별 상성 분석
- **위험 신호**: 재미있는 관계 경고 메시지
- **파일 업로드**: 프로필과 대화 파일 분리 업로드

## 기술 스택
- Python 3.8+
- Flask (RESTful API 프레임워크)  
- OpenAI API (GPT-4o-mini)

## 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/yourusername/mbti-analyzer.git
cd mbti-analyzer
```

### 2. 가상환경 설정 및 의존성 설치
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. 환경 변수 설정
.env 파일을 생성하고 OpenAI API 키를 설정합니다:
```
OPENAI_API_KEY=your-api-key-here
```

## 사용 방법

### 1. 서버 실행
```bash
python run.py
```
서버는 기본적으로 `http://0.0.0.0:5000`에서 실행됩니다.

### 2. API 엔드포인트

#### A. 텍스트 기반 분석
```bash
curl -X POST http://localhost:5000/analyze-mbti \
  -H "Content-Type: application/json" \
  -d '{
    "profile": "사용자 이름: 준호\nMBTI: ESTJ\n성별: 남\n\n상대방 이름: 지민",
    "content": "카카오톡 대화 내용..."
  }'
```

#### B. 파일 업로드 분석 (권장)
```bash
curl -X POST http://localhost:5000/analyze-mbti-file \
  -F "profile=@profile.txt" \
  -F "content=@content.txt"
```

### 3. 파일 형식 예시

**profile.txt:**
```
사용자 이름: 준호
MBTI: ESTJ
성별: 남

상대방 이름: 지민
상대방 MBTI: ISFP
```

**content.txt:**
```
--------------- 2024년 5월 31일 금요일 ---------------
[민준] [오전 10:16] [사진]
[민준] [오전 10:16] 회사 근처에 강아지풀이 바람에 흔들리는데 예뻐서요.. 갑자기 생각나서요 ㅎㅎ
[수현] [오전 10:17] 어머 사진 예뻐요! 저도 민준님 생각났어요 (아침에 출근길에..!)
[민준] [오전 10:17] ㅋㅋㅋ 아침부터 생각해주시다니 영광인데요? 😄 오늘 점심은 뭐 드실 예정이세요?
[수현] [오전 10:18] 아직 딱히 정한 곳은 없어요. 민준님은요?
[민준] [오전 10:18] 저도 아직인데요.. 혹시 근처시면... 같이 먹을 수도 있나.. 싶어서요 (무리수일까요? ㅋㅋ)
[수현] [오전 10:19] 엇? 생각보다 가까울지도 모르겠네요! 어디신데요? 알려주시면...
...
```

## API 응답 형식 (v2.0)
```json
{
  "profile": {
    "user_name": "준호",
    "user_mbti": "ESTJ", 
    "partner_name": "지민",
    "partner_mbti": "ISFP"
  },
  "mbti_prediction": {
    "original": {
      "type": "ISFP",
      "confidence": "100%",
      "animal_character": "나비",
      "character_type": "감성적인 예술가",
      "mbti_comments": "프로필에 제시된 ISFP..."
    },
    "predict": {
      "type": "ESFJ", 
      "confidence": "75%",
      "animal_character": "판다",
      "character_type": "따뜻한 케어베어",
      "mbti_comments": "대화 분석 결과..."
    }
  },
  "likability_score": {
    "user": "80%",
    "partner": "75%" 
  },
  "conversational_tone": {
    "user": "친근함",
    "partner": "공감적"
  },
  "likability_comments": [
    "질문이 많아요!🤔\n상대방이 5번의 질문을 던졌어요...",
    "긍정적 반응!✨\n웃음과 긍정 표현이 많네요..."
  ],
  "solutions": {
    "conversation_advice": [
      "공통 관심사 찾기 🔍\n취미에 대해 더 물어보세요"
    ],
    "action_plan": [
      "다음 만남 제안 📅\n구체적인 계획을 세워보세요"
    ]
  },
  "chemistry_analysis": [
    {
      "analysis_type": "original",
      "partner_mbti": "ISFP", 
      "chemistry_score": 68,
      "chemistry_description": "**준호과 지민은 사자와 나비 – 강한 추진력과 섬세한 감성의 대조적 케미**",
      "score_summary": "**우리의 케미 점수: 68점! (대조적인 매력! 🎭)**",
      "warning_signal": "⚠️ **위험 신호:** 사자가 나비의 섬세함에 매료되어 계획을 바꿀 위험!",
      "character_info": {
        "user": {
          "animal": "사자",
          "type": "체계적인 관리자", 
          "traits": ["책임감 있는", "조직적인"],
          "keywords": ["책임", "체계", "안정"]
        },
        "partner": {
          "animal": "나비",
          "type": "감성적인 예술가",
          "traits": ["온화한", "예술적인"],
          "keywords": ["감성", "예술", "자유"]
        }
      }
    }
  ]
}
```

## 프로젝트 구조 (v2.0)
```
d:\study\sai\
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── data/                    # 🆕 데이터 파일들
│   │   ├── mbti_characters.py   # MBTI 캐릭터 정보
│   │   ├── compatibility_matrix.py # 궁합 매트릭스  
│   │   └── warning_patterns.py  # 위험 신호 패턴
│   ├── routes/
│   │   ├── __init__.py
│   │   └── mbti_routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── mbti_service.py      # 메인 분석 로직
│   │   └── chemistry_service.py # 🆕 케미 분석 서비스
│   ├── templates/               # 🆕 프롬프트 템플릿
│   │   └── prompts.py
│   └── utils/
│       ├── __init__.py
│       ├── openai_utils.py
│       └── json_utils.py        # 🆕 JSON 처리 유틸
├── test/                        # 🆕 테스트 파일들
│   ├── profile.txt
│   ├── content.txt
│   └── test_file.py
├── .env
├── requirements.txt
├── run.py
└── README.md
```

## 테스트 방법

### 1. 간단한 텍스트 테스트
```bash
python test/test_simple.py
```

### 2. 파일 업로드 테스트 
```bash
cd test
python test_file.py
```

### 3. 결과를 JSON 파일로 저장
```bash
cd test  
python save_sample.py  # sample.json 생성
```

## MBTI 동물 캐릭터 🐾
- **ENTJ**: 불도저 - 직진형 리더
- **ENFP**: 꽃사슴 - 감성형 꿈쟁이  
- **INTJ**: 올빼미 - 전략형 마스터플래너
- **INFP**: 유니콘 - 순수한 꿈꾸는 예술가
- **ESTJ**: 사자 - 체계적인 관리자
- **ESFP**: 앵무새 - 자유로운 엔터테이너
- **ISFP**: 나비 - 감성적인 예술가
- **ISFJ**: 토끼 - 조용한 수호천사
- ...등 16가지

## 주의사항
- OpenAI API 사용에는 비용이 발생할 수 있으니 API 호출 빈도와 사용량에 주의하세요.
- 대화 내용 분석 시 개인정보를 포함하지 않도록 주의하세요.
- API 키는 절대 공개 저장소에 업로드하지 마세요.
- 분석 결과는 엔터테인먼트 목적이며, 실제 심리학적 진단이 아닙니다.

## 라이선스
MIT License
