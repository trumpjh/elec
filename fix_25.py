"""
제1회 25번 보기 수정
"""
import json

data = json.load(open('questions.json', 'r', encoding='utf-8'))

# 정확한 보기들
options_25 = [
    "대지 전압은 300[V] 이하여야 한다.",
    "애자사용공사에 의한 경우",
    "케이블을 사용하여 지중에 시설할 것",
    "모든 접속은 전폐형으로 할 것"
]

# 제1회 25번 찾아서 수정
for q in data['questions']:
    if q['exam'] == '제1회' and q['number'] == 25:
        q['options'] = options_25
        print("【수정 완료】")
        print("-" * 50)
        print(f"문제: {q['question'][:50]}...")
        print(f"\n수정된 보기:")
        for i, opt in enumerate(options_25):
            print(f"  {i+1}번: {opt}")
        print(f"\n답: ②번 (인덱스 1)")
        break

# 저장
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✓ questions.json 저장 완료")
