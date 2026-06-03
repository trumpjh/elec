from docx import Document
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import json
import re

doc = Document('2025년도 설명.docx')

# 핵심: python-docx에서 문단과 테이블의 순서를 파악하려면
# document의 body element를 직접 순회해야 함

explanations_by_problem = {}  # (exam, number) -> explanation

current_exam = None
last_problem_num = None
last_problem_exam = None

# body의 모든 요소(문단과 테이블)를 순회
for element in doc.element.body:
    # 문단인지 테이블인지 확인
    if element.tag.endswith('p'):  # 문단
        # 문단의 텍스트 추출
        text = ''.join([t.text for t in element.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])
        
        # 회차 헤더 감지
        if '2025년도' in text and '설명' in text:
            match = re.search(r'제(\d)회', text)
            if match:
                current_exam = int(match.group(1))
                print(f"[헤더] 제{current_exam}회 설명 시작")
        
        # 문제 번호 감지
        if text and re.match(r'^\d+\.$', text.strip()) and current_exam:
            problem_num = int(text.strip()[:-1])
            last_problem_num = problem_num
            last_problem_exam = current_exam
            print(f"[문제] 제{current_exam}회 {problem_num}번 발견")
    
    elif element.tag.endswith('tbl'):  # 테이블
        # 테이블의 첫 셀에서 텍스트 추출
        from docx.table import Table
        table = Table(element, doc)
        
        if len(table.rows) > 0 and len(table.rows[0].cells) > 0:
            explanation_text = table.rows[0].cells[0].text.strip()
            
            if last_problem_exam and last_problem_num:
                key = (last_problem_exam, last_problem_num)
                explanations_by_problem[key] = explanation_text
                print(f"  -> 제{last_problem_exam}회 {last_problem_num}번 설명: {explanation_text[:60]}...")
                
                # 다음 문제를 위해 리셋
                last_problem_num = None
                last_problem_exam = None

print(f"\n\n총 추출된 설명: {len(explanations_by_problem)}개")

# JSON에 업데이트
with open('questions.json', 'r', encoding='utf-8') as f:
    questions_data = json.load(f)

updated = 0
not_found = []

for q in questions_data['questions']:
    exam = int(q['exam'].replace('제', '').replace('회', ''))
    num = q['number']
    
    key = (exam, num)
    if key in explanations_by_problem:
        q['explanation'] = explanations_by_problem[key]
        updated += 1
    else:
        not_found.append(f"제{exam}회 {num}번")

print(f"\n업데이트됨: {updated}개")
if not_found:
    print(f"설명을 찾을 수 없는 문제: {len(not_found)}개")
    for p in not_found[:10]:
        print(f"  - {p}")

# 저장
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions_data, f, ensure_ascii=False, indent=2)

print("\n✓ JSON 저장 완료")
