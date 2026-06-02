// 전역 변수
let allQuestions = [];
let filteredQuestions = [];
let currentQuestionIndex = 0;
let selectedAnswer = null;
let score = 0;
let answered = false;
let currentCategory = 'all';
let currentExam = 'all';

// DOM 요소
let questionNumberEl = document.getElementById('questionNumber');
let questionTextEl = document.getElementById('questionText');
let optionsContainer = document.getElementById('optionsContainer');
let submitBtn = document.getElementById('submitBtn');
let nextBtn = document.getElementById('nextBtn');
const progressFill = document.getElementById('progressFill');
const currentQuestionEl = document.getElementById('currentQuestion');
let totalQuestionsEl = document.getElementById('totalQuestions');
let resultSection = document.getElementById('resultSection');
let resultMessage = document.getElementById('resultMessage');
let correctAnswerEl = document.getElementById('correctAnswer');
const completionSection = document.getElementById('completionSection');
const finalScoreEl = document.getElementById('finalScore');
const scorePercentEl = document.getElementById('scorePercent');
const restartBtn = document.getElementById('restartBtn');

// 페이지 로드
document.addEventListener('DOMContentLoaded', async () => {
    await loadData();
    setupEventListeners();
    setupCategoryFilter();
    setupExamFilter();
    displayQuestion();
});

// 데이터 로드 (integrated_questions.json)
async function loadData() {
    try {
        const response = await fetch('integrated_questions.json');
        const data = await response.json();
        allQuestions = data.questions;
        filteredQuestions = allQuestions;
        
        totalQuestionsEl.textContent = filteredQuestions.length;
        console.log(`✓ ${filteredQuestions.length}개 문제 로드됨 (통합 파일)`);
        
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
    
    filteredQuestions = filtered;
    
    currentQuestionIndex = 0;
    selectedAnswer = null;
    score = 0;
    answered = false;
    
    totalQuestionsEl.textContent = filteredQuestions.length;
    completionSection.style.display = 'none';
    
    displayQuestion();
}

// 문제 표시
function displayQuestion() {
    if (currentQuestionIndex >= filteredQuestions.length) {
        showCompletionScreen();
        return;
    }

    const question = filteredQuestions[currentQuestionIndex];
    answered = false;
    selectedAnswer = null;

    // 문제 번호
    questionNumberEl.textContent = `문제 ${question.number}`;

    // 문제 텍스트
    questionTextEl.textContent = question.question;

    // 선택지
    optionsContainer.innerHTML = '';
    const symbols = ['①', '②', '③', '④'];
    
    if (question.options && question.options.length > 0) {
        question.options.forEach((option, index) => {
            const optionDiv = document.createElement('div');
            optionDiv.className = 'option';
            optionDiv.innerHTML = `
                <input type="radio" id="option${index}" name="answer" value="${index}">
                <label for="option${index}">
                    <span class="symbol">${symbols[index]}</span>
                    <span class="text">${option}</span>
                </label>
            `;
            optionDiv.addEventListener('click', () => selectOption(index, optionDiv));
            optionsContainer.appendChild(optionDiv);
        });
    }

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
    const question = filteredQuestions[currentQuestionIndex];
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
    const symbols = ['①', '②', '③', '④'];

    // 결과 메시지
    if (isCorrect) {
        resultMessage.className = 'result-message correct';
        resultMessage.textContent = '✓ 정답입니다!';
    } else {
        resultMessage.className = 'result-message incorrect';
        resultMessage.textContent = '✗ 오답입니다.';
    }

    // 정답 및 설명 표시
    const correctOptionLabel = symbols[question.answer];
    let resultHTML = `<strong>정답:</strong> ${correctOptionLabel} ${question.options[question.answer]}`;

    // 설명 표시
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
    const progress = ((currentQuestionIndex + 1) / filteredQuestions.length) * 100;
    progressFill.style.width = progress + '%';
}

// 다음 문제
function nextQuestion() {
    currentQuestionIndex++;
    displayQuestion();
}

// 완료 화면 표시
function showCompletionScreen() {
    completionSection.style.display = 'block';
    submitBtn.style.display = 'none';
    nextBtn.style.display = 'none';

    // 최종 점수 표시
    finalScoreEl.textContent = score;
    const percent = Math.round((score / filteredQuestions.length) * 100);
    scorePercentEl.textContent = percent;

    // 스크롤
    completionSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// 처음부터 시작
function restartQuiz() {
    currentQuestionIndex = 0;
    selectedAnswer = null;
    score = 0;
    answered = false;

    // UI 초기화
    completionSection.style.display = 'none';
    submitBtn.style.display = 'block';
    nextBtn.style.display = 'none';
    
    displayQuestion();
}
