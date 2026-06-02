import json

with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 80)
print("✅ 수정 완료 - 제4회 10번, 14번, 19번 최종 확인")
print("=" * 80)

problem_nums = [10, 14, 19]

for num in problem_nums:
    for q in data['questions']:
        if q['exam'] == '제4회' and q['number'] == num:
            print(f"\n【제4회 {num}번】")
            print(f"문제: {q['question']}")
            print(f"보기:")
            for i, opt in enumerate(q['options'], 1):
                marker = '→' if i-1 == q['answer'] else ' '
                print(f"  {marker} {i}. {opt}")
            print(f"정답: {q['answer']+1}번")
            break

print("\n" + "=" * 80)
print("모든 문제 수정이 완료되었습니다!")
print("=" * 80)
