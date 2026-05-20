from docx import Document
import re

doc = Document(r"C:\Users\Administrator\Documents\history\elec\2025년도 문제.docx")

print("=== 문서 구조 분석 ===\n")
for i, para in enumerate(doc.paragraphs[:100]):
    text = para.text.strip()
    if text:
        # 길이 100자 이상이면 앞 100자만 표시
        display_text = text[:120] if len(text) > 120 else text
        print(f"{i:3d}: {display_text}")
