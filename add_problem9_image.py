"""
제4회 문제 9의 이미지 추가 (수동 수정)
"""

import json

print("\n제4회 문제 9 이미지 추가 중...\n")

with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 제4회 문제 9 찾기
found = False
for question in data['questions']:
    if question['exam'] == '제4회' and question['number'] == 9:
        question['image'] = 'images/problem_image_5.png'
        found = True
        print(f"✓ {question['exam']} 문제 {question['number']}: 이미지 추가됨")
        print(f"  문제: {question['question'][:60]}...")
        print(f"  이미지: {question['image']}")
        break

if not found:
    print("❌ 제4회 문제 9를 찾을 수 없습니다")

# 저장
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✓ questions.json 업데이트 완료")

# 모든 이미지 포함 문제 확인
print("\n【최종 이미지 포함 문제 목록】")
print("-" * 50)

problems_with_images = [q for q in data['questions'] if q.get('image')]
for q in problems_with_images:
    print(f"  {q['exam']} 문제 {q['number']}: {q['image']}")

print(f"\n총 {len(problems_with_images)}개")
