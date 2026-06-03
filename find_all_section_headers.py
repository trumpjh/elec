from docx import Document
import re

doc = Document('2025년도 설명.docx')

# 모든 문단에서 회차 관련 텍스트 찾기
print("문서의 모든 회차 관련 항목들:")
for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    if '회' in text and len(text) < 100:  # 짧은 텍스트만 - 헤더일 가능성
        print(f"[{i}] {text}")
