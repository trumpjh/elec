import json

# questions.json 열기
with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 수정할 문제들
corrections = {
    ('제1회', 60): {
        'question': '다음 보기 중 금속관, 애자, 합성수지관 및 케이블 공사가 모두 가능한 특수 장소를 옳게 나열한 것은?\n\n㉠ 화약고 등의 위험 장소\n㉡ 부식성 가스가 있는 장소\n㉢ 위험물 등이 존재하는 장소\n㉣ 불연성 먼지가 많은 장소\n㉤ 습기가 많은 장소'
    },
    ('제3회', 55): {
        'question': '자기저항은 자기 회로의 길이에 (  ⓐ  )하고 자로의 단면적과 투자율의 곱에 (   ⓑ   )한다.\n\n위 빈칸 ⓐ, ⓑ에 들어갈 내용으로 알맞은 것은?'
    },
    ('제3회', 58): {
        'question': '"2차 전지의 대표적인 것으로 납축전지가 있다. 전해액으로 비중 약(  ㉠  ) 정도의 (  ㉡  )을 사용한다."\n\n위 빈칸 ㉠, ㉡에 들어갈 내용으로 알맞은 것은?'
    }
}

# 수정 적용
for q in data['questions']:
    key = (q['exam'], q['number'])
    if key in corrections:
        exam, num = key
        print(f"\n수정: {exam} {num}번")
        print(f"  이전 문제: {q['question'][:50]}...")
        
        q['question'] = corrections[key]['question']
        
        print(f"  수정 후: {q['question'][:50]}...")

# 파일에 저장
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*70}")
print(f"✅ 3개 문제의 완전한 문제 내용으로 수정 완료!")
print(f"{'='*70}")
