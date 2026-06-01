from docx import Document
import json

doc = Document('2025년도 문제.docx')

# 각 회차별 설명 수집
missing_explanations = {}

# 문제: 제1회 39, 60, 제4회 8
targets = {
    '제1회': [39, 60],
    '제4회': [8]
}

current_exam = None
current_problem_num = None
collecting = False
collected_text = []

for para in doc.paragraphs:
    text = para.text.strip()
    
    # 회차 감지
    if '제1회' in text:
        current_exam = '제1회'
        continue
    elif '제2회' in text:
        current_exam = '제2회'
        continue
    elif '제3회' in text:
        current_exam = '제3회'
        continue
    elif '제4회' in text:
        current_exam = '제4회'
        continue
    
    if not text or not current_exam:
        continue
    
    # 문제 번호 감지 (예: "39.", "60.", "8.")
    if text and text[0].isdigit():
        try:
            num = int(text.split('.')[0])
            if current_exam in targets and num in targets[current_exam]:
                current_problem_num = num
                collecting = True
                collected_text = [text]
            else:
                collecting = False
        except:
            if collecting:
                collected_text.append(text)
    else:
        # 답 섹션 시작 감지
        if '①' in text or '②' in text or '③' in text or '④' in text:
            if collecting and current_problem_num and current_exam:
                full_text = ' '.join(collected_text)
                key = f"{current_exam}-{current_problem_num}"
                missing_explanations[key] = full_text
                collecting = False
        elif collecting and text:
            collected_text.append(text)

print("=" * 80)
print("누락된 설명 추출 결과")
print("=" * 80)
for key, explanation in sorted(missing_explanations.items()):
    print(f"\n{key}:")
    print(f"  {explanation[:200]}...")
