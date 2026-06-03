/* ============================================================
   전기기능사 문제풀이 시스템 - JavaScript
   ============================================================ */

class QuestionApp {
    constructor() {
        this.allQuestions = [];
        this.filteredQuestions = [];
        this.currentQuestionIndex = 0;
        this.selectedAnswers = {};
        this.currentYear = 2025;
        this.currentExam = 'all';
        this.currentCategory = 'all';
        this.init();
    }

    async init() {
        // 데이터 로드
        await this.loadQuestions();
        
        // 회차 버튼 동적 생성
        this.generateExamButtons();
        
        // 이벤트 리스너 등록
        this.setupEventListeners();
        
        // 초기화
        this.displayWelcome();
        this.updateStats();
    }

    async loadQuestions() {
        try {
            const response = await fetch('questions.json');
            const data = await response.json();
            this.allQuestions = data.questions;
            console.log(`✓ ${this.allQuestions.length}개 문제 로드됨`);
        } catch (error) {
            console.error('❌ 문제 로드 실패:', error);
            alert('문제를 불러올 수 없습니다. questions.json 파일을 확인해주세요.');
        }
    }

    setupEventListeners() {
        // 년도 선택
        document.querySelectorAll('.year-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.year-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.currentYear = parseInt(e.target.dataset.year);
                this.generateExamButtons();
                this.currentExam = 'all';
                this.filterQuestions();
            });
        });

        // 회차 선택 (동적으로 등록)
        this.setupExamButtonListeners();

        // 단원 선택
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.currentCategory = e.target.dataset.category;
                this.filterQuestions();
            });
        });

        // 선택지 클릭
        document.addEventListener('click', (e) => {
            if (e.target.closest('.option')) {
                this.handleOptionClick(e);
            }
        });

        // 네비게이션
        document.getElementById('prevBtn')?.addEventListener('click', () => this.previousQuestion());
        document.getElementById('nextBtn')?.addEventListener('click', () => this.nextQuestion());
        document.getElementById('resetBtn')?.addEventListener('click', () => this.resetQuestion());
    }

    setupExamButtonListeners() {
        // 회차 선택
        document.querySelectorAll('.exam-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.exam-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.currentExam = e.target.dataset.exam;
                this.filterQuestions();
            });
        });
    }

    generateExamButtons() {
        // 선택된 년도의 모든 문제 필터링
        const yearQuestions = this.allQuestions.filter(q => q.year === this.currentYear);
        
        // 회차별로 문제 수 계산
        const examCounts = {};
        yearQuestions.forEach(q => {
            if (!examCounts[q.exam]) {
                examCounts[q.exam] = 0;
            }
            examCounts[q.exam]++;
        });
        
        // 회차 목록 (순서 유지)
        const exams = ['제1회', '제2회', '제3회', '제4회'].filter(exam => examCounts[exam]);
        
        // 버튼 생성
        const examButtonsContainer = document.getElementById('examButtons');
        examButtonsContainer.innerHTML = '<button class="exam-btn active" data-exam="all">전체</button>';
        
        exams.forEach(exam => {
            const btn = document.createElement('button');
            btn.className = 'exam-btn';
            btn.dataset.exam = exam;
            btn.textContent = `${exam} (${examCounts[exam]}문)`;
            examButtonsContainer.appendChild(btn);
        });
        
        // 이벤트 리스너 재등록
        this.setupExamButtonListeners();
    }

    filterQuestions() {
        this.filteredQuestions = this.allQuestions.filter(q => {
            const yearMatch = q.year === this.currentYear;
            const examMatch = this.currentExam === 'all' || q.exam === this.currentExam;
            const categoryMatch = this.currentCategory === 'all' || q.category === this.currentCategory;
            return yearMatch && examMatch && categoryMatch;
        });

        this.currentQuestionIndex = 0;
        this.updateProblemList();
        
        if (this.filteredQuestions.length > 0) {
            this.displayQuestion();
        } else {
            document.getElementById('problemDetail').style.display = 'none';
            document.getElementById('problemContainer').innerHTML = '<p>해당하는 문제가 없습니다.</p>';
        }
    }

    updateProblemList() {
        const problemList = document.getElementById('problemList');
        problemList.innerHTML = '';

        this.filteredQuestions.forEach((q, idx) => {
            const btn = document.createElement('button');
            btn.className = 'problem-item-btn';
            
            if (this.selectedAnswers[`${q.exam}-${q.number}`]) {
                btn.classList.add('solved');
            }

            btn.textContent = `${q.number}번`;
            btn.addEventListener('click', () => {
                this.currentQuestionIndex = idx;
                this.displayQuestion();
            });

            problemList.appendChild(btn);
        });
    }

    displayWelcome() {
        const container = document.getElementById('problemContainer');
        container.className = 'problem-container welcome';
        container.innerHTML = `
            <div class="welcome-text">
                <h2>⚡ 전기기능사 문제풀이</h2>
                <p>좌측 메뉴에서 회차를 선택하고 문제를 풀어보세요!</p>
                <p>총 <strong>${this.allQuestions.length}개</strong>의 문제가 준비되어 있습니다.</p>
            </div>
        `;
        document.getElementById('problemDetail').style.display = 'none';
    }

    displayQuestion() {
        if (this.filteredQuestions.length === 0) {
            this.displayWelcome();
            return;
        }

        const q = this.filteredQuestions[this.currentQuestionIndex];
        const answerKey = `${q.exam}-${q.number}`;
        const selectedAnswer = this.selectedAnswers[answerKey];

        // 컨테이너 숨기고 상세정보 표시
        document.getElementById('problemContainer').style.display = 'none';
        document.getElementById('problemDetail').style.display = 'block';

        // 문제 정보
        document.getElementById('detailNumber').textContent = q.number;
        document.getElementById('detailExam').textContent = q.exam;
        // innerHTML을 사용하여 HTML 테이블 렌더링 지원
        document.getElementById('detailQuestion').innerHTML = q.question;

        // 문제 이미지 처리
        const problemImageEl = document.getElementById('problemImage');
        const problemImg = document.getElementById('problemImg');
        if (q.image) {
            problemImg.src = q.image;
            problemImg.alt = `${q.exam} 문제 ${q.number} 이미지`;
            
            // 제4회 9번은 이미지 크기 2배로 설정
            if (q.exam === '제4회' && q.number === 9) {
                problemImg.style.maxHeight = '800px';
            } else {
                problemImg.style.maxHeight = '400px';
            }
            
            problemImageEl.style.display = 'block';
        } else {
            problemImageEl.style.display = 'none';
        }

        // 선택지
        q.options.forEach((option, idx) => {
            const optionEl = document.getElementById(`option${idx}`);
            optionEl.textContent = option;
        });

        // 결과 표시 여부
        if (selectedAnswer !== undefined) {
            this.showResult(q, selectedAnswer, answerKey);
        } else {
            document.getElementById('resultContainer').style.display = 'none';
            
            // 선택지 리셋
            document.querySelectorAll('.option').forEach(opt => {
                opt.classList.remove('selected', 'correct', 'incorrect');
            });
        }

        // 네비게이션 버튼 상태
        document.getElementById('prevBtn').disabled = this.currentQuestionIndex === 0;
        document.getElementById('nextBtn').disabled = this.currentQuestionIndex === this.filteredQuestions.length - 1;

        // 문제 목록 스크롤
        const activeBtn = document.querySelectorAll('.problem-item-btn')[this.currentQuestionIndex];
        if (activeBtn) {
            activeBtn.scrollIntoView({ block: 'nearest' });
        }
    }

    handleOptionClick(e) {
        if (document.getElementById('resultContainer').style.display !== 'none') {
            return; // 이미 답변한 경우 클릭 불가
        }

        const option = e.target.closest('.option');
        const selectedIndex = parseInt(option.dataset.index);
        const q = this.filteredQuestions[this.currentQuestionIndex];
        const answerKey = `${q.exam}-${q.number}`;

        this.selectedAnswers[answerKey] = selectedIndex;
        this.showResult(q, selectedIndex, answerKey);
        this.updateProblemList();
        this.updateStats();
    }

    showResult(q, selectedIndex, answerKey) {
        const isCorrect = selectedIndex === q.answer;
        const resultContainer = document.getElementById('resultContainer');
        const resultMessage = document.getElementById('resultMessage');
        const explanationDiv = document.getElementById('explanation');

        // 결과 메시지
        resultMessage.className = `result ${isCorrect ? 'correct' : 'incorrect'}`;
        resultMessage.innerHTML = isCorrect 
            ? '✓ 정답입니다! 축하합니다!' 
            : '✗ 오답입니다. 다시 확인해보세요.';

        // 선택지 스타일 업데이트
        document.querySelectorAll('.option').forEach((opt, idx) => {
            opt.classList.remove('selected', 'correct', 'incorrect');
            
            if (idx === selectedIndex) {
                opt.classList.add(isCorrect ? 'correct' : 'incorrect');
            } else if (idx === q.answer) {
                opt.classList.add('correct');
            }
        });

        // 설명
        let explanationHTML = '<div class="explanation-title">📚 설명</div>';
        if (q.explanation) {
            explanationHTML += `<div class="explanation-content">${q.explanation}</div>`;
        } else {
            explanationHTML += '<div class="explanation-content">설명이 준비 중입니다.</div>';
        }
        
        // 설명 이미지
        if (q.explanation_image) {
            explanationHTML += `<div style="margin-top: 15px; text-align: center;">
                <img src="${q.explanation_image}" alt="설명 이미지" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; padding: 5px;">
            </div>`;
        }
        
        explanationDiv.innerHTML = explanationHTML;

        resultContainer.style.display = 'block';
    }

    previousQuestion() {
        if (this.currentQuestionIndex > 0) {
            this.currentQuestionIndex--;
            this.displayQuestion();
        }
    }

    nextQuestion() {
        if (this.currentQuestionIndex < this.filteredQuestions.length - 1) {
            this.currentQuestionIndex++;
            this.displayQuestion();
        }
    }

    resetQuestion() {
        const q = this.filteredQuestions[this.currentQuestionIndex];
        const answerKey = `${q.exam}-${q.number}`;
        
        delete this.selectedAnswers[answerKey];
        this.updateProblemList();
        this.updateStats();
        this.displayQuestion();
    }

    updateStats() {
        const total = this.allQuestions.length;
        const solved = Object.keys(this.selectedAnswers).length;
        const correct = Object.entries(this.selectedAnswers).filter(([key, idx]) => {
            const [exam, num] = key.split('-');
            const question = this.allQuestions.find(q => q.exam === exam && q.number == num);
            return question && question.answer === idx;
        }).length;

        document.getElementById('totalProblems').textContent = total;
        document.getElementById('solvedProblems').textContent = solved;
        document.getElementById('correctRate').textContent = 
            solved > 0 ? `${Math.round((correct / solved) * 100)}%` : '0%';
    }
}

// 앱 시작
document.addEventListener('DOMContentLoaded', () => {
    new QuestionApp();
});
