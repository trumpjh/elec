"""
기본 구현 템플릿 (사용자가 필요에 따라 수정해서 사용)
"""

from docx import Document
import re
import json
from pathlib import Path

class QuestionExtractor:
    """문제 추출 기본 클래스"""
    
    def __init__(self):
        self.questions = []
        self.current_exam = None
    
    def extract_from_docx(self, filepath):
        """docx 파일에서 문제 추출"""
        doc = Document(filepath)
        
        # TODO: 사용자가 구현할 부분
        # 1. 문단 순회
        # 2. 회차 감지
        # 3. 문제 추출
        # 4. 선택지 추출
        # 5. 정답 추출
        
        return self.questions
    
    def save_json(self, output_file, indent=2):
        """JSON으로 저장"""
        data = {
            'total': len(self.questions),
            'questions': self.questions
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        
        print(f"✓ {output_file} 저장 완료 ({len(self.questions)}개 문제)")


class ExplanationExtractor:
    """설명 추출 기본 클래스"""
    
    def __init__(self):
        self.explanations = {}
    
    def extract_from_docx(self, filepath):
        """docx 파일에서 설명 추출"""
        doc = Document(filepath)
        
        # TODO: 사용자가 구현할 부분
        # 1. 표 순회
        # 2. 설명 추출
        # 3. 문제번호 매칭
        
        return self.explanations
    
    def save_json(self, output_file, indent=2):
        """JSON으로 저장"""
        examples = list(self.explanations.values())
        data = {
            'total': len(examples),
            'examples': examples
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        
        print(f"✓ {output_file} 저장 완료 ({len(examples)}개 설명)")


class DataIntegrator:
    """데이터 통합 기본 클래스"""
    
    @staticmethod
    def integrate(questions, explanations):
        """문제와 설명 통합"""
        integrated = []
        
        for q in questions:
            q_num = q.get('number')
            explanation = explanations.get(q_num, {}).get('explanation', '')
            
            q['explanation'] = explanation
            integrated.append(q)
        
        return integrated
    
    @staticmethod
    def save_json(questions, output_file, indent=2):
        """JSON으로 저장"""
        data = {
            'total': len(questions),
            'questions': questions
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        
        print(f"✓ {output_file} 저장 완료 ({len(questions)}개 문제)")


# ============================================================
# 사용 예시
# ============================================================

if __name__ == '__main__':
    # 1단계: 문제 추출
    print("1단계: 문제 추출 중...")
    q_extractor = QuestionExtractor()
    questions = q_extractor.extract_from_docx('2025년도 문제.docx')
    q_extractor.save_json('questions.json')
    
    # 2단계: 설명 추출
    print("\n2단계: 설명 추출 중...")
    e_extractor = ExplanationExtractor()
    explanations = e_extractor.extract_from_docx('2025년도 설명.docx')
    e_extractor.save_json('example.json')
    
    # 3단계: 데이터 통합
    print("\n3단계: 데이터 통합 중...")
    integrated_questions = DataIntegrator.integrate(questions, explanations)
    DataIntegrator.save_json(integrated_questions, 'integrated_questions.json')
    
    print("\n✅ 모든 작업 완료!")
