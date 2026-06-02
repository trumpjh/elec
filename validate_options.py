"""
questions.json의 옵션 검증
"""
import json

data = json.load(open('questions.json', 'r', encoding='utf-8'))

print("【문제별 옵션 검증】")
print("-" * 70)

problems_with_empty_options = []

for q in data['questions']:
    # 옵션 수 확인
    if len(q['options']) != 4:
        problems_with_empty_options.append(q)
    
    # 빈 옵션 확인
    for i, opt in enumerate(q['options']):
        if not opt or len(opt.strip()) == 0:
            problems_with_empty_options.append(q)
            break

if problems_with_empty_options:
    print(f"⚠️  문제 있는 문제: {len(problems_with_empty_options)}개\n")
    for q in problems_with_empty_options[:5]:  # 처음 5개만 표시
        print(f"{q['exam']} 문제 {q['number']}:")
        print(f"  옵션 수: {len(q['options'])}")
        for i, opt in enumerate(q['options']):
            print(f"    {i}: '{opt}'")
        print()
else:
    print("✓ 모든 문제의 옵션이 정상입니다")

# 이미지 경로 확인
print("\n【이미지 경로 확인】")
print("-" * 70)

for q in data['questions']:
    if q.get('image'):
        print(f"✓ {q['exam']} 문제 {q['number']}: {q['image']}")
