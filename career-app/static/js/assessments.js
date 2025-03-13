class AssessmentManager {
    constructor() {
      this.currentQuestion = 0;
      this.responses = {};
      this.initProgressTracking();
    }
  
    initProgressTracking() {
      const observer = new MutationObserver(() => this.updateProgress());
      observer.observe(document.getElementById('assessment-questions'), {
        childList: true,
        subtree: true
      });
    }
  
    handleOptionSelect(event) {
      const questionId = event.target.closest('[data-question-id]').dataset.questionId;
      const value = JSON.parse(event.target.value);
      
      this.responses[questionId] = value;
      this.updateProgress();
      this.animateSelection(event.target);
    }
  
    animateSelection(element) {
      element.closest('.option-label').animate([
        { transform: 'scale(1)', boxShadow: 'none' },
        { transform: 'scale(1.02)', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' },
        { transform: 'scale(1)' }
      ], 300);
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
      toast.className = 'error-toast';
      // Toast animation and styling
    }
  }