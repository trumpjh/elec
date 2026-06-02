"""
문단 249의 전체 내용 확인
"""
from docx import Document

doc = Document('2025년도 문제.docx')

para = doc.paragraphs[249]

print("\n【문단 249 상세 정보】")
print("-" * 70)
print(f"텍스트 길이: {len(para.text)}")
print(f"전체 텍스트:\n{para.text}")

# 다시 추출된 문제들과 비교
import json

with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 문제 9가 다른 회차에 있는지 확인
for q in data['questions']:
    if q['number'] == 9:
        print(f"\n문제 9 발견: {q['exam']}")
        print(f"  {q['question'][:60]}...")
