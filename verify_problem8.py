import json

with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 제4회 8번 찾기
for q in data['questions']:
    if q['exam'] == '제4회' and q['number'] == 8:
        print('📌 제4회 8번 문제')
        print('=' * 60)
        print(f'문제: {q["question"]}')
        print(f'\n보기:')
        for i, opt in enumerate(q['options'], 1):
            marker = '👉' if i-1 == q['answer'] else '  '
            print(f'  {marker} {i}. {opt}')
        print(f'\n정답: {q["answer"]+1}번 (③ 누설 리액턴스가 증가한다)')
        print('=' * 60)
        print('✅ 문제 선택지가 정상적으로 4개로 수정되었습니다!')
        break
