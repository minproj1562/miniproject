let skills = {{ resume.get('skills', [])|tojson|safe }};
let photoPreview = document.getElementById('previewPhoto');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and JavaScript running');
    updatePreview();
    updateTemplatePreview(); // Initial template load
    const skillInput = document.getElementById('skillInput');
    const suggestionsDiv = document.getElementById('suggestions');
    const selectedSkillsDiv = document.getElementById('selectedSkills');
    const hiddenSkills = document.getElementById('hiddenSkills');

    document.querySelector('[name="photo"]').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                photoPreview.src = e.target.result;
                photoPreview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
        updatePreview();
    });

    document.querySelectorAll('input, textarea').forEach(element => {
        element.addEventListener('input', updatePreview);
    });

    let timeout;
    skillInput.addEventListener('input', function(e) {
        clearTimeout(timeout);
        timeout = setTimeout(async () => {
            const value = e.target.value.trim();
            if (value.length < 2) {
                suggestionsDiv.innerHTML = '';
                return;
            }
            const response = await fetch(`/api/career-suggestions?skills=${encodeURIComponent(value)}`);
            const suggestions = await response.json();
            suggestionsDiv.innerHTML = suggestions.map(skill => `
                <div class="suggestion-item" onclick="addSkill('${skill}')">${skill}</div>
            `).join('');
        }, 300);
    });

    skillInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && skillInput.value.trim()) {
            e.preventDefault();
            addSkill(skillInput.value.trim());
        }
    });

    document.getElementById('resumeForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        hiddenSkills.value = JSON.stringify(skills);
        const formData = new FormData(this);
        const response = await fetch(this.action, {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        if (result.success) {
            alert('Resume saved successfully!');
            window.location.href = `/export-resume/${result.resume_id}`;
        } else {
            alert('Failed to save resume.');
        }
    });

    updateSkillsDisplay();
});

function addEducation() {
    const fields = document.getElementById('educationFields');
    const newEdu = document.createElement('div');
    newEdu.className = 'dynamic-section mt-2';
    newEdu.innerHTML = `
        <input type="text" class="form-control" name="education[]" placeholder="Degree" required onchange="updatePreview()">
        <input type="text" class="form-control" name="institution[]" placeholder="Institution" required onchange="updatePreview()">
        <input type="month" class="form-control" name="education_date[]" onchange="updatePreview()">
        <button type="button" class="btn btn-sm btn-danger mt-2" onclick="this.parentElement.remove(); updatePreview()">Remove</button>
    `;
    fields.appendChild(newEdu);
}

function addExperience() {
    const fields = document.getElementById('experienceFields');
    const newExp = document.createElement('div');
    newExp.className = 'dynamic-section mt-2';
    newExp.innerHTML = `
        <input type="text" class="form-control" name="position[]" placeholder="Position" required onchange="updatePreview()">
        <input type="text" class="form-control" name="company[]" placeholder="Company" onchange="updatePreview()">
        <textarea class="form-control" name="description[]" placeholder="Job Description" onchange="updatePreview()"></textarea>
        <input type="month" class="form-control" name="experience_date[]" onchange="updatePreview()">
        <button type="button" class="btn btn-sm btn-danger mt-2" onclick="this.parentElement.remove(); updatePreview()">Remove</button>
    `;
    fields.appendChild(newExp);
}

function addSkill(skill) {
    if (!skill || skills.includes(skill)) return;
    skills.push(skill);
    updateSkillsDisplay();
    document.getElementById('skillInput').value = '';
    document.getElementById('suggestions').innerHTML = '';
    updatePreview();
}

function removeSkill(skill) {
    skills = skills.filter(s => s !== skill);
    updateSkillsDisplay();
    updatePreview();
}

function updateSkillsDisplay() {
    document.getElementById('selectedSkills').innerHTML = skills.map(skill => `
        <span class="skill-tag">${skill} <button type="button" onclick="removeSkill('${skill}'); updatePreview()">×</button></span>
    `).join('');
}

