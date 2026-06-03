import json
from docx import Document
import re

# docx 로드
doc = Document('2025년도 문제.docx')

print("="*80)
print("제1회 문제 60 상세 분석")
print("="*80)

# paragraphs 추출
paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

# 제1회 문제 60 찾기
in_exam1 = False
found = False

for i, text in enumerate(paragraphs):
    if '제1회' in text and '회' in text:
        in_exam1 = True
        continue
    
    if in_exam1 and text.startswith('60.'):
        found = True
        print(f"\n발견! (인덱스 {i})")
        print(f"\n문제 문단 [i]:")
        print(f"  {text[:80]}...")
        
        print(f"\n다음 10개 문단:")
        for j in range(1, 11):
            if i + j < len(paragraphs):
                next_text = paragraphs[i + j]
                print(f"  [{i+j}] {next_text[:80]}")
        
        break

# JSON에서도 확인
print("\n" + "="*80)
print("JSON의 현재 데이터")
print("="*80)

with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data['questions']:
    if q['exam'] == '제1회' and q['number'] == 60:
        print(f"\n문제: {q['question']}")
        print(f"\n선택지 ({len(q['options'])}개):")
        for i, opt in enumerate(q['options'], 1):
            symbol = chr(9312 + i - 1)
            print(f"  {symbol}. {opt}")
        print(f"\n정답: {chr(9312 + q['answer'])}")
        break
