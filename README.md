# 📚 2025년도 전기기능사 문제풀이 시스템 구축 가이드

## 🎯 목표
docx 파일을 분석하여 JSON 형식의 문제 데이터베이스를 만들고, 이를 이용해 문제풀이 시스템을 구현합니다.

---

## 📋 분석 자료

### 📄 필독 자료
- **ANALYSIS_REPORT.md**: docx 파일의 완벽한 구조 분석 보고서
  - 각 파일의 구성 방식
  - 데이터 추출 패턴
  - 주의사항
  - JSON 형식

### 🔍 분석 스크립트
```bash
python analyze_docx.py
```
필요할 때마다 docx 파일의 최신 구조를 확인할 수 있습니다.

---

## 🛠️ 구현 단계

### 1단계: 기본 클래스 구현 ⭐
**파일**: `extract.py` (직접 작성)

필요한 것:
- `QuestionExtractor` 클래스
  - `extract_from_docx()`: 문제 추출 로직
  - `save_json()`: JSON 저장

```python
# 참고: template.py의 QuestionExtractor 클래스 구조
```

**핵심 로직**:
1. docx 파일의 모든 문단 순회
2. "제X회"를 찾아 현재_회차 저장
3. "숫자."로 시작하는 문단을 문제로 인식
4. 정답 심볼(①②③④) 추출
5. 다음 문단에서 선택지 추출

**수도코드**:
```
for 각 문단:
    if "제" in 문단 and "회" in 문단:
        현재_회차 = extract_round()
    
    if regex.match(r'^(\d+)\.\s+', 문단):
        문제 = {
            'number': 문제번호,
            'question': 문제텍스트,
            'options': 선택지들,
            'answer': 정답인덱스,
            'exam': 현재_회차
        }
        저장(문제)
```

### 2단계: 설명 추출 구현
**파일**: `extract.py` (계속)

필요한 것:
- `ExplanationExtractor` 클래스
  - `extract_from_docx()`: 설명 추출 로직

**핵심 로직**:
1. docx의 모든 표 순회
2. 각 표의 첫 번째 셀에서 텍스트 추출
3. "설명: 단원명-" 부분 제거
4. 문제번호와 연결

**주의**: 
- 설명.docx의 표는 문제 순서대로 배열됨
- 표의 인덱스와 문제번호가 일치하지 않을 수 있음

### 3단계: 데이터 통합
**파일**: `extract.py` (계속)

필요한 것:
- 문제와 설명을 매칭하는 로직

```python
# 문제번호를 기준으로 설명 추가
for 각 문제:
    해당_설명 = 설명맵[문제번호]
    문제['explanation'] = 해당_설명
```

### 4단계: 검증 (선택)
**파일**: `validate.py` (직접 작성)

체크할 것:
- 모든 75개 문제가 추출되었나?
- 각 회차별 문제 개수가 맞나?
- 모든 선택지가 4개인가?
- 정답이 모두 있나?

```python
def validate(questions):
    """
    확인 사항:
    - total == 75
    - 제1회: 32개, 제2회: 16개, 제3회: 12개, 제4회: 15개
    - 모든 문제가 옵션 4개, 정답 1개를 가짐
    """
```

### 5단계: 웹 인터페이스 (선택)
**파일**: `index.html`, `style.css`, `app.js` (직접 작성)

기능:
- 문제 표시
- 정답 선택
- 즉시 정답 + 설명 표시
- 진행률 표시
- 최종 성적 계산

### 6단계: CLI 도구 (선택)
**파일**: `cli.py` (직접 작성)

기능:
```bash
python cli.py                # 모든 문제 풀기
python cli.py -p 5          # 문제 5번만
python cli.py -s "변압기"   # 검색
```

---

## 📝 JSON 파일 구조

### questions.json
```json
{
  "total": 75,
  "questions": [
    {
      "number": 1,
      "question": "진동이 심한...",
      "options": ["선지1", "선지2", "선지3", "선지4"],
      "answer": 3,
      "exam": "제1회"
    }
  ]
}
```

### example.json
```json
{
  "total": 47,
  "examples": [
    {
      "problem_number": 1,
      "category": "전기설비",
      "explanation": "- 진동이 있는..."
    }
  ]
}
```

### integrated_questions.json (통합)
```json
{
  "total": 75,
  "questions": [
    {
      "number": 1,
      "question": "진동이 심한...",
      "options": ["선지1", "선지2", "선지3", "선지4"],
      "answer": 3,
      "explanation": "- 진동이 있는...",
      "exam": "제1회"
    }
  ]
}
```

---

## 🔧 추천 구현 순서

### 빠른 구현 (1-2시간)
```
Step 1: 문제 추출 (extract.py)
Step 2: 설명 추출 (extract.py)
Step 3: 데이터 통합 (extract.py)
Step 4: JSON 생성
```

### 완벽한 구현 (3-4시간)
```
위 + Step 5 (검증)
+ Step 6 (웹 인터페이스)
+ Step 7 (CLI 도구)
```

---

## 💡 팁

### 정규식 참고
```python
import re

# 문제 찾기
match = re.match(r'^(\d+)\.\s+(.+)$', text)
if match:
    num = int(match.group(1))      # 문제번호
    rest = match.group(2)           # 나머지 텍스트

# 정답 심볼 찾기
for symbol, idx in {'①': 0, '②': 1, '③': 2, '④': 3}.items():
    if rest.endswith(symbol):
        answer = idx
        question = rest[:-len(symbol)].strip()

# 선택지 추출
option_pattern = r'[①②③④]\s*([^①②③④]+?)(?=[①②③④]|$)'
matches = re.findall(option_pattern, next_text)
options = [m.strip() for m in matches]
```

### 디버깅
```python
# 진행 상황 확인
print(f"✓ {len(questions)}개 문제 추출됨")
print(f"  제1회: {len([q for q in questions if q['exam']=='제1회'])}개")

# 특정 문제 확인
q = [q for q in questions if q['number'] == 1][0]
print(json.dumps(q, ensure_ascii=False, indent=2))
```

---

## 📚 참고 파일

| 파일 | 설명 |
|------|------|
| `ANALYSIS_REPORT.md` | ⭐ 필독: 상세 분석 보고서 |
| `analyze_docx.py` | 분석 도구 (재실행 가능) |
| `template.py` | 기본 클래스 템플릿 |
| `2025년도 문제.docx` | 원본 데이터 |
| `2025년도 설명.docx` | 원본 데이터 |

---

## ✅ 완료 체크리스트

- [ ] ANALYSIS_REPORT.md 읽음
- [ ] analyze_docx.py 실행해봄
- [ ] extract.py 작성 시작
  - [ ] QuestionExtractor 구현
  - [ ] ExplanationExtractor 구현
  - [ ] 데이터 통합 구현
- [ ] JSON 파일 생성 확인
- [ ] validate.py로 검증 (선택)
- [ ] 웹 인터페이스 구현 (선택)
- [ ] CLI 도구 구현 (선택)

---

## 🚀 시작하기

1. **ANALYSIS_REPORT.md 읽기** (10분)
   ```bash
   더보기 ANALYSIS_REPORT.md
   ```

2. **analyze_docx.py 실행** (1분)
   ```bash
   python analyze_docx.py
   ```

3. **extract.py 작성 시작** (30분~2시간)
   - template.py를 참고하면서 구현

4. **테스트** (10분)
   ```bash
   python extract.py
   ```

행운을 빕니다! 💪

---

**마지막 수정**: 2026-06-02
**상태**: 준비 완료 🟢
