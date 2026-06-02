from docx import Document
import json

doc = Document('2025년도 설명.docx')

# 제1회 44번 찾기
in_44 = False
explanation_lines = []

for para in doc.paragraphs:
    text = para.text.strip()
    if '44' in text and '제1회' in text:
        in_44 = True
        explanation_lines = []
    elif in_44:
        if text and len(text) > 0:
            # 다음 문제 시작 감지
            if any(char.isdigit() for char in text[:3]) and '번' in text[:5]:
                break
            explanation_lines.append(text)

print("=== 제1회 44번 설명 ===")
print('\n'.join(explanation_lines[:30]))

# 전체 설명 내용
full_explanation = '\n'.join(explanation_lines)
print(f"\n\n전체 내용:\n{full_explanation}")
