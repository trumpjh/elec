// 전역 변수
let questions = [];
let examples = {};  // 문제번호 -> 설명 매핑
let currentQuestionIndex = 0;
let selectedAnswer = null;
let score = 0;
let answered = false;

// DOM 요소
const questionNumberEl = document.getElementById('questionNumber');
const questionTextEl = document.getElementById('questionText');
const optionsContainer = document.getElementById('optionsContainer');
const submitBtn = document.getElementById('submitBtn');
const nextBtn = document.getElementById('nextBtn');
const progressFill = document.getElementById('progressFill');
const currentQuestionEl = document.getElementById('currentQuestion');
const totalQuestionsEl = document.getElementById('totalQuestions');
const resultSection = document.getElementById('resultSection');
const resultMessage = document.getElementById('resultMessage');
const correctAnswerEl = document.getElementById('correctAnswer');
const completionSection = document.getElementById('completionSection');
const finalScoreEl = document.getElementById('finalScore');
const scorePercentEl = document.getElementById('scorePercent');
const restartBtn = document.getElementById('restartBtn');

// 전역 변수
let allQuestions = [];
let currentCategory = 'all';
let currentExam = 'all';

// 페이지 로드
document.addEventListener('DOMContentLoaded', async () => {
    await loadData();
    displayQuestion();
    setupEventListeners();
    setupCategoryFilter();
    setupExamFilter();
});

// 데이터 로드 (questions.json + example.json)
async function loadData() {
    try {
        // 1. questions.json 로드
        const questionsResponse = await fetch('questions.json');
        const questionsData = await questionsResponse.json();
        allQuestions = questionsData.questions;
        questions = allQuestions;
        
        // 2. example.json 로드
        const examplesResponse = await fetch('example.json');
        const examplesData = await examplesResponse.json();
        
        // 문제번호별로 설명을 매핑
        examplesData.examples.forEach(exp => {
            examples[exp.problem_number] = exp;
        });
        
        // 3. 문제에 설명 추가
        questions.forEach(q => {
            if (examples[q.number]) {
                q.category = examples[q.number].category;
                q.explanation = examples[q.number].explanation;
            }
        });
        
        totalQuestionsEl.textContent = questions.length;
        console.log(`✓ ${questions.length}개 문제 로드됨`);
        console.log(`✓ ${Object.keys(examples).length}개 설명 로드됨`);
        
    } catch (error) {
        console.error('데이터 로드 실패:', error);
        questionTextEl.textContent = '데이터를 로드할 수 없습니다.';
    }
}

// 카테고리 필터 설정
function setupCategoryFilter() {
    const categorySelect = document.getElementById('categorySelect');
    if (!categorySelect) return;
    
    categorySelect.addEventListener('change', (e) => {
        currentCategory = e.target.value;
        applyFilters();
    });
}

// 회차 필터 설정
function setupExamFilter() {
    const examSelect = document.getElementById('examSelect');
    if (!examSelect) return;
    
    examSelect.addEventListener('change', (e) => {
        currentExam = e.target.value;
        applyFilters();
    });
}

// 필터 적용
function applyFilters() {
    let filtered = allQuestions;
    
    // 회차 필터
    if (currentExam !== 'all') {
        filtered = filtered.filter(q => q.exam === currentExam);
    }
    
    // 카테고리 필터
    if (currentCategory !== 'all') {
        filtered = filtered.filter(q => q.category === currentCategory);
    }
    
    questions = filtered;
    
    currentQuestionIndex = 0;
    selectedAnswer = null;
    score = 0;
    answered = false;
    
    totalQuestionsEl.textContent = questions.length;
    document.querySelector('.completion-section').style.display = 'none';
    document.querySelector('.progress-section').style.display = 'block';
    
    displayQuestion();
}

// 문제 표시
function displayQuestion() {
    if (currentQuestionIndex >= questions.length) {
        showCompletionScreen();
        return;
    }

    const question = questions[currentQuestionIndex];
    answered = false;
    selectedAnswer = null;

    // 문제 번호 및 카테고리
    const categoryClass = question.category ? question.category.replace(/\s+/g, '-') : 'default';
    questionNumberEl.textContent = `문제 ${question.number}`;
    questionNumberEl.className = `question-number ${categoryClass}`;

    // 문제 텍스트
    questionTextEl.textContent = question.question + '?';

    // 선택지
    optionsContainer.innerHTML = '';
    question.options.forEach((option, index) => {
        const optionDiv = document.createElement('div');
        optionDiv.className = 'option';
        optionDiv.innerHTML = `
            <input type="radio" id="option${index}" name="answer" value="${index}">
            <label for="option${index}">${option}</label>
        `;
        optionDiv.addEventListener('click', () => selectOption(index, optionDiv));
        optionsContainer.appendChild(optionDiv);
    });

    // UI 초기화
    resultSection.style.display = 'none';
    submitBtn.style.display = 'block';
    nextBtn.style.display = 'none';
    submitBtn.disabled = false;

    // 진행 상황 업데이트
    updateProgress();

    // 현재 문제 표시
    currentQuestionEl.textContent = currentQuestionIndex + 1;
}

