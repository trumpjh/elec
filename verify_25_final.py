"""
제1회 25번 최종 검증
"""
import json

data = json.load(open('questions.json', 'r', encoding='utf-8'))

for q in data['questions']:
    if q['exam'] == '제1회' and q['number'] == 25:
        print("✅ 제1회 25번 최종 상태")
        print("=" * 60)
        print(f"문제: {q['question']}")
        print(f"\n보기 수: {len(q['options'])}")
        for i, opt in enumerate(q['options']):
            symbol = "①②③④"[i]
            print(f"  {symbol} {opt}")
        print(f"\n정답: {q['answer']+1}번")
        break
