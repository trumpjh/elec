from docx import Document
import re

doc = Document('2025년도 설명.docx')

current_exam = None
last_problem_num = None

# 제4회를 찾기
found_4th = False

for element in doc.element.body:
    if element.tag.endswith('p'):
        text = ''.join([t.text for t in element.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])
        
        if '2025년도' in text and '설명' in text and '제4회' in text:
            current_exam = 4
            found_4th = True
            print(f"✓ 제4회 설명 시작")
        
        if found_4th and text and re.match(r'^\d+\.$', text.strip()):
            problem_num = int(text.strip()[:-1])
            last_problem_num = problem_num
            print(f"\n제4회 {problem_num}번")
    
    elif element.tag.endswith('tbl') and found_4th and last_problem_num:
        from docx.table import Table
        table = Table(element, doc)
        
        if len(table.rows) > 0:
            explanation_text = table.rows[0].cells[0].text.strip()
            print(f"  {explanation_text[:120]}")
        
        if last_problem_num >= 10:  # 처음 10개만 확인
            break