function updatePreview() {
    const name = document.querySelector('[name="name"]').value || '{{ resume.get('personal_info', {}).get('name', 'Your Name') }}';
    const email = document.querySelector('[name="email"]').value || '{{ resume.get('personal_info', {}).get('email', 'your.email@example.com') }}';
    const phone = document.querySelector('[name="phone"]').value || '{{ resume.get('personal_info', {}).get('phone', '(123) 456-7890') }}';
    const linkedin = document.querySelector('[name="linkedin"]').value || '{{ resume.get('personal_info', {}).get('linkedin', 'linkedin.com/in/yourprofile') }}';
    const summary = document.querySelector('[name="summary"]').value || '{{ resume.get('summary', 'Your professional summary will appear here.') }}';

    document.getElementById('previewName').textContent = name;
    document.getElementById('previewEmail').textContent = `Email: ${email}`;
    document.getElementById('previewPhone').textContent = `Phone: ${phone}`;
    document.getElementById('previewLinkedIn').textContent = `LinkedIn: ${linkedin}`;
    document.getElementById('previewSummary').textContent = summary;

    const eduPreview = document.getElementById('previewEducation');
    eduPreview.innerHTML = '<h3>Education</h3>' + Array.from(document.querySelectorAll('#educationFields .dynamic-section'))
        .map(section => {
            const degree = section.querySelector('[name="education[]"]').value;
            const institution = section.querySelector('[name="institution[]"]').value;
            const date = section.querySelector('[name="education_date[]"]').value;
            return degree && institution ? `
                <div class="education-item">
                    <h4>${degree}</h4>
                    <p>${institution} - ${date || ''}</p>
                </div>
            ` : '';
        }).join('');

    const expPreview = document.getElementById('previewExperience');
    expPreview.innerHTML = '<h3>Experience</h3>' + Array.from(document.querySelectorAll('#experienceFields .dynamic-section'))
        .map(section => {
            const position = section.querySelector('[name="position[]"]').value;
            const company = section.querySelector('[name="company[]"]').value;
            const desc = section.querySelector('[name="description[]"]').value;
            const date = section.querySelector('[name="experience_date[]"]').value;
            return position ? `
                <div class="experience-item">
                    <h4>${position}</h4>
                    <p>${company || ''} - ${date || ''}</p>
                    <p>${desc || ''}</p>
                </div>
            ` : '';
        }).join('');

    document.getElementById('previewSkills').innerHTML = '<h3>Skills</h3>' + skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('');
    updateTemplatePreview(); // Sync template with content changes
}

async function updateTemplatePreview() {
    const templateSelect = document.getElementById('templateSelect');
    const currentTemplate = templateSelect.value;
    document.getElementById('currentTemplate').value = currentTemplate;

    // Fetch the template HTML
    const response = await fetch(`/get-template-html?template=${currentTemplate}`);
    const templateHtml = await response.text();

    // Inject the template HTML into the preview
    const parser = new DOMParser();
    const doc = parser.parseFromString(templateHtml, 'text/html');
    const resumeContainer = doc.querySelector('.resume-container');
    const preview = document.getElementById('resumePreview');

    // Preserve dynamic content
    const photo = preview.querySelector('#previewPhoto');
    const name = preview.querySelector('#previewName');
    const contactInfo = preview.querySelector('.contact-info');
    const summary = preview.querySelector('#previewSummary');
    const education = preview.querySelector('#previewEducation');
    const experience = preview.querySelector('#previewExperience');
    const skills = preview.querySelector('#previewSkills');

    // Replace preview content with template structure
    preview.innerHTML = resumeContainer ? resumeContainer.innerHTML : templateHtml;
    preview.querySelector('.photo-preview').appendChild(photo);
    preview.querySelector('h1').replaceWith(name);
    preview.querySelector('.contact-info').replaceWith(contactInfo);
    preview.querySelector('.summary-preview p').replaceWith(summary);
    preview.querySelector('#previewEducation').replaceWith(education);
    preview.querySelector('#previewExperience').replaceWith(experience);
    preview.querySelector('#previewSkills').replaceWith(skills);

    // Apply template-specific styles (simplified approach)
    const style = doc.querySelector('style').textContent;
    const styleElement = document.createElement('style');
    styleElement.textContent = style;
    preview.appendChild(styleElement);
}

async function exportPDF() {
    document.getElementById('hiddenSkills').value = JSON.stringify(skills);
    const formData = new FormData(document.getElementById('resumeForm'));
    const response = await fetch('/resume', {
        method: 'POST',
        body: formData
    });
    const result = await response.json();
    if (result.success) {
        window.location.href = `/export-resume/${result.resume_id}`;
    } else {
        alert('Failed to generate PDF.');
    }
}