document.addEventListener('DOMContentLoaded', () => {
    // Initialize cognitive radar chart
    const cognitiveChart = new Chart(document.getElementById('cognitiveChart'), {
        type: 'radar',
        data: {
            labels: ['Fluid Intel', 'Crystal Intel', 'Quantitative', 'Visual', 'Memory'],
            datasets: [{
                label: 'Cognitive Profile',
                data: [85, 72, 68, 79, 82],
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgb(54, 162, 235)'
            }]
        }
    });

    // Initialize personality bar chart
    const personalityChart = new Chart(document.getElementById('personalityChart'), {
        type: 'bar',
        data: {
            labels: ['Openness', 'Conscientious', 'Extraversion', 'Agreeableness', 'Neuroticism'],
            datasets: [{
                label: 'Personality Traits',
                data: [75, 82, 65, 78, 42],
                backgroundColor: ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
            }]
        }
    });

    // Load career recommendations
    fetch('/api/careers')
        .then(response => response.json())
        .then(careers => {
            const grid = document.getElementById('careerGrid');
            careers.forEach(career => {
                grid.innerHTML += `
                    <div class="career-card p-4 rounded-lg border hover:shadow-md transition">
                        <h3 class="font-bold">${career.title}</h3>
                        <p class="text-sm text-gray-600">${career.match}% Match</p>
                        <div class="mt-2">
                            ${career.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                        </div>
                    </div>
                `;
            });
        });
});