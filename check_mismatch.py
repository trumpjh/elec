from docx import Document
import json

doc = Document('2025년도 문제.docx')

# 1. 현재 questions.json의 모든 문제 수집
with open('questions.json', 'r', encoding='utf-8') as f:
    questions_data = json.load(f)

questions_by_num = {}
for q in questions_data['questions']:
    questions_by_num[q['number']] = q

# 2. 설명 매칭: 테이블에서 추출
explanation_map = {}

# 테이블에서 설명 추출
table_idx = 0
paragraph_idx = 0

for table in doc.tables:
    for row in table.rows:
        if len(row.cells) > 0:
            cell_text = row.cells[0].text.strip()
            
            # "설명:" 으로 시작하는 테이블 행
            if cell_text.startswith('설명:'):
                parts = cell_text.split('설명:', 1)
                if len(parts) == 2:
                    explanation_full = parts[1].strip()
                    
                    # 단원명 추출
                    if '단원명-' in explanation_full:
                        cat_part, exp_part = explanation_full.split('단원명-', 1)
                        
                        category = None
                        explanation = None
                        
                        for cat in ['전기설비', '전기기기', '전기이론']:
                            if cat in exp_part:
                                category = cat
                                explanation = exp_part.replace(cat, '', 1).strip()
                                break
                        
                        if category and explanation:
                            # 이 설명이 어느 문제에 속하는지 찾아야 함
                            # 순서대로 저장
                            current_problem_num = len(explanation_map) + 1
                            if current_problem_num in questions_by_num:
                                explanation_map[current_problem_num] = {
                                    'category': category,
                                    'explanation': explanation
                                }

print("추출된 설명 매핑:")
print(f"총 {len(explanation_map)}개")

# 3. questions.json 의 순서와 example.json의 순서가 맞는지 확인
with open('example.json', 'r', encoding='utf-8') as f:
    examples_data = json.load(f)

print("\n" + "=" * 80)
print("현재 example.json의 문제 번호:")
current_problem_nums = sorted([e['problem_number'] for e in examples_data['examples']])
print(f"{current_problem_nums[:20]}...")
print(f"Total: {len(current_problem_nums)}")

print("\n" + "=" * 80)
print("questions.json 의 문제 번호:")
q_nums = sorted([q['number'] for q in questions_data['questions']])
print(f"{q_nums[:20]}...")
print(f"Total: {len(q_nums)}")

print("\n" + "=" * 80)
print("불일치:")
only_in_examples = set(current_problem_nums) - set(q_nums)
only_in_questions = set(q_nums) - set(current_problem_nums)

if only_in_examples:
    print(f"example.json에만 있는 번호: {sorted(only_in_examples)}")
if only_in_questions:
    print(f"questions.json에만 있는 번호: {sorted(only_in_questions)}")
