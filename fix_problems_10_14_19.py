import json

# questions.json 열기
with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 문제 번호별 수정 내용
corrections = {
    10: {
        "options": [
            "다른 방식에 비해 장치가 간단하다.",
            "고장 구간의 고속도 동시 차단이 가능하다.",
            "고장 구간의 선택이 확실하다.",
            "동작을 예민하게 할 수 있다."
        ],
        "answer": 0  # ① (틀린 것: "장치가 간단하다"가 이점이 아님)
    },
    14: {
        "options": [
            "단락시킨다.",
            "개방시킨다.",
            "직류를 공급한다.",
            "단상교류를 공급한다."
        ],
        "answer": 0  # ① 단락시킨다
    },
    19: {
        "options": [
            "배전용 변압기의 1차 측에 시설하여 변압기의 단락 보호용으로 쓰인다.",
            "배전용 변압기의 2차 측에 시설하여 변압기의 단락 보호용으로 쓰인다.",
            "배전용 변압기의 1차 측에 시설하여 배전 구역 전환용으로 쓰인다.",
            "배전용 변압기의 2차 측에 시설하여 배전 구역 전환용으로 쓰인다."
        ],
        "answer": 0  # ① 1차 측 단락 보호용
    }
}

# 수정 적용
for q in data['questions']:
    if q['exam'] == '제4회' and q['number'] in corrections:
        num = q['number']
        
        print(f"\n수정 전 - 제4회 {num}번:")
        print(f"  선택지: {q['options']}")
        print(f"  정답: {q['answer']+1}번")
        
        q['options'] = corrections[num]['options']
        q['answer'] = corrections[num]['answer']
        
        print(f"\n수정 후 - 제4회 {num}번:")
        print(f"  선택지: {len(q['options'])}개")
        for i, opt in enumerate(q['options'], 1):
            marker = '→' if i-1 == q['answer'] else ' '
            print(f"    {marker} {i}. {opt[:40]}...")
        print(f"  정답: {q['answer']+1}번")

# 파일에 저장
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 70)
print("✅ 제4회 10번, 14번, 19번 수정 완료!")
print("=" * 70)
