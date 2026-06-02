"""
제1회 25번 문제 상세 확인
"""
import json

data = json.load(open('questions.json', 'r', encoding='utf-8'))

for q in data['questions']:
    if q['exam'] == '제1회' and q['number'] == 25:
        print("【제1회 25번】")
        print("-" * 70)
        print(f"문제: {q['question']}")
        print(f"\n옵션 수: {len(q['options'])}")
        for i, opt in enumerate(q['options']):
            print(f"  {i+1}번: {opt}")
        print(f"\n답: {q['answer']} (선택지 {q['answer']+1})")
        print(f"설명: {q['explanation'][:80]}...")
        break
