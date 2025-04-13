// Debounce function to limit frequent calls
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Update preview with debounced server call
const updatePreview = debounce(() => {
    const form = document.getElementById('resumeForm');
    const formData = new FormData(form);

    fetch('/resume_builder', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            localStorage.setItem('lastResumeId', JSON.stringify(data.resume_id)); // Store resume ID
            fetchResumePreview(data.resume_id);
            alert('Resume saved successfully!');
        } else {
            alert(`Error saving resume: ${data.error || 'Unknown error'}`);
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
        alert('An error occurred while updating the preview.');
    });
}, 500); // 500ms debounce delay

function fetchResumePreview(resumeId) {
    fetch(`/get-template-html?template=${document.getElementById('templateSelect').value}`)
    .then(response => response.text())
    .then(html => {
        document.getElementById('resumePreview').innerHTML = html;

        // Fetch latest resume data from server
        fetch(`/resume_builder?resume_id=${resumeId}`, {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            const resume = data.resume || {};
            localStorage.setItem('resumePreview', JSON.stringify(resume));

            // Update preview elements
            document.getElementById('previewName').textContent = resume.personal_info?.name || 'Your Name';
            document.getElementById('previewEmail').textContent = `Email: ${resume.personal_info?.email || 'your.email@example.com'}`;
            document.getElementById('previewPhone').textContent = `Phone: ${resume.personal_info?.phone || '(123) 456-7890'}`;
            document.getElementById('previewLinkedIn').textContent = `LinkedIn: ${resume.personal_info?.linkedin || 'linkedin.com/in/yourprofile'}`;
            document.getElementById('previewSummary').textContent = resume.summary || 'Your professional summary will appear here.';

            // Update education
            const educationPreview = document.getElementById('previewEducation');
            educationPreview.innerHTML = '<h3>Education</h3>';
            (resume.education || []).forEach(edu => {
                const div = document.createElement('div');
                div.className = 'education-item';
                div.innerHTML = `<h4>${edu.degree || ''}</h4><p>${edu.institution || ''} - ${edu.date || ''}</p>`;
                educationPreview.appendChild(div);
            });

            // Update experience
            const experiencePreview = document.getElementById('previewExperience');
            experiencePreview.innerHTML = '<h3>Experience</h3>';
            (resume.experience || []).forEach(exp => {
                const div = document.createElement('div');
                div.className = 'experience-item';
                div.innerHTML = `<h4>${exp.position || ''}</h4><p>${exp.company || ''} - ${exp.date || ''}</p><p>${exp.description || ''}</p>`;
                experiencePreview.appendChild(div);
            });

            // Update skills
            const skillsPreview = document.getElementById('previewSkills');
            skillsPreview.innerHTML = '<h3>Skills</h3>';
            (resume.skills || []).forEach(skill => {
                const span = document.createElement('span');
                span.className = 'skill-tag';
                span.textContent = skill;
                skillsPreview.appendChild(span);
            });

            // Update photo if present
            const previewPhoto = document.getElementById('previewPhoto');
            if (resume.photo) {
                previewPhoto.src = resume.photo;
                previewPhoto.style.display = 'block';
            } else {
                previewPhoto.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error fetching resume data:', error);
            alert('Failed to load preview data.');
        });
    })
    .catch(error => {
        console.error('Error loading template:', error);
        alert('Failed to load resume template.');
    });
}

function addEducation() {
    const educationFields = document.getElementById('educationFields');
    const existingFields = educationFields.getElementsByClassName('dynamic-section').length;
    if (existingFields >= 5) { // Limit to 5 education entries
        alert('Maximum 5 education entries allowed.');
        return;
    }

    const newField = document.createElement('div');
    newField.className = 'dynamic-section mt-2';
    newField.innerHTML = `
        <input type="text" class="form-control" name="education[]" placeholder="Degree" required onchange="updatePreview()">
        <input type="text" class="form-control" name="institution[]" placeholder="Institution" required onchange="updatePreview()">
        <input type="month" class="form-control" name="education_date[]" onchange="updatePreview()">
        <button type="button" class="btn btn-sm btn-danger mt-2" onclick="this.parentElement.remove(); updatePreview()">Remove</button>
    `;
    educationFields.appendChild(newField);
}

function addExperience() {
    const experienceFields = document.getElementById('experienceFields');
    const existingFields = experienceFields.getElementsByClassName('dynamic-section').length;
    if (existingFields >= 5) { // Limit to 5 experience entries
        alert('Maximum 5 experience entries allowed.');
        return;
    }

    const newField = document.createElement('div');
    newField.className = 'dynamic-section mt-2';
    newField.innerHTML = `
        <input type="text" class="form-control" name="position[]" placeholder="Position" onchange="updatePreview()">
        <input type="text" class="form-control" name="company[]" placeholder="Company" onchange="updatePreview()">
        <textarea class="form-control" name="description[]" placeholder="Job Description" onchange="updatePreview()"></textarea>
        <input type="month" class="form-control" name="experience_date[]" onchange="updatePreview()">
        <button type="button" class="btn btn-sm btn-danger mt-2" onclick="this.parentElement.remove(); updatePreview()">Remove</button>
    `;
    experienceFields.appendChild(newField);
}

function removeSkill(skill) {
    let skills = JSON.parse(document.getElementById('hiddenSkills').value || '[]');
    skills = skills.filter(s => s !== skill);
    document.getElementById('hiddenSkills').value = JSON.stringify(skills);
    document.getElementById('selectedSkills').innerHTML = skills.map(s => `<span class="skill-tag">${s} <button type="button" onclick="removeSkill('${s}'); updatePreview()">×</button></span>`).join('');
    updatePreview(); // Ensure preview reflects change
}

function updateTemplatePreview() {
    const template = document.getElementById('templateSelect').value;
    document.getElementById('currentTemplate').value = template;
    updatePreview();
}

function exportPDF() {
    const resumeId = JSON.parse(localStorage.getItem('lastResumeId'));
    if (resumeId) {
        window.location.href = `/export-resume/${resumeId}`;
    } else {
        alert('Please save your resume first!');
    }
}

// Suggestion dropdown
document.getElementById('skillInput').addEventListener('input', function(e) {
    const query = e.target.value.trim();
    if (query.length < 1) {
        document.getElementById('suggestions').style.display = 'none';
        return;
    }
    fetch(`/api/career-suggestions?skills=${encodeURIComponent(query)}`)
    .then(response => response.json())
    .then(suggestions => {
        const suggestionsDiv = document.getElementById('suggestions');
        suggestionsDiv.innerHTML = suggestions.map(s => `<div class="suggestion-item" onclick="selectSuggestion('${s}')">${s}</div>`).join('');
        suggestionsDiv.style.display = 'block';
    })
    .catch(error => {
        console.error('Error fetching suggestions:', error);
        document.getElementById('suggestions').style.display = 'none';
    });
});

function selectSuggestion(skill) {
    let skills = JSON.parse(document.getElementById('hiddenSkills').value || '[]');
    if (!skills.includes(skill)) {
        skills.push(skill);
        document.getElementById('hiddenSkills').value = JSON.stringify(skills);
        document.getElementById('selectedSkills').innerHTML += `<span class="skill-tag">${skill} <button type="button" onclick="removeSkill('${skill}'); updatePreview()">×</button></span>`;
    }
    document.getElementById('skillInput').value = '';
    document.getElementById('suggestions').style.display = 'none';
    updatePreview();
}

// Close suggestions only when clicking outside the input
document.addEventListener('click', function(e) {
    const skillsContainer = document.getElementById('skillsContainer');
    const skillInput = document.getElementById('skillInput');
    if (!skillsContainer.contains(e.target) && e.target !== skillInput) {
        document.getElementById('suggestions').style.display = 'none';
    }
});

// Initialize preview on page load
document.addEventListener('DOMContentLoaded', () => {
    const resumeId = JSON.parse(localStorage.getItem('lastResumeId'));
    if (resumeId) {
        fetchResumePreview(resumeId);
    }
});