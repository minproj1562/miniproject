// Consolidated Assessment Manager, Timer, and Progress Functions

class AssessmentManager {
  constructor() {
    this.currentQuestion = 0;
    this.responses = {};
    if (document.getElementById('assessment-questions')) {
      this.initProgressTracking();
    }
  }

  initProgressTracking() {
    const observer = new MutationObserver(() => this.updateProgress());
    observer.observe(document.getElementById('assessment-questions'), {
      childList: true,
      subtree: true
    });
  }

  handleOptionSelect(event) {
    const questionElement = event.target.closest('[data-question-id]');
    if (!questionElement) return;
    const questionId = questionElement.dataset.questionId;
    const value = JSON.parse(event.target.value);
    
    this.responses[questionId] = value;
    if (typeof this.updateProgress === "function") {
      this.updateProgress();
    }
    this.animateSelection(event.target);
  }

  animateSelection(element) {
    const optionLabel = element.closest('.option-label');
    if (optionLabel) {
      optionLabel.animate([
        { transform: 'scale(1)', boxShadow: 'none' },
        { transform: 'scale(1.02)', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' },
        { transform: 'scale(1)' }
      ], 300);
    }
  }

  async submitAssessment() {
    try {
      const response = await fetch('/submit-assessment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': document.querySelector('[name=csrf_token]').value
        },
        body: JSON.stringify(this.responses)
      });
      if (!response.ok) throw new Error('Submission failed');
      window.location = response.headers.get('Location');
    } catch (error) {
      this.showErrorToast('Submission failed. Please try again.');
    }
  }

  showErrorToast(message) {
    const toast = document.createElement('div');
    toast.className = 'error-toast alert alert-danger';
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => {
      toast.remove();
    }, 3000);
  }
}

class AssessmentTimer {
  constructor(timerElementId, formElementId, timeDataElementId) {
    this.timerElement = document.getElementById(timerElementId);
    this.formElement = document.getElementById(formElementId);
    this.timeDataElement = document.getElementById(timeDataElementId);
    this.timerInterval = null;
    this.startTime = Date.now();
  }

  start() {
    this.timerInterval = setInterval(() => this.updateDisplay(), 1000);
  }

  updateDisplay() {
    if (!this.timerElement) return;
    const elapsed = Math.floor((Date.now() - this.startTime) / 1000);
    const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
    const seconds = (elapsed % 60).toString().padStart(2, '0');
    this.timerElement.textContent = `${minutes}:${seconds}`;
  }

  stop() {
    clearInterval(this.timerInterval);
  }

  attachFormListener() {
    if (this.formElement && this.timeDataElement) {
      this.formElement.addEventListener('submit', () => {
        const elapsed = Math.floor((Date.now() - this.startTime) / 1000);
        this.timeDataElement.value = JSON.stringify({ total_time: elapsed });
      });
    }
  }
}

function saveProgress(stageId) {
  const checkbox = document.getElementById(stageId);
  if (checkbox) {
    const isChecked = checkbox.checked;
    localStorage.setItem(stageId, isChecked);
    updateProgressBar();
  }
}

function loadProgress() {
  const stages = document.querySelectorAll('.progress-check');
  stages.forEach(stage => {
    const stageId = stage.id;
    const isChecked = localStorage.getItem(stageId) === 'true';
    stage.checked = isChecked;
  });
}

function updateProgressBar() {
  const stages = document.querySelectorAll('.progress-check');
  const completedStages = Array.from(stages).filter(stage => stage.checked).length;
  const totalStages = stages.length;
  const progressPercentage = (completedStages / totalStages) * 100;
  const progressBarInner = document.getElementById('progress-bar-inner');
  if (progressBarInner) {
    progressBarInner.style.width = progressPercentage + '%';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // Timer initialization (if the relevant elements exist)
  if (
    document.getElementById('timer') &&
    document.getElementById('assessmentForm') &&
    document.getElementById('timeData')
  ) {
    const timer = new AssessmentTimer('timer', 'assessmentForm', 'timeData');
    timer.start();
    timer.attachFormListener();
  }
  loadProgress();
  updateProgressBar();
});
