import json

# questions.json 열기
with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 제4회 8번 찾아서 수정
for q in data['questions']:
    if q['exam'] == '제4회' and q['number'] == 8:
        print(f"수정 전:")
        print(f"  문제: {q['question']}")
        print(f"  선택지: {q['options']}")
        print(f"  정답: {q['answer']}")
        
        # 올바른 선택지로 업데이트
        q['options'] = [
            "동기 속도가 감소한다.",
            "철손이 증가한다.",
            "누설 리액턴스가 증가한다.",
            "효율이 나빠진다."
        ]
        # 정답 인덱스: 2 (선택지 3번, 누설 리액턴스가 증가한다가 옳지 않음)
        q['answer'] = 2
        
        print(f"\n수정 후:")
        print(f"  문제: {q['question']}")
        print(f"  선택지: {q['options']}")
        print(f"  정답: {q['answer']+1}번 (③ 누설 리액턴스가 증가한다)")
        break

# 파일에 저장
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✅ questions.json 수정 완료!")
