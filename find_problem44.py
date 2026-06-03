from docx import Document
import re

doc = Document('2025년도 설명.docx')

# 제1회 44번의 올바른 설명 찾기
current_exam = None
found_problem = False
last_problem_num = None

for i, element in enumerate(doc.element.body):
    if element.tag.endswith('p'):
        # paragraph 객체로 변환
        from docx.oxml import parse_xml
        from docx.text.paragraph import CT_P
        p = doc.paragraphs[doc.element.body.index(element)]
        text = p.text.strip()
        
        # 헤더에서 회차 추출
        if '제' in text and '회' in text and ('설명' in text or '문제' in text):
            match = re.search(r'제(\d)회', text)
            if match:
                current_exam = f"제{match.group(1)}회"
                print(f"[헤더] {text}")
        
        # 문제 번호 감지
        if text and text[0].isdigit():
            match = re.match(r'^(\d+)\.$', text.split('\n')[0])
            if match:
                problem_num = int(match.group(1))
                last_problem_num = problem_num
                if current_exam == '제1회' and problem_num == 44:
                    print(f"\n✓ 찾음: {current_exam} {problem_num}번")
                    found_problem = True
    
    elif element.tag.endswith('tbl') and found_problem:
        # 테이블에서 설명 추출
        table = element
        if len(table.rows) > 0:
            explanation_text = table.rows[0].cells[0].text
            print(f"설명 내용:\n{explanation_text}\n")
            found_problem = False
            break
