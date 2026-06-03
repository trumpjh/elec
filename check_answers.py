import json
from docx import Document
import re

# JSON 로드
with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# docx 로드
doc = Document('2025년도 문제.docx')
paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

def extract_all_docx_problems_with_answer():
    """docx에서 모든 문제의 정답 추출"""
    problems = {}
    current_exam = None
    
    for i, text in enumerate(paragraphs):
        # 회차 감지
        if '제' in text and '회' in text:
            match = re.search(r'제(\d+)회', text)
            if match:
                current_exam = f'제{match.group(1)}회'
            continue
        
        # 문제 찾기: "숫자. 문제텍스트 정답심볼"
        match = re.match(r'^(\d+)\.\s+(.+)$', text)
        if match and current_exam:
            problem_num = int(match.group(1))
            problem_text_with_answer = match.group(2)
            
            # 정답 심볼 추출
            answer_symbol = None
            answer_index = None
            for symbol, idx in {'①': 0, '②': 1, '③': 2, '④': 3}.items():
                if problem_text_with_answer.endswith(symbol):
                    answer_symbol = symbol
                    answer_index = idx
                    break
            
            problem_key = (current_exam, problem_num)
            problems[problem_key] = answer_index
    
    return problems

docx_answers = extract_all_docx_problems_with_answer()

print("="*80)
print("JSON과 DOCX 정답 비교")
print("="*80)

answer_mismatches = []

for q in data['questions']:
    key = (q['exam'], q['number'])
    
    if key in docx_answers:
        json_answer = q['answer']
        docx_answer = docx_answers[key]
        
        if json_answer != docx_answer:
            answer_mismatches.append({
                'exam': q['exam'],
                'number': q['number'],
                'question': q['question'],
                'json_answer': json_answer,
                'docx_answer': docx_answer,
                'options': q['options']
            })

if answer_mismatches:
    print(f"\n⚠️  발견된 정답 불일치: {len(answer_mismatches)}개\n")
    
    for i, mismatch in enumerate(answer_mismatches, 1):
        json_ans = chr(9312 + mismatch['json_answer'])
        docx_ans = chr(9312 + mismatch['docx_answer']) if mismatch['docx_answer'] is not None else '?'
        
        print(f"{i}. {mismatch['exam']} 문제 {mismatch['number']}")
        print(f"   문제: {mismatch['question'][:60]}...")
        print(f"   JSON 정답: {json_ans} (인덱스: {mismatch['json_answer']})")
        print(f"   DOCX 정답: {docx_ans} (인덱스: {mismatch['docx_answer']})")
        print()
else:
    print("\n✅ 모든 정답이 일치합니다!")

# 종합 정리
print("\n" + "="*80)
print("종합 진단")
print("="*80)

with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 선택지가 4개가 아닌 문제
incomplete_options = [q for q in data['questions'] if len(q['options']) != 4]
# 정답이 없는 문제
no_answer = [q for q in data['questions'] if q['answer'] is None or q['answer'] < 0]

print(f"\n📊 상태:")
print(f"  - 총 문제: {len(data['questions'])}개")
print(f"  - 선택지가 4개가 아닌 문제: {len(incomplete_options)}개")
print(f"  - 정답 불일치: {len(answer_mismatches)}개")
print(f"  - 정답 없는 문제: {len(no_answer)}개")

if incomplete_options:
    print(f"\n❌ 선택지 이상 문제 ({len(incomplete_options)}개):")
    for q in incomplete_options:
        print(f"  - {q['exam']} 문제 {q['number']}: {len(q['options'])}개 선택지")

if len(answer_mismatches) == 0 and len(incomplete_options) == 0:
    print("\n✅ 모든 문제의 선택지와 정답이 일치합니다!")
