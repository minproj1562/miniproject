// Resume Builder Core Functionality
document.addEventListener('DOMContentLoaded', () => {
    initializeTemplateSelector();
    initializeSkillManagement();
    initializeFormValidation();
    initializeDynamicSections();
    loadSavedResume();
});

// Template Management
function initializeTemplateSelector() {
    document.querySelectorAll('.template-option').forEach(option => {
        option.addEventListener('click', function() {
            // Remove all active classes
            document.querySelectorAll('.template-option').forEach(opt => 
                opt.classList.remove('active'));
            
            // Set new active template
            this.classList.add('active');
            const template = this.dataset.value;
            document.getElementById('templateSelect').value = template;
            document.getElementById('templateName').textContent = 
                `${template.charAt(0).toUpperCase() + template.slice(1)} Template`;
            
            updatePreview();
        });
    });
}

// Skill Management System
function initializeSkillManagement() {
    // Handle common skill checkboxes
    document.querySelectorAll('.skill-checkbox input').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const category = this.name === 'technical_skills' ? 'technical' : 'soft';
            updateHiddenSkills(category);
            updatePreview();
        });
    });

    // Custom skill addition
    document.querySelectorAll('.btn-add-skill').forEach(button => {
        button.addEventListener('click', function() {
            const category = this.dataset.category;
            const input = document.getElementById(`custom${category.charAt(0).toUpperCase() + category.slice(1)}`);
            const skill = input.value.trim();
            
            if (skill) {
                const hiddenField = document.getElementById(`hidden${category.charAt(0).toUpperCase() + category.slice(1)}Skills`);
                const skills = JSON.parse(hiddenField.value || '[]');
                
                if (!skills.includes(skill)) {
                    skills.push(skill);
                    hiddenField.value = JSON.stringify(skills);
                    appendSkillToPreview(skill, category);
                    input.value = '';
                }
            }
        });
    });
}

function updateHiddenSkills(category) {
    const checkboxes = document.querySelectorAll(`input[name="${category}_skills"]:checked`);
    const skills = Array.from(checkboxes).map(cb => cb.value);
    document.getElementById(`hidden${category.charAt(0).toUpperCase() + category.slice(1)}Skills`).value = 
        JSON.stringify(skills);
}

function appendSkillToPreview(skill, category) {
    const previewSection = document.getElementById(`${category}-skills-preview`);
    const tag = document.createElement('span');
    tag.className = 'skill-tag';
    tag.innerHTML = `
        ${skill}
        <button type="button" class="btn-remove-skill" onclick="removeSkill('${skill}', '${category}')">
            &times;
        </button>
    `;
    previewSection.appendChild(tag);
}

// Dynamic Section Management
function initializeDynamicSections() {
    // Education section
    document.getElementById('educationFields').addEventListener('input', debounce(updatePreview, 300));
    
    // Experience section
    document.getElementById('experienceFields').addEventListener('input', debounce(updatePreview, 300));
}

function addEducation() {
    const educationFields = document.getElementById('educationFields');
    if (educationFields.children.length >= 5) {
        showAlert('Maximum of 5 education entries allowed', 'warning');
        return;
    }

    const newField = createDynamicSection([
        { type: 'text', name: 'education[]', placeholder: 'Degree', required: true },
        { type: 'text', name: 'institution[]', placeholder: 'Institution', required: true },
        { type: 'month', name: 'education_date[]' }
    ]);
    
    educationFields.appendChild(newField);
    updatePreview();
}

function addExperience() {
    const experienceFields = document.getElementById('experienceFields');
    if (experienceFields.children.length >= 5) {
        showAlert('Maximum of 5 experience entries allowed', 'warning');
        return;
    }

    const newField = createDynamicSection([
        { type: 'text', name: 'position[]', placeholder: 'Position' },
        { type: 'text', name: 'company[]', placeholder: 'Company' },
        { type: 'textarea', name: 'description[]', placeholder: 'Description' },
        { type: 'month', name: 'experience_date[]' }
    ]);
    
    experienceFields.appendChild(newField);
    updatePreview();
}

