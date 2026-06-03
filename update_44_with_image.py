import json

# JSON 로드
with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 제1회 44번 찾아서 수정
for q in data['questions']:
    if q['exam'] == '제1회' and q['number'] == 44:
        # 설명을 이미지로 변경
        q['explanation'] = '설명: 단원명-전기설비\n교류 송전 방식의 장점 및 단점'
        q['explanation_image'] = 'images/2025년도 설명 제1회 44번.png'
        print(f"업데이트됨: 제1회 44번")
        print(f"  설명: {q['explanation']}")
        print(f"  이미지: {q['explanation_image']}")

# 저장
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✓ JSON 저장 완료")
