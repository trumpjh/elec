"""
설명에서 단원 정보를 추출하여 문제에 추가
전기기기, 전기설비, 전기이론으로 분류
"""

import json
import re

# questions.json 로드
with open('questions.json', 'r', encoding='utf-8') as f:
    questions_data = json.load(f)

# 단원별로 나누기
category_keywords = {
    '전기기기': ['전기기기', '유도전동기', '발전기', '변압기', '다이오드', '계전기', '동기'],
    '전기설비': ['전기설비', '가공', '금속관', '접지', '배전', '전선', '애자', '배선'],
    '전기이론': ['전기이론', '전기', '자기저항', '직류', '교류', '임피던스', '공진', 'RLC']
}

def extract_category(explanation):
    """설명에서 단원 추출"""
    if not explanation:
        return '기타'
    
    # 맨 앞의 단원명 추출 (개행 전까지)
    first_line = explanation.split('\n')[0].strip()
    
    # 알려진 단원명 확인
    if first_line in ['전기기기', '전기설비', '전기이론']:
        return first_line
    
    # 키워드로 매칭
    explanation_lower = explanation.lower()
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in explanation:
                return category
    
    return '기타'

# 각 문제에 단원 추가
print("📚 단원 분류 중...")
category_count = {'전기기기': 0, '전기설비': 0, '전기이론': 0, '기타': 0}

for question in questions_data['questions']:
    explanation = question.get('explanation', '')
    category = extract_category(explanation)
    question['category'] = category
    category_count[category] += 1

# 결과 출력
print("\n📊 단원별 분류 결과:")
for category, count in category_count.items():
    print(f"  {category}: {count}개")

# 저장
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions_data, f, ensure_ascii=False, indent=2)

print("\n✓ questions.json 업데이트 완료!")

# 샘플 확인
print("\n📋 샘플 문제:")
for i in range(3):
    q = questions_data['questions'][i]
    print(f"\n문제 {q['number']} ({q['exam']}) - 단원: {q['category']}")
    print(f"  설명: {q['explanation'][:50]}...")
