from docx import Document

doc = Document('2025년도 문제.docx')

print("=" * 80)
print("DOCX 파일의 모든 테이블 내용 상세 분석")
print("=" * 80)

for table_idx, table in enumerate(doc.tables):
    print(f"\n【테이블 {table_idx}】")
    print(f"행 개수: {len(table.rows)}, 열 개수: {len(table.columns)}")
    
    # 테이블을 HTML로 변환
    html_table = "<table border='1' cellpadding='10' cellspacing='0'>\n"
    
    for row_idx, row in enumerate(table.rows):
        html_table += "  <tr>\n"
        for col_idx, cell in enumerate(row.cells):
            cell_text = cell.text.strip()
            # 셀 내용에서 줄바꿈을 <br>로 변환
            cell_text = cell_text.replace('\n', '<br>')
            html_table += f"    <td>{cell_text}</td>\n"
        html_table += "  </tr>\n"
    
    html_table += "</table>"
    
    print("\nHTML 테이블:")
    print(html_table)
    
    # 텍스트 내용도 출력
    print("\n텍스트 내용:")
    for row_idx, row in enumerate(table.rows):
        for col_idx, cell in enumerate(row.cells):
            cell_text = cell.text.strip()
            if cell_text:
                print(f"  [{row_idx},{col_idx}]: {cell_text[:100]}")
