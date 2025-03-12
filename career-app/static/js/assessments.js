document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.personality-assessment form');
    const progressFill = document.querySelector('.progress-fill');
    
    form.addEventListener('change', updateProgress);
    
    function updateProgress() {
        const answered = document.querySelectorAll('input:checked').length;
        const total = document.querySelectorAll('input[type="radio"]').length/4;
        const progress = (answered / total) * 100;
        progressFill.style.width = `${progress}%`;
    }
});