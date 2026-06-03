from docx import Document
import re

doc = Document('2025년도 설명.docx')

current_exam = None
last_problem_num = None

for element in doc.element.body:
    if element.tag.endswith('p'):
        text = ''.join([t.text for t in element.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])
        
        if '2025년도' in text and '설명' in text:
            match = re.search(r'제(\d)회', text)
            if match:
                current_exam = int(match.group(1))
        
        if text and re.match(r'^\d+\.$', text.strip()):
            problem_num = int(text.strip()[:-1])
            last_problem_num = problem_num
            
            if current_exam == 1 and problem_num == 44:
                print(f"찾음: 제1회 44번")
    
    elif element.tag.endswith('tbl'):
        from docx.table import Table
        table = Table(element, doc)
        
        if last_problem_num == 44 and current_exam == 1:
            if len(table.rows) > 0 and len(table.rows[0].cells) > 0:
                explanation_text = table.rows[0].cells[0].text.strip()
                print(f"\n제1회 44번의 docx 원본 설명:")
                print(explanation_text)
                break