function createDynamicSection(fields) {
    const section = document.createElement('div');
    section.className = 'dynamic-section';
    
    fields.forEach(field => {
        const element = document.createElement(field.type === 'textarea' ? 'textarea' : 'input');
        element.className = 'form-control';
        element.placeholder = field.placeholder;
        element.name = field.name;
        
        if (field.type !== 'textarea') {
            element.type = field.type;
        }
        
        if (field.required) {
            element.required = true;
        }
        
        section.appendChild(element);
    });

    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.className = 'btn-remove';
    removeBtn.innerHTML = '<i class="fas fa-times"></i>';
    removeBtn.addEventListener('click', () => {
        section.remove();
        updatePreview();
    });
    
    section.appendChild(removeBtn);
    return section;
}

// Form Validation System
function initializeFormValidation() {
    const form = document.getElementById('resumeForm');
    
    form.addEventListener('submit', function(e) {
        let isValid = true;
        clearValidationErrors();

        // Name validation
        if (!form.elements.name.value.trim()) {
            isValid = false;
            showError(form.elements.name, 'Full name is required');
        }

        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(form.elements.email.value)) {
            isValid = false;
            showError(form.elements.email, 'Valid email is required');
        }

        // LinkedIn validation
        const linkedinRegex = /^(https?:\/\/)?(www\.)?linkedin\.com\/(in|pub)\/[a-zA-Z0-9-]+\/?$/;
        if (form.elements.linkedin.value && !linkedinRegex.test(form.elements.linkedin.value)) {
            isValid = false;
            showError(form.elements.linkedin, 'Invalid LinkedIn URL format');
        }

        if (!isValid) e.preventDefault();
    });
}

function showError(element, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    element.parentNode.appendChild(errorDiv);
    element.classList.add('error');
}

function clearValidationErrors() {
    document.querySelectorAll('.error-message').forEach(e => e.remove());
    document.querySelectorAll('.error').forEach(e => e.classList.remove('error'));
}

// Preview System
const updatePreview = debounce(() => {
    const formData = new FormData(document.getElementById('resumeForm'));
    
    fetch('/resume_builder', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    })
    .then(data => {
        if (data.success) {
            loadPreviewData(data.resume_id);
        }
    })
    .catch(error => {
        console.error('Preview update error:', error);
        showAlert('Failed to update preview', 'error');
    });
}, 500);

function loadPreviewData(resumeId) {
    const template = document.getElementById('templateSelect').value;
    
    fetch(`/get-template-html?template=${template}&resume_id=${resumeId}`)
    .then(response => response.text())
    .then(html => {
        document.getElementById('resumePreview').innerHTML = html;
    })
    .catch(error => {
        console.error('Preview load error:', error);
        document.getElementById('resumePreview').innerHTML = 
            `<div class="preview-error">Preview unavailable</div>`;
    });
}

function updatePreviewSkills(skills, category) {
    const container = document.getElementById(`${category}-skills-preview`);
    container.innerHTML = skills?.map(skill => `
        <span class="skill-tag">
            ${skill}
            <button type="button" onclick="removeSkill('${skill}', '${category}')">&times;</button>
        </span>
    `).join('') || '';
}

// Skill Removal System
function removeSkill(skill, category) {
    const hiddenField = document.getElementById(`hidden${category.charAt(0).toUpperCase() + category.slice(1)}Skills`);
    let skills = JSON.parse(hiddenField.value || '[]');
    skills = skills.filter(s => s !== skill);
    hiddenField.value = JSON.stringify(skills);
    updatePreview();
}

// Export System
function exportPDF() {
    const resumeId = localStorage.getItem('lastResumeId');
    if (resumeId) {
        window.open(`/export-resume/${resumeId}`, '_blank');
    } else {
        showAlert('Please save your resume before exporting', 'warning');
    }
}

// Initialize all components
document.addEventListener('DOMContentLoaded', () => {
    initializeTemplateSelector();
    initializeSkillManagement();
    initializeFormValidation();
    initializeDynamicSections();
    
    // Load initial preview if resume exists
    const resumeId = localStorage.getItem('lastResumeId');
    if (resumeId) {
        loadPreviewData(resumeId);
    }
});
// Utility Functions
function debounce(func, wait) {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

function showAlert(message, type = 'success') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    document.body.appendChild(alert);
    setTimeout(() => alert.remove(), 3000);
}

function handleResponse(response) {
    if (!response.ok) throw new Error('Network response was not ok');
    return response.json();
}

function handleError(error) {
    console.error('Error:', error);
    showAlert('An error occurred. Please try again.', 'error');
}
// Add to resume.js
window.onerror = function(message, source, lineno, colno, error) {
    console.error('Global error:', {message, source, lineno, colno, error});
    showAlert('Application error occurred. Please refresh the page.', 'error');
    return true;
};