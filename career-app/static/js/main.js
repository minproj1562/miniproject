document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('sample-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            let allAnswered = true;
            document.querySelectorAll('.question-card').forEach(card => {
                const selected = card.querySelector('input[type="radio"]:checked');
                if (!selected) {
                    allAnswered = false;
                }
            });

            if (!allAnswered) {
                e.preventDefault();
                alert('Please answer all questions before submitting.');
            }
        });
    }
});