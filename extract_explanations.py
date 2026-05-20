from docx import Document
import json
import re

doc = Document(r"C:\Users\Administrator\Documents\history\elec\2025년도 문제.docx")

# 문단에서 문제 추출
lines = [para.text.strip() for para in doc.paragraphs if para.text.strip()]

# 테이블에서 설명과 단원 추출
explanations = {}  # {문제번호: {"category": "단원명", "explanation": "설명"}}

for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            text = cell.text.strip()
            if text.startswith("설명:"):
                # "설명: 단원명-[단원명]\n- [설명]" 형식 파싱
                lines_text = text.split('\n')
                
                # 첫 번째 라인에서 단원명 추출
                first_line = lines_text[0]
                category = ""
                if "단원명-" in first_line:
                    category = first_line.split("단원명-")[1].strip()
                
                # 설명 추출 (- 로 시작하는 라인들)
                explanation_lines = []
                for line in lines_text[1:]:
                    if line.startswith("-"):
                        explanation_lines.append(line[1:].strip())
                    elif line.strip():
                        explanation_lines.append(line.strip())
                
                explanation = " ".join(explanation_lines)
                
                # 마지막 추출된 문제 번호와 매칭
                if explanations:
                    last_num = max(explanations.keys())
                    next_num = last_num + 1
                else:
                    next_num = 1
                
                explanations[next_num] = {
                    "category": category,
                    "explanation": explanation
                }
                print(f"문제 {next_num}: {category} - {explanation[:60]}...")

print("\n\n=== 추출된 설명 ===")
for num in sorted(explanations.keys()):
    print(f"{num}: {explanations[num]['category']} - {explanations[num]['explanation'][:60]}")
