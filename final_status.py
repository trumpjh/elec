"""
모든 이미지 포함 문제 최종 확인
"""
import json

data = json.load(open('questions.json', 'r', encoding='utf-8'))

print("\n" + "="*70)
print("✅ 최종 이미지 통합 현황")
print("="*70)

# 이미지 있는 문제 확인
image_problems = [q for q in data['questions'] if q.get('image')]

print(f"\n【이미지 포함 문제】")
print("-" * 70)

for q in sorted(image_problems, key=lambda x: (x['exam'], x['number'])):
    print(f"\n{q['exam']} 문제 {q['number']}")
    print(f"  문제: {q['question'][:60]}...")
    print(f"  이미지: {q['image']}")
    print(f"  카테고리: {q['category']}")
    print(f"  설명: {q['explanation'][:50]}...")

print(f"\n\n【통계】")
print("-" * 70)
print(f"총 문제: {data['total']}개")
print(f"이미지 포함: {len(image_problems)}개")
print(f"이미지 없음: {data['total'] - len(image_problems)}개")

print("\n" + "="*70)
print("✅ 이미지 통합 완료!")
print("="*70)
