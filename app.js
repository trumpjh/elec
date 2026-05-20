// 전역 변수
let questions = [];
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

// 페이지 로드
document.addEventListener('DOMContentLoaded', async () => {
    await loadQuestions();
    displayQuestion();
    setupEventListeners();
});

// 문제 로드
async function loadQuestions() {
    try {
        const response = await fetch('questions.json');
        const data = await response.json();
        questions = data.questions;
        totalQuestionsEl.textContent = questions.length;
    } catch (error) {
        console.error('문제 로드 실패:', error);
        questionTextEl.textContent = '문제를 로드할 수 없습니다.';
    }
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

    // 문제 번호
    questionNumberEl.textContent = `문제 ${question.number}`;

    // 문제 텍스트
    questionTextEl.textContent = question.question + '?';

    // 선택지
    optionsContainer.innerHTML = '';
    question.options.forEach((option, index) => {
        const optionDiv = document.createElement('div');
        optionDiv.className = 'option';
        optionDiv.innerHTML = `
            <input type="radio" id="option${index}" name="answer" value="${index}">
            <label for="option${index}">${getOptionLabel(index)}. ${option}</label>
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

// 선택지 라벨 (①②③④)
function getOptionLabel(index) {
    return String.fromCharCode(9312 + index);
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
    const correctOptionLabel = getOptionLabel(question.answer);
    correctAnswerEl.innerHTML = `
        <strong>정답:</strong> ${correctOptionLabel}. ${question.options[question.answer]}
    `;

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
    document.querySelector('.quiz-container').innerHTML = `
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

        <div class="completion-section" id="completionSection" style="display:none;">
            <h2>모든 문제를 풀었습니다! 🎉</h2>
            <div class="final-score">
                <p class="score-text">최종 성적</p>
                <p class="score-number"><span id="finalScore">0</span> / ${questions.length}</p>
                <p class="score-percent"><span id="scorePercent">0</span>%</p>
            </div>
            <button class="btn btn-restart" id="restartBtn">처음부터 시작</button>
        </div>
    `;

    // DOM 요소 재할당
    document.getElementById('submitBtn').addEventListener('click', checkAnswer);
    document.getElementById('nextBtn').addEventListener('click', nextQuestion);
    document.getElementById('restartBtn').addEventListener('click', restartQuiz);

    // 첫 번째 문제 표시
    displayQuestion();
}
