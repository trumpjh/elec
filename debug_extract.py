from docx import Document
import json
import re

doc = Document(r'2025년도 문제.docx')

# 문제 추출
questions_list = []
lines = [para.text.strip() for para in doc.paragraphs if para.text.strip()]

# 전체 라인 보기
print("=== 모든 라인 ===")
for i, line in enumerate(lines):
    print(f"{i:2d}: {line}")
