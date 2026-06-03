import json
from docx import Document

# 1. JSON에서 제2회 2번 확인
print("="*60)
print("JSON 데이터 확인")
print("="*60)

with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data['questions']:
    if q['exam'] == '제2회' and q['number'] == 2:
        print(f"\n문제 번호: {q['number']}")
        print(f"문제: {q['question']}")
        print(f"선택지:")
        for i, opt in enumerate(q['options'], 1):
            print(f"  {i}. {opt}")
        print(f"정답: {chr(9312 + q['answer'])}")
        json_options = q['options']
        json_answer = q['answer']
        break

# 2. docx 파일에서 직접 확인
print("\n" + "="*60)
print("DOCX 파일 원본 데이터")
print("="*60)

doc = Document('2025년도 문제.docx')
paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

# 제2회 찾기
in_exam2 = False
problem_2_idx = None

for i, text in enumerate(paragraphs):
    if '제2회' in text and '회' in text:
        in_exam2 = True
        print(f"\n제2회 시작 발견")
        continue
    
    if in_exam2 and text.startswith('2.'):
        problem_2_idx = i
        print(f"\n문제 발견 (인덱스 {i}):")
        print(f"문제: {text}")
        
        # 다음 줄이 선택지
        if i + 1 < len(paragraphs):
            options_text = paragraphs[i + 1]
            print(f"선택지 문단: {options_text}")
            
            # 선택지 파싱
            import re
            option_pattern = r'[①②③④]\s*([^①②③④]+?)(?=[①②③④]|$)'
            options = re.findall(option_pattern, options_text)
            options = [opt.strip() for opt in options if opt.strip()]
            
            print(f"\n파싱된 선택지 ({len(options)}개):")
            for j, opt in enumerate(options, 1):
                print(f"  {j}. {opt}")
        break

print("\n" + "="*60)
print("비교 결과")
print("="*60)
print(f"\nJSON 선택지 ({len(json_options)}개): {json_options}")
print(f"DOCX 선택지: {options}")
print(f"\n일치 여부: {'✓ 같음' if json_options == options else '✗ 다름'}")