// 선택지 선택
function selectOption(index, optionDiv) {
    if (answered) return;

    selectedAnswer = index;

    // 이전 선택 제거
    document.querySelectorAll('.option').forEach(opt => {
        opt.classList.remove('selected');
        opt.querySelector('input[type="radio"]').checked = false;
    });

    // 현재 선택 표시
    optionDiv.classList.add('selected');
    optionDiv.querySelector('input[type="radio"]').checked = true;
}

// 이벤트 리스너 설정
function setupEventListeners() {
    submitBtn.addEventListener('click', checkAnswer);
    nextBtn.addEventListener('click', nextQuestion);
    restartBtn.addEventListener('click', restartQuiz);
}

// 답변 확인
function checkAnswer() {
    if (selectedAnswer === null) {
        alert('선택지를 선택해주세요.');
        return;
    }

    answered = true;
    const question = questions[currentQuestionIndex];
    const isCorrect = selectedAnswer === question.answer;

    // 점수 계산
    if (isCorrect) {
        score++;
    }

    // 결과 표시
    showResult(isCorrect, question);

    // 버튼 전환
    submitBtn.style.display = 'none';
    nextBtn.style.display = 'block';
}

// 결과 표시
function showResult(isCorrect, question) {
    resultSection.style.display = 'block';

    // 결과 메시지
    if (isCorrect) {
        resultMessage.className = 'result-message correct';
        resultMessage.textContent = '✓ 정답입니다!';
    } else {
        resultMessage.className = 'result-message incorrect';
        resultMessage.textContent = '✗ 오답입니다.';
    }

    // 정답 표시
    const correctOptionLabel = question.answer + 1;
    const categoryClass = question.category ? question.category.replace(/\s+/g, '-') : 'default';
    
    let resultHTML = `<strong>정답:</strong> ${correctOptionLabel}. ${question.options[question.answer]}`;

    // 단원명 표시
    if (question.category) {
        resultHTML += `
            <div style="margin-top: 10px;">
                <span class="category-badge ${categoryClass}">${question.category}</span>
            </div>
        `;
    }

    // 설명 표시 (example.json에서 가져온 설명)
    if (question.explanation && question.explanation.trim()) {
        resultHTML += `
            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #cbd5e0;">
                <strong>설명:</strong>
                <p style="margin-top: 8px; line-height: 1.6; white-space: pre-wrap;">${question.explanation}</p>
            </div>
        `;
    }

    correctAnswerEl.innerHTML = resultHTML;

    // 스크롤
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// 진행 상황 업데이트
function updateProgress() {
    const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
    progressFill.style.width = progress + '%';
}

// 다음 문제
function nextQuestion() {
    currentQuestionIndex++;
    displayQuestion();
}

// 완료 화면 표시
function showCompletionScreen() {
    // 메인 컨텐츠 숨기기
    document.querySelector('.quiz-container').innerHTML = '';
    document.querySelector('.quiz-container').appendChild(completionSection);
    completionSection.style.display = 'block';

    // 최종 점수 표시
    finalScoreEl.textContent = score;
    const percent = Math.round((score / questions.length) * 100);
    scorePercentEl.textContent = percent;

    // 헤더 숨기기
    document.querySelector('.progress-section').style.display = 'none';
}

// 처음부터 시작
function restartQuiz() {
    currentQuestionIndex = 0;
    selectedAnswer = null;
    score = 0;
    answered = false;

    // UI 초기화
    document.querySelector('.progress-section').style.display = 'block';
    completionSection.style.display = 'none';
    
    // 컨테이너 다시 구성
    const quizContainer = document.querySelector('.quiz-container');
    quizContainer.innerHTML = `
        <div class="question-card">
            <div class="question-number" id="questionNumber">문제 1</div>
            <div class="question-text" id="questionText">로딩 중...</div>
            
            <div class="options-section">
                <div class="options" id="optionsContainer"></div>
            </div>

            <div class="result-section" id="resultSection" style="display:none;">
                <div class="result-message" id="resultMessage"></div>
                <div class="correct-answer" id="correctAnswer"></div>
            </div>
        </div>

        <div class="button-group">
            <button class="btn btn-submit" id="submitBtn">채점하기</button>
            <button class="btn btn-next" id="nextBtn" style="display:none;">다음 문제</button>
        </div>
    `;
    
    // DOM 요소 재할당
    const newSubmitBtn = document.getElementById('submitBtn');
    const newNextBtn = document.getElementById('nextBtn');
    
    newSubmitBtn.addEventListener('click', checkAnswer);
    newNextBtn.addEventListener('click', nextQuestion);
    
    // 전역 변수 업데이트
    submitBtn = newSubmitBtn;
    nextBtn = newNextBtn;
    optionsContainer = document.getElementById('optionsContainer');
    questionNumberEl = document.getElementById('questionNumber');
    questionTextEl = document.getElementById('questionText');
    resultSection = document.getElementById('resultSection');
    resultMessage = document.getElementById('resultMessage');
    correctAnswerEl = document.getElementById('correctAnswer');
    
    displayQuestion();
}
