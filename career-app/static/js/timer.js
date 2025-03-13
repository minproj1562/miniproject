class AssessmentTimer {
    constructor() {
        this.timeData = {};
        this.timerInterval = null;
        this.startTime = Date.now();
    }

    start() {
        this.timerInterval = setInterval(() => this.updateDisplay(), 1000);
    }

    updateDisplay() {
        const elapsed = Math.floor((Date.now() - this.startTime) / 1000);
        const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
        const seconds = (elapsed % 60).toString().padStart(2, '0');
        document.getElementById('timer').textContent = `${minutes}:${seconds}`;
    }

    stop() {
        clearInterval(this.timerInterval);
    }
}

// Initialize timer
document.addEventListener('DOMContentLoaded', () => {
    const timer = new AssessmentTimer();
    timer.start();
    
    document.getElementById('assessmentForm').addEventListener('submit', () => {
        const elapsed = Math.floor((Date.now() - timer.startTime) / 1000);
        document.getElementById('timeData').value = JSON.stringify({
            total_time: elapsed
        });
    });
});