#!/usr/bin/env python3
"""
2025년도 전기기능사 시험 학습 도구
문제를 풀고 정답과 설명을 즉시 확인할 수 있습니다.
"""

import json
import sys
from pathlib import Path

class ExamTutor:
    def __init__(self, json_file='integrated_questions.json'):
        """초기화"""
        self.json_file = json_file
        self.data = self.load_data()
        self.questions = self.data.get('questions', [])
        self.total = len(self.questions)
        self.score = 0
        self.attempt = 0
    
    def load_data(self):
        """JSON 파일 로드"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"오류: {self.json_file} 파일을 찾을 수 없습니다.")
            sys.exit(1)
    
    def display_question(self, question):
        """문제 표시"""
        num = question.get('number', '?')
        q_text = question.get('question', '')
        options = question.get('options', [])
        
        print(f"\n{'='*80}")
        print(f"문제 {num}")
        print(f"{'='*80}")
        print(f"\n{q_text}\n")
        
        if options:
            for i, opt in enumerate(options, 1):
                print(f"  ① {opt}" if i == 1 else f"  ② {opt}" if i == 2 else f"  ③ {opt}" if i == 3 else f"  ④ {opt}", end='')
                if i < len(options):
                    print()
        else:
            print("[선택지 정보 없음]")
        
        print(f"\n{'-'*80}")
    
    def check_answer(self, question, answer_idx):
        """답 확인"""
        correct_answer = question.get('answer')
        explanation = question.get('explanation', '설명이 없습니다.')
        
        # 0-indexed를 1-indexed로 변환
        answer_symbols = ['①', '②', '③', '④']
        
        print(f"\n당신의 답: {answer_symbols[answer_idx]}")
        print(f"정답: {answer_symbols[correct_answer] if correct_answer is not None else '?'}")
        
        is_correct = answer_idx == correct_answer
        
        if is_correct:
            print(f"\n✓ 정답입니다!")
            self.score += 1
        else:
            print(f"\n✗ 틀렸습니다.")
        
        print(f"\n[설명]")
        print(f"{explanation}")
        
        return is_correct
    
    def interactive_mode(self):
        """대화형 모드"""
        print(f"\n{'='*80}")
        print(f"2025년도 전기기능사 문제 학습 도구")
        print(f"총 {self.total}개 문제")
        print(f"{'='*80}")
        
        for q_idx, question in enumerate(self.questions, 1):
            self.display_question(question)
            
            while True:
                try:
                    answer = input("정답을 선택하세요 (1-4, 0:건너뛰기, q:종료): ").strip()
                    
                    if answer.lower() == 'q':
                        self.show_summary()
                        return
                    elif answer == '0':
                        print("건너뛰었습니다.\n")
                        break
                    elif answer in ['1', '2', '3', '4']:
                        answer_idx = int(answer) - 1
                        self.check_answer(question, answer_idx)
                        self.attempt += 1
                        
                        input("\n[Enter를 누르세요 계속...]")
                        break
                    else:
                        print("잘못된 입력입니다. 1-4 또는 0, q를 입력하세요.")
                except KeyboardInterrupt:
                    print("\n\n프로그램을 종료합니다.")
                    self.show_summary()
                    return
        
        self.show_summary()
    
    def search_mode(self, keyword):
        """검색 모드"""
        print(f"\n'{keyword}'를(을) 포함하는 문제들:\n")
        
        found = []
        for q in self.questions:
            if keyword in q.get('question', ''):
                found.append(q)
        
        if not found:
            print(f"'{keyword}'를(을) 포함하는 문제가 없습니다.")
            return
        
        for question in found:
            self.display_question(question)
            print(f"[설명]\n{question.get('explanation', '설명이 없습니다.')}\n")
    
    def problem_mode(self, problem_num):
        """특정 문제 학습 모드"""
        for q in self.questions:
            if q.get('number') == problem_num:
                self.display_question(q)
                
                while True:
                    try:
                        answer = input("정답을 선택하세요 (1-4, q:종료): ").strip()
                        
                        if answer.lower() == 'q':
                            return
                        elif answer in ['1', '2', '3', '4']:
                            answer_idx = int(answer) - 1
                            self.check_answer(q, answer_idx)
                            self.attempt += 1
                            break
                        else:
                            print("잘못된 입력입니다.")
                    except KeyboardInterrupt:
                        return
                break
        else:
            print(f"문제 {problem_num}을(를) 찾을 수 없습니다.")
    
    def show_summary(self):
        """학습 결과 요약"""
        print(f"\n{'='*80}")
        print(f"학습 완료!")
        print(f"{'='*80}")
        if self.attempt > 0:
            print(f"시도: {self.attempt}문제")
            print(f"정답: {self.score}문제")
            print(f"오답: {self.attempt - self.score}문제")
            print(f"정답률: {self.score/self.attempt*100:.1f}%")
        else:
            print(f"풀어본 문제가 없습니다.")
        print(f"{'='*80}\n")
    
    def show_help(self):
        """도움말"""
        print(f"""
사용 방법:
  python exam_tutor.py [옵션]

옵션:
  (옵션 없음)     대화형 모드 - 순서대로 모든 문제 풀기
  -p <번호>       특정 문제 풀기 (예: -p 1, -p 10)
  -s <키워드>     키워드로 문제 검색 (예: -s "변압기")
  -l              모든 문제 목록 보기
  -h, --help      이 도움말 보기

예시:
  python exam_tutor.py                   # 모든 문제를 순서대로 풀기
  python exam_tutor.py -p 5               # 문제 5번만 풀기
  python exam_tutor.py -s "접지"          # "접지"를 포함하는 문제 검색
        """)
    
    def show_list(self):
        """문제 목록 표시"""
        print(f"\n{'='*80}")
        print(f"전체 문제 목록 ({self.total}개)")
        print(f"{'='*80}\n")
        
        for q in self.questions:
            num = q.get('number')
            question = q.get('question', '')[:60]
            print(f"문제 {num:2d}: {question}...")
        
        print()

def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description='2025년도 전기기능사 시험 학습 도구')
    parser.add_argument('-p', '--problem', type=int, help='특정 문제 번호')
    parser.add_argument('-s', '--search', help='키워드 검색')
    parser.add_argument('-l', '--list', action='store_true', help='문제 목록 보기')
    parser.add_argument('-j', '--json', default='integrated_questions.json', help='JSON 파일 경로')
    
    args = parser.parse_args()
    
    tutor = ExamTutor(args.json)
    
    if args.problem:
        tutor.problem_mode(args.problem)
    elif args.search:
        tutor.search_mode(args.search)
    elif args.list:
        tutor.show_list()
    else:
        tutor.interactive_mode()

if __name__ == '__main__':
    main()
