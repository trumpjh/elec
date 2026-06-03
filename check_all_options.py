import json
from docx import Document
import re

# 1단계: JSON에서 선택지가 4개가 아닌 문제 찾기
print("="*70)
print("1단계: 선택지가 4개가 아닌 문제 찾기")
print("="*70)

with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

problems_with_wrong_options = []

for q in data['questions']:
    if len(q['options']) != 4:
        problems_with_wrong_options.append(q)
        print(f"\n❌ {q['exam']} 문제 {q['number']}: 선택지 {len(q['options'])}개")
        for i, opt in enumerate(q['options'], 1):
            print(f"   {i}. {opt[:50]}...")

print(f"\n총 {len(problems_with_wrong_options)}개 문제 발견")

# 2단계: docx 파일에서 각 문제의 실제 선택지 추출
print("\n" + "="*70)
print("2단계: 각 문제의 실제 선택지 docx에서 추출")
print("="*70)

doc = Document('2025년도 문제.docx')
paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

def get_options_from_docx(problem_num, exam_num):
    """docx에서 특정 문제의 선택지 추출"""
    exam_str = f'제{exam_num}회'
    
    # 해당 회차 찾기
    in_target_exam = False
    for i, text in enumerate(paragraphs):
        if exam_str in text and '회' in text:
            in_target_exam = True
            start_idx = i
            continue
        
        if in_target_exam and ('제' in text and '회' in text and exam_str not in text):
            # 다음 회차 시작
            break
        
        # 해당 문제 찾기
        if in_target_exam and text.startswith(f'{problem_num}.'):
            # 다음 4개 문단에서 선택지 수집
            options = {}
            for offset in range(1, 5):
                if i + offset < len(paragraphs):
                    para = paragraphs[i + offset]
                    for symbol, idx in {'①': 0, '②': 1, '③': 2, '④': 3}.items():
                        if para.startswith(symbol):
                            option_text = para[1:].strip()
                            options[idx] = option_text
            
            if len(options) == 4:
                return [options[j] for j in range(4)]
            else:
                # 한 줄에 모든 선택지가 있는 경우
                if i + 1 < len(paragraphs):
                    next_para = paragraphs[i + 1]
                    option_pattern = r'[①②③④]\s*([^①②③④]+?)(?=[①②③④]|$)'
                    matches = re.findall(option_pattern, next_para)
                    options_list = [m.strip() for m in matches if m.strip()]
                    if len(options_list) == 4:
                        return options_list
            
            return None
    
    return None

# 3단계: 불일치 항목 비교
print("\n불일치 상세 검토:\n")

for prob in problems_with_wrong_options:
    exam_num = int(prob['exam'].replace('제', '').replace('회', ''))
    docx_options = get_options_from_docx(prob['number'], exam_num)
    
    print(f"\n{'='*70}")
    print(f"{prob['exam']} 문제 {prob['number']}")
    print(f"{'='*70}")
    print(f"문제: {prob['question'][:60]}...")
    print(f"\nJSON 선택지 ({len(prob['options'])}개):")
    for i, opt in enumerate(prob['options'], 1):
        print(f"  {i}. {opt}")
    
    if docx_options:
        print(f"\nDOCX 선택지 ({len(docx_options)}개):")
        for i, opt in enumerate(docx_options, 1):
            print(f"  {i}. {opt}")
        
        if len(prob['options']) < len(docx_options):
            print(f"\n⚠️  DOCX에는 {len(docx_options)}개 있지만 JSON에는 {len(prob['options'])}개만 있습니다!")
            print("누락된 선택지:")
            for i, opt in enumerate(docx_options[len(prob['options']):], len(prob['options'])+1):
                print(f"  {i}. {opt}")
    else:
        print(f"\nDOCX에서 찾기 실패")

print("\n" + "="*70)
print(f"정리: 선택지 이상 문제 {len(problems_with_wrong_options)}개")
print("="*70)
