from docx import Document
import re

doc = Document('2025년도 설명.docx')

# 문제를 찾아서 그 이전의 내용을 확인
current_exam = None
element_list = list(doc.element.body)

for i, element in enumerate(element_list):
    if element.tag.endswith('p'):
        text = ''.join([t.text for t in element.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])
        
        if '2025년도' in text and '설명' in text:
            match = re.search(r'제(\d)회', text)
            if match:
                current_exam = int(match.group(1))
        
        if text and re.match(r'^\d+\.$', text.strip()):
            problem_num = int(text.strip()[:-1])
            
            if current_exam == 1 and problem_num == 43:
                print(f"제1회 43번 발견 (인덱스 {i})")
                # 43번부터 45번까지의 모든 요소를 출력
                for j in range(i, min(i+15, len(element_list))):
                    elem = element_list[j]
                    if elem.tag.endswith('p'):
                        elem_text = ''.join([t.text for t in elem.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])
                        print(f"  [{j}] 문단: {elem_text[:80]}")
                    elif elem.tag.endswith('tbl'):
                        from docx.table import Table
                        table = Table(elem, doc)
                        if len(table.rows) > 0:
                            cell_text = table.rows[0].cells[0].text.strip()[:80]
                            print(f"  [{j}] 표: {cell_text}")
