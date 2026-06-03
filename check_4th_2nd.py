from docx import Document
import re

doc = Document('2025년도 설명.docx')

current_exam = None
last_problem_num = None
element_list = list(doc.element.body)

# 제4회부터의 모든 문제 확인
for i, element in enumerate(element_list):
    if element.tag.endswith('p'):
        text = ''.join([t.text for t in element.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])
        
        if '2025년도' in text and '설명' in text:
            match = re.search(r'제(\d)회', text)
            if match:
                current_exam = int(match.group(1))
        
        if text and re.match(r'^\d+\.$', text.strip()):
            problem_num = int(text.strip()[:-1])
            last_problem_num = problem_num
            
            if current_exam == 4 and problem_num >= 1 and problem_num <= 10:
                print(f"제4회 {problem_num}번 (인덱스 {i})")
    
    elif element.tag.endswith('tbl'):
        from docx.table import Table
        table = Table(element, doc)
        
        if current_exam == 4 and last_problem_num and last_problem_num >= 1 and last_problem_num <= 10:
            if len(table.rows) > 0:
                explanation_text = table.rows[0].cells[0].text.strip()
                print(f"  설명: {explanation_text[:100]}")
