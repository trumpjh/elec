"""
docx 파일에서 회차별 문제 개수를 정확히 파악하는 스크립트
"""

from docx import Document
import re

def analyze_rounds(docx_path):
    """회차별 문제 분석"""
    doc = Document(docx_path)
    
    print(f"\n{'='*80}")
    print(f"파일: {docx_path}")
    print(f"{'='*80}\n")
    
    # 문단에서 회차 찾기
    rounds = {}
    current_round = None
    question_count = 0
    
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        
        # 회차 찾기 (예: "2025년도 제1회 문제")
        if '제' in text and '회' in text and '문제' in text:
            match = re.search(r'제(\d+)회', text)
            if match:
                current_round = f"제{match.group(1)}회"
                print(f"[{current_round}]")
                rounds[current_round] = []
        
        # 문제 번호 찾기 (예: "1.", "11.", "2.")
        if current_round:
            match = re.match(r'^(\d+)\.\s+', text)
            if match:
                q_num = int(match.group(1))
                rounds[current_round].append(q_num)
                print(f"  문제 {q_num}")
    
    # 통계
    print(f"\n{'='*80}")
    print(f"[회차별 통계]")
    print(f"{'='*80}")
    total = 0
    for round_name in sorted(rounds.keys()):
        questions = sorted(set(rounds[round_name]))
        count = len(questions)
        total += count
        print(f"{round_name}: {count}개 - {questions}")
    
    print(f"\n총계: {total}개")
    print(f"{'='*80}\n")

# 문제 파일 분석
print("\n【2025년도 문제.docx 분석】")
analyze_rounds('2025년도 문제.docx')
