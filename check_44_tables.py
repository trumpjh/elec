from docx import Document
import re

doc = Document('2025년도 설명.docx')

current_exam = None
last_problem_num = None
problem_found = False
table_count = 0

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
                problem_found = True
                table_count = 0
    
    elif element.tag.endswith('tbl') and problem_found:
        from docx.table import Table
        table = Table(element, doc)
        table_count += 1
        
        if len(table.rows) > 0:
            # 모든 행과 셀의 내용 확인
            print(f"\n표 #{table_count}:")
            for row_idx, row in enumerate(table.rows):
                for cell_idx, cell in enumerate(row.cells):
                    text = cell.text.strip()
                    if text:
                        print(f"  행{row_idx} 셀{cell_idx}: {text[:100]}")
        
        if table_count >= 3:  # 3개 표 확인
            break
