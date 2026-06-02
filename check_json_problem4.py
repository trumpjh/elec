"""
JSON의 제1회 문제 4 확인
"""
import json

data = json.load(open('questions.json', 'r', encoding='utf-8'))

for q in data['questions']:
    if q['exam'] == '제1회' and q['number'] == 4:
        print("【JSON의 제1회 문제 4】")
        print("-" * 70)
        print(f"문제: {q['question']}")
        print(f"옵션 수: {len(q['options'])}")
        for i, opt in enumerate(q['options']):
            print(f"  {i}: '{opt}'")
        print(f"답: {q['answer']} (선택지 {q['answer']})")
        break
