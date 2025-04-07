const mockQuestions = [
    "Tell me about yourself.",
    "Why are you interested in this position?",
    "What are your greatest strengths?",
    "Where do you see yourself in 5 years?",
    "Why should we hire you?",
    "Describe a challenging situation and how you handled it.",
    "What are your salary expectations?",
    "Do you have any questions for us?"
];

const technicalTopics = [
    "Data Structures", "Algorithms", "System Design", "Programming Languages",
    "Databases", "Web Technologies", "Operating Systems", "Networking", "Cloud Computing"
];

const behavioralQuestions = [
    "Describe a time when you demonstrated leadership.",
    "Tell me about a project you're proud of.",
    "How do you handle conflicts in a team?",
    "Describe a failure and what you learned from it.",
    "How do you prioritize tasks when you have multiple deadlines?"
];

let currentQuestionIndex = 0;
let timer;

function startMockInterview() {
    document.getElementById('mockInterviewModal').style.display = 'flex';
    currentQuestionIndex = 0;
    showQuestion();
    startTimer();
    document.querySelector('.loading-overlay').style.display = 'flex';
    setTimeout(() => document.querySelector('.loading-overlay').style.display = 'none', 500);
}

function showQuestion() {
    document.getElementById('questionContainer').innerHTML = mockQuestions[currentQuestionIndex];
    document.getElementById('feedback').innerHTML = '';
}

function nextQuestion() {
    currentQuestionIndex = (currentQuestionIndex + 1) % mockQuestions.length;
    showQuestion();
    updateMockProgress();
}

function startTimer() {
    let seconds = 0;
    clearInterval(timer);
    timer = setInterval(() => {
        seconds++;
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        document.getElementById('timer').innerHTML = `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
    }, 1000);
}

function closeMockInterview() {
    document.getElementById('mockInterviewModal').style.display = 'none';
    clearInterval(timer);
}

function showTechnicalTopics() {
    const modal = document.getElementById('technicalModal');
    const topicsContainer = document.getElementById('techTopics');
    topicsContainer.innerHTML = technicalTopics.map(topic => `<span class="tag">${topic}</span>`).join('');
    modal.style.display = 'flex';
    document.querySelector('.loading-overlay').style.display = 'flex';
    setTimeout(() => document.querySelector('.loading-overlay').style.display = 'none', 500);
}

function closeTechnical() {
    document.getElementById('technicalModal').style.display = 'none';
}

function showBehavioralQuestions() {
    const modal = document.getElementById('behavioralModal');
    document.getElementById('starGuide').innerHTML = `
        <h3>STAR Method:</h3>
        <p><strong>S</strong>ituation: Describe the context</p>
        <p><strong>T</strong>ask: Explain your responsibility</p>
        <p><strong>A</strong>ction: What steps did you take?</p>
        <p><strong>R</strong>esult: What was the outcome?</p>
    `;
    document.getElementById('behavioralQuestion').innerHTML = behavioralQuestions[Math.floor(Math.random() * behavioralQuestions.length)];
    modal.style.display = 'flex';
    document.querySelector('.loading-overlay').style.display = 'flex';
    setTimeout(() => document.querySelector('.loading-overlay').style.display = 'none', 500);
}

function closeBehavioral() {
    document.getElementById('behavioralModal').style.display = 'none';
}

function updateMockProgress() {
    const progress = ((currentQuestionIndex + 1) / mockQuestions.length) * 100;
    document.getElementById('mockProgress').style.width = `${progress}%`;
}

function updateProgress() {
    const checkboxes = document.querySelectorAll('.checklist input[type="checkbox"]');
    const checked = Array.from(checkboxes).filter(cb => cb.checked).length;
    const progress = (checked / checkboxes.length) * 100;
    document.getElementById('mockProgress').style.width = `${progress}%`;
}

window.onclick = function(event) {
    const modals = document.getElementsByClassName('modal');
    Array.from(modals).forEach(modal => {
        if (event.target == modal) {
            modal.style.display = 'none';
            if (modal.id === 'mockInterviewModal') {
                clearInterval(timer);
            }
            document.querySelector('.loading-overlay').style.display = 'none';
        }
    });
};