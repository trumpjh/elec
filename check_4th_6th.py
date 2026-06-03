from docx import Document
import re

doc = Document('2025년도 설명.docx')

current_exam = None
last_problem_num = None

# 제4회 6번 찾기
for element in doc.element.body:
    if element.tag.endswith('p'):
        text = ''.join([t.text for t in element.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])
        
        if '2025년도' in text and '설명' in text and '제4회' in text:
            current_exam = 4
            print(f"[찾음] 제4회 설명 섹션 시작")
        
        if current_exam == 4 and text and re.match(r'^6\.$', text.strip()):
            print(f"✓ 제4회 6번 발견")
            last_problem_num = 6
    
    elif element.tag.endswith('tbl') and last_problem_num == 6 and current_exam == 4:
        from docx.table import Table
        table = Table(element, doc)
        
        if len(table.rows) > 0:
            explanation_text = table.rows[0].cells[0].text.strip()
            print(f"\n제4회 6번 설명:")
            print(explanation_text)
        break
