import json
import re

# questions.json 로드
with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 단원 분류 매핑
category_mapping = {
    '전기설비': '전기설비',
    '전기기기': '전기기기',
    '전기공학': '전기이론',  # 변경
    '전기이론': '전기이론',
    '기타': '기타',
}

# 각 문제에서 설명의 첫 번째 단어를 단원으로 사용
for q in data['questions']:
    if 'explanation' in q and q['explanation']:
        # 설명의 첫 번째 줄 추출
        first_line = q['explanation'].split('\n')[0].strip()
        
        # 단원명 추출
        category = None
        for key in category_mapping.keys():
            if key in first_line:
                category = category_mapping[key]
                break
        
        if category is None:
            # 단원을 찾을 수 없으면 기타
            category = '기타'
        
        q['category'] = category
    else:
        q['category'] = '기타'

# 단원별 통계 출력
categories = {}
for q in data['questions']:
    cat = q.get('category', '기타')
    if cat not in categories:
        categories[cat] = 0
    categories[cat] += 1

print("="*60)
print("단원별 문제 수 (category 추가 후)")
print("="*60)
for cat in sorted(categories.keys()):
    print(f"  {cat}: {categories[cat]}개")

# 저장
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✓ questions.json 업데이트 완료")
