// ResumAI Dashboard JavaScript

// Initialize Socket.IO connection
const socket = io();

// State
let currentPhase = 'all-active';
let jobs = [];
let phaseCounts = {};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeWebSocket();
    loadResumes();
    loadJobs();
    startLogPolling();
    setupEventListeners();
    setupFileViewerModal();
    setupJobEditorModal();
});

// WebSocket event handlers
function initializeWebSocket() {
    socket.on('connect', () => {
        console.log('Connected to server');
        showToast('Connected to ResumAI', 'success');
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from server');
        showToast('Disconnected from server', 'warning');
    });

    socket.on('toast', (data) => {
        showToast(data.message, data.level);
    });

    socket.on('job_update', (data) => {
        handleJobUpdate(data);
    });

    socket.on('phase_update', (data) => {
        handlePhaseUpdate(data);
    });
}

// Setup event listeners
function setupEventListeners() {
    // Phase selection
    document.querySelectorAll('#phase-list li').forEach(li => {
        li.addEventListener('click', () => {
            selectPhase(li.dataset.phase);
        });
    });

    // Action buttons
    document.getElementById('fetch-jobs').addEventListener('click', fetchJobsFromEmail);
    document.getElementById('add-url').addEventListener('click', addJobByURL);
    document.getElementById('manual-entry').addEventListener('click', manualEntry);
    document.getElementById('refresh-resumes').addEventListener('click', loadResumes);
    document.getElementById('batch-process').addEventListener('click', batchProcessJobs);
    document.getElementById('copy-logs').addEventListener('click', copyLogsToClipboard);
}

// Phase selection
function selectPhase(phase) {
    currentPhase = phase;
    
    // Update UI
    document.querySelectorAll('#phase-list li').forEach(li => {
        li.classList.remove('active');
    });
    document.querySelector(`#phase-list li[data-phase="${phase}"]`).classList.add('active');
    
    // Update header
    const phaseName = phase.replace(/_/g, ' ').replace(/^\d+/, '').trim() || phase;
    document.getElementById('phase-header').textContent = `Jobs in ${phaseName}`;
    
    // Reload jobs
    loadJobs();
}

// Load resumes
async function loadResumes() {
    try {
        const response = await fetch('/api/resumes');
        const data = await response.json();
        
        const select = document.getElementById('resume-select');
        select.innerHTML = '';
        
        data.resumes.forEach(resume => {
            const option = document.createElement('option');
            option.value = resume;
            option.textContent = resume.replace('.yaml', '');
            if (resume === data.selected) {
                option.selected = true;
            }
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Failed to load resumes:', error);
        showToast('Failed to load resumes', 'error');
    }
}

// Load jobs
async function loadJobs() {
    try {
        console.log('Loading jobs for phase:', currentPhase);
        const response = await fetch(`/api/jobs?phase=${currentPhase}`);
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Received data:', data);
        console.log('Jobs count:', data.jobs ? data.jobs.length : 0);
        
        jobs = data.jobs;
        phaseCounts = data.phase_counts;
        
        renderJobs();
        updatePhaseCounts();
        
        console.log('Jobs loaded successfully');
    } catch (error) {
        console.error('Failed to load jobs:', error);
        console.error('Error stack:', error.stack);
        showToast('Failed to load jobs: ' + error.message, 'error');
    }
}

// Render jobs
function renderJobs() {
    try {
        console.log('Rendering jobs, count:', jobs.length);
        const grid = document.getElementById('jobs-grid');
        
        if (!grid) {
            console.error('jobs-grid element not found!');
            return;
        }
        
        if (jobs.length === 0) {
            grid.innerHTML = '<p class="loading">No jobs found in this phase</p>';
            return;
        }
        
        console.log('Creating job cards...');
        const cards = jobs.map((job, index) => {
            try {
                return createJobCard(job);
            } catch (err) {
                console.error(`Error creating card for job ${index}:`, job, err);
                return `<div class="job-card error">Error loading job: ${job.folder_name || 'unknown'}</div>`;
            }
        });
        
        grid.innerHTML = cards.join('');
        console.log('Job cards created');
        
        // Add event listeners
        addJobCardEventListeners();
        
        // Set up intersection observer for lazy loading job details
        setupLazyLoadJobDetails();
        
        console.log('Jobs rendered successfully');
    } catch (error) {
        console.error('Error in renderJobs:', error);
        console.error('Error stack:', error.stack);
        showToast('Error rendering jobs: ' + error.message, 'error');
    }
}

// Load detailed job information
async function loadJobDetails(jobFolderName) {
    try {
        const response = await fetch(`/api/job/${jobFolderName}`);
        const data = await response.json();
        
        if (data.error) {
            console.error('Error loading job details:', data.error);
            return;
        }
        
        // Update subcontent status for Queued phase
        const subcontentDiv = document.getElementById(`subcontent-${jobFolderName}`);
        if (subcontentDiv) {
            subcontentDiv.innerHTML = createSubcontentStatus(data);
            // Add event listeners to the newly created elements
            attachSubcontentEventListeners(jobFolderName);
        }
        
        // Update doc status for Data Generated phase
        const docStatusDiv = document.getElementById(`docstatus-${jobFolderName}`);
        if (docStatusDiv) {
            docStatusDiv.innerHTML = createDocStatus(data);
        }
        
        // Update doc list for Docs Generated phase
        const docListDiv = document.getElementById(`doclist-${jobFolderName}`);
        if (docListDiv) {
            docListDiv.innerHTML = createDocList(data);
        }
    } catch (error) {
        console.error('Failed to load job details:', error);
    }
}

// Attach event listeners to subcontent elements for a specific job
function attachSubcontentEventListeners(jobFolderName) {
    const container = document.getElementById(`subcontent-${jobFolderName}`);
    if (!container) return;
    
    // Subcontent name click (open file for editing)
    container.querySelectorAll('.subcontent-name.clickable').forEach(name => {
        name.addEventListener('click', (e) => {
            e.stopPropagation();
            const jobFolderName = name.dataset.job;
            const fileName = name.dataset.file;
            viewFile(jobFolderName, fileName);
        });
    });
    
    // Subcontent type toggle (⚙️ ↔ 🧠)
    container.querySelectorAll('.subcontent-type-icon').forEach(icon => {
        icon.addEventListener('click', async (e) => {
            e.stopPropagation();
            const jobFolderName = icon.dataset.job;
            const section = icon.dataset.section;
            await toggleGeneration(jobFolderName, section);
        });
    });
    
    // Subcontent play/generate icon (▶️ → ✅)
    container.querySelectorAll('.subcontent-play-icon').forEach(icon => {
        icon.addEventListener('click', async (e) => {
            e.stopPropagation();
            const jobFolderName = icon.dataset.job;
            const section = icon.dataset.section;
            await generateSection(jobFolderName, section);
        });
    });
}

// Create subcontent status HTML
function createSubcontentStatus(data) {
    // Order: contacts, summary, skills, highlights, experience, education, awards, coverletter
    // Display in 2 columns, 4 rows:
    // contacts      | experience
    // summary       | education
    // skills        | awards
    // highlights    | coverletter
    const sections = ['contacts', 'experience', 'summary', 'education', 'skills', 'awards', 'highlights', 'coverletter'];
    let html = '<div class="subcontent-grid">';
    
    sections.forEach(section => {
        const status = data.subcontent_status[section];
        const event = data.subcontent_events[section] || `gen_static_subcontent_${section}`;
        const isLLM = event.includes('llm');
        const exists = status.exists;
        
        // Play icon (▶️) if not generated, checkmark (✅) if generated
        const playIcon = exists ? '✅' : '▶️';
        
        html += `
            <div class="subcontent-item">
                <span class="subcontent-play-icon clickable" 
                      data-job="${data.job.folder_name}" 
                      data-section="${section}"
                      title="Click to generate ${section}">
                    ${playIcon}
                </span>
                <span class="subcontent-type-icon clickable" 
                      data-job="${data.job.folder_name}" 
                      data-section="${section}"
                      title="Click to toggle LLM/Static">
                    ${isLLM ? '🧠' : '⚙️'}
                </span>
                <span class="subcontent-name clickable" 
                      data-job="${data.job.folder_name}" 
                      data-file="subcontent.${section}.yaml"
                      title="Click to edit ${section}">
                    ${section}
                </span>
            </div>
        `;
    });
    
    html += '</div>';
    return html;
}

// Create doc status HTML
function createDocStatus(data) {
    const docs = [
        { name: 'resume.html', key: 'resume_html', locked: false },
        { name: 'coverletter.html', key: 'coverletter_html', locked: false },
        { name: 'resume.pdf', key: 'resume_pdf', locked: !data.doc_status.resume_html },
        { name: 'coverletter.pdf', key: 'coverletter_pdf', locked: !data.doc_status.coverletter_html }
    ];
    
    let html = '<div class="doc-status-grid">';
    
    docs.forEach(doc => {
        const exists = data.doc_status[doc.key];
        // ✅ = exists, ▶️ = ready to generate, 🔒 = locked (waiting on HTML)
        const icon = doc.locked ? '🔒' : (exists ? '✅' : '▶️');
        const clickable = !doc.locked && !exists ? 'clickable' : '';
        const title = doc.locked ? 'Generate HTML first' : (exists ? 'Click to view' : 'Click to generate');
        
        html += `
            <div class="doc-status-item ${clickable}" data-job="${data.job.folder_name}" data-doc="${doc.key}" title="${title}">
                <span class="doc-name">${doc.name}</span>
                <span class="doc-icon">${icon}</span>
            </div>
        `;
    });
    
    html += '</div>';
    
    // Add error.md link if exists
    if (data.doc_status.error_md) {
        html += `
            <div class="file-links-row error-row">
                <span class="file-link-item error">
                    <span>⚠️</span>
                    <a href="#" class="file-link" data-job="${data.job.folder_name}" data-file="error.md">Error.md</a>
                </span>
            </div>
        `;
    }
    
    return html;
}

// Create doc list HTML
function createDocList(data) {
    let html = '<div class="doc-list-grid">';
    
    const docs = [
        { key: 'resume_html', label: 'Resume HTML', icon: '📄' },
        { key: 'coverletter_html', label: 'Cover Letter HTML', icon: '📄' },
        { key: 'resume_pdf', label: 'Resume PDF', icon: '📕' },
        { key: 'coverletter_pdf', label: 'Cover Letter PDF', icon: '📕' }
    ];
    
    docs.forEach(doc => {
        const exists = data.doc_status[doc.key];
        html += `
            <div class="doc-list-item ${exists ? 'exists' : 'missing'}">
                <span>${doc.icon} ${doc.label}</span>
                <span>${exists ? '✅' : '❌'}</span>
            </div>
        `;
    });
    
    if (data.doc_status.error_md) {
        html += `
            <div class="doc-list-item error">
                <span>⚠️ Error.md</span>
                <a href="#" class="file-link" data-job="${data.job.folder_name}" data-file="error.md">View</a>
            </div>
        `;
    }
    
    html += '</div>';
    return html;
}

// Add event listeners to job cards
function addJobCardEventListeners() {
    // Generate data buttons
    document.querySelectorAll('.btn-generate-data').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.stopPropagation();
            const jobFolderName = btn.dataset.job;
            await generateData(jobFolderName);
        });
    });
    
    // Generate docs buttons
    document.querySelectorAll('.btn-generate-docs').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.stopPropagation();
            const jobFolderName = btn.dataset.job;
            await generateDocs(jobFolderName);
        });
    });
    
    // Skip buttons
    document.querySelectorAll('.btn-skip').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.stopPropagation();
            const jobFolderName = btn.dataset.job;
            await moveToPhase(jobFolderName, 'Skipped');
        });
    });
    
    // Move to dropdown
    document.querySelectorAll('.move-to-dropdown').forEach(select => {
        select.addEventListener('change', async (e) => {
            e.stopPropagation();
            const jobFolderName = select.dataset.job;
            const targetPhase = select.value;
            if (targetPhase) {
                await moveToPhase(jobFolderName, targetPhase);
                select.value = ''; // Reset dropdown
            }
        });
    });
    
    // File links
    document.querySelectorAll('.file-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            const jobFolderName = link.dataset.job;
            const fileName = link.dataset.file;
            viewFile(jobFolderName, fileName);
        });
    });
    
    // Company name click (open job editor)
    document.querySelectorAll('.job-company').forEach(company => {
        company.addEventListener('click', (e) => {
            e.stopPropagation();
            const card = company.closest('.job-card');
            const jobFolderName = card.dataset.job;
            console.log('Company clicked! Job folder:', jobFolderName);
            openJobEditor(jobFolderName);
        });
    });
    
    // Job card click (for future detail view)
    document.querySelectorAll('.job-card').forEach(card => {
        card.addEventListener('click', () => {
            const jobFolderName = card.dataset.job;
            console.log('Job card clicked:', jobFolderName);
            // TODO: Open job detail modal
        });
    });
}

// Create job card HTML
function createJobCard(job) {
    const phase = job.phase;
    
    // Ensure tags is an array
    const tags = Array.isArray(job.tags) ? job.tags : [];
    
    // Base card structure
    let cardHTML = `
        <div class="job-card" data-job="${job.folder_name}" data-phase="${phase}">
            <h3 class="job-company">${job.company || 'Unknown Company'}</h3>
            <p class="job-title">${job.title || 'Unknown Title'}</p>
            <p class="job-meta">
                <span>📅 ${job.date || 'Unknown Date'}</span>
                ${job.location ? `<span>📍 ${job.location}</span>` : ''}
                ${job.salary ? `<span>💰 ${job.salary}</span>` : ''}
            </p>
            ${job.source ? `<p class="job-source">Source: <a href="${job.url || '#'}" target="_blank">${job.source}</a></p>` : ''}
            ${tags.length > 0 ? `<p class="job-tags">${tags.map(t => `<span class="tag">${t}</span>`).join(' ')}</p>` : ''}
    `;
    
    // Phase-specific content
    if (phase === '1_Queued') {
        cardHTML += createQueuedPhaseContent(job);
    } else if (phase === '2_Data_Generated') {
        cardHTML += createDataGeneratedPhaseContent(job);
    } else {
        cardHTML += createDocsGeneratedPhaseContent(job);
    }
    
    // Common footer
    cardHTML += `
            <div class="job-footer">
                <span class="job-phase-badge">${phase.replace(/_/g, ' ')}</span>
                <select class="move-to-dropdown" data-job="${job.folder_name}">
                    <option value="">Move to...</option>
                    <option value="1_Queued">Queued</option>
                    <option value="2_Data_Generated">Data Generated</option>
                    <option value="3_Docs_Generated">Docs Generated</option>
                    <option value="4_Applied">Applied</option>
                    <option value="5_FollowUp">Follow Up</option>
                    <option value="6_Interviewing">Interviewing</option>
                    <option value="7_Negotiating">Negotiating</option>
                    <option value="8_Accepted">Accepted</option>
                    <option value="Skipped">Skipped</option>
                    <option value="Expired">Expired</option>
                    <option value="Errored">Errored</option>
                </select>
                <span class="file-count">📁 ${job.file_count || 0} files</span>
            </div>
        </div>
    `;
    
    return cardHTML;
}

// Create content for Queued phase
function createQueuedPhaseContent(job) {
    return `
        <div class="phase-content queued-content">
            <p class="section-title">Section Generation</p>
            <div class="subcontent-status" id="subcontent-${job.folder_name}">
                <p class="loading-text">Loading status...</p>
            </div>
            <div class="action-buttons">
                <button class="btn-generate-data" data-job="${job.folder_name}">
                    🚀 Generate Resume Data
                </button>
                <button class="btn-skip" data-job="${job.folder_name}">
                    ⏭️ Skip this Job
                </button>
            </div>
        </div>
    `;
}

// Create content for Data Generated phase
function createDataGeneratedPhaseContent(job) {
    return `
        <div class="phase-content data-generated-content">
            <p class="section-title">Subcontent Generation</p>
            <div class="subcontent-status" id="subcontent-${job.folder_name}">
                <p class="loading-text">Loading status...</p>
            </div>
            <div class="file-links-row" id="filelinks-${job.folder_name}">
                <span class="file-link-item">
                    <span>✅</span>
                    <a href="#" class="file-link" data-job="${job.folder_name}" data-file="job.yaml">job.yaml</a>
                </span>
                <span class="file-link-item">
                    <span>✅</span>
                    <a href="#" class="file-link" data-job="${job.folder_name}" data-file="job.log">job.log</a>
                </span>
            </div>
            <p class="section-title">Next Steps: Generate Final Documents</p>
            <div class="doc-status" id="docstatus-${job.folder_name}">
                <p class="loading-text">Loading status...</p>
            </div>
            <div class="action-buttons">
                <button class="btn-generate-docs" data-job="${job.folder_name}">
                    📄 Generate All Resume Docs
                </button>
            </div>
        </div>
    `;
}

// Create content for Docs Generated and higher phases
function createDocsGeneratedPhaseContent(job) {
    return `
        <div class="phase-content docs-generated-content">
            <p class="section-title">Documents</p>
            <div class="doc-list" id="doclist-${job.folder_name}">
                <p class="loading-text">Loading documents...</p>
            </div>
            <div class="file-links">
                <a href="#" class="file-link" data-job="${job.folder_name}" data-file="resume.pdf">📄 View Resume PDF</a>
                <a href="#" class="file-link" data-job="${job.folder_name}" data-file="coverletter.pdf">📄 View Cover Letter PDF</a>
                <a href="#" class="file-link" data-job="${job.folder_name}" data-file="job.log">📋 View job.log</a>
            </div>
        </div>
    `;
}

// Update phase counts
function updatePhaseCounts() {
    Object.entries(phaseCounts).forEach(([phase, count]) => {
        const li = document.querySelector(`#phase-list li[data-phase="${phase}"]`);
        if (li) {
            li.querySelector('.count').textContent = count;
        }
    });
}

// Handle job update from WebSocket
function handleJobUpdate(data) {
    console.log('Job update:', data);
    loadJobs(); // Reload jobs to reflect changes
}

// Handle phase update from WebSocket
function handlePhaseUpdate(data) {
    console.log('Phase update:', data);
    phaseCounts[data.phase] = data.count;
    updatePhaseCounts();
}

// Start log polling
function startLogPolling() {
    updateLogs();
    setInterval(updateLogs, 1000); // Poll every second
}

// Update logs
async function updateLogs() {
    try {
        const response = await fetch('/api/logs');
        const data = await response.json();
        
        const logsContent = document.getElementById('logs-content');
        
        // Split into lines and keep only last 50
        const lines = data.logs.split('\n');
        const last50Lines = lines.slice(-50).join('\n');
        
        logsContent.textContent = last50Lines;
        
        // Auto-scroll to bottom
        logsContent.scrollTop = logsContent.scrollHeight;
    } catch (error) {
        console.error('Failed to load logs:', error);
    }
}

// Action handlers
async function fetchJobsFromEmail() {
    showToast('Fetching jobs from email...', 'info');
    try {
        const response = await fetch('/api/fetch_email', { method: 'POST' });
        const data = await response.json();
        showToast(data.message, data.ok ? 'success' : 'error');
        if (data.ok) {
            loadJobs();
        }
    } catch (error) {
        console.error('Failed to fetch jobs:', error);
        showToast('Failed to fetch jobs from email', 'error');
    }
}

function addJobByURL() {
    const url = prompt('Enter job URL:');
    if (!url) return;
    
    showToast('Adding job from URL...', 'info');
    fetch('/api/add_url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
    })
    .then(response => response.json())
    .then(data => {
        showToast(data.message, data.ok ? 'success' : 'error');
        if (data.ok) {
            loadJobs();
        }
    })
    .catch(error => {
        console.error('Failed to add job:', error);
        showToast('Failed to add job from URL', 'error');
    });
}

function manualEntry() {
    showToast('Manual entry not yet implemented', 'info');
}

async function generateData(jobFolderName) {
    showToast('Generating resume data...', 'info');
    try {
        const response = await fetch('/api/generate_data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ job_folder_name: jobFolderName })
        });
        const data = await response.json();
        showToast(data.message, data.ok ? 'success' : 'error');
        if (data.ok) {
            setTimeout(() => loadJobs(), 1000);
        }
    } catch (error) {
        console.error('Failed to generate data:', error);
        showToast('Failed to generate resume data', 'error');
    }
}

async function generateDocs(jobFolderName) {
    showToast('Generating documents...', 'info');
    try {
        const response = await fetch('/api/generate_docs', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ job_folder_name: jobFolderName })
        });
        const data = await response.json();
        showToast(data.message, data.ok ? 'success' : 'error');
        if (data.ok) {
            setTimeout(() => loadJobs(), 1000);
        }
    } catch (error) {
        console.error('Failed to generate docs:', error);
        showToast('Failed to generate documents', 'error');
    }
}

async function moveToPhase(jobFolderName, targetPhase) {
    showToast(`Moving job to ${targetPhase}...`, 'info');
    try {
        const response = await fetch('/api/move_phase', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                job_folder_name: jobFolderName,
                target_phase: targetPhase
            })
        });
        const data = await response.json();
        showToast(data.message, data.ok ? 'success' : 'error');
        if (data.ok) {
            setTimeout(() => loadJobs(), 500);
        }
    } catch (error) {
        console.error('Failed to move job:', error);
        showToast('Failed to move job', 'error');
    }
}

async function toggleGeneration(jobFolderName, section) {
    try {
        const response = await fetch('/api/toggle_generation', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                job_folder_name: jobFolderName,
                section: section
            })
        });
        const data = await response.json();
        showToast(data.message, data.ok ? 'success' : 'info');
        if (data.ok) {
            // Reload job details to update icons
            loadJobDetails(jobFolderName);
        }
    } catch (error) {
        console.error('Failed to toggle generation:', error);
        showToast('Failed to toggle generation type', 'error');
    }
}

async function generateSection(jobFolderName, section) {
    showToast(`Generating ${section}...`, 'info');
    try {
        const response = await fetch('/api/generate_section', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                job_folder_name: jobFolderName,
                section: section
            })
        });
        const data = await response.json();
        showToast(data.message, data.ok ? 'success' : 'error');
        if (data.ok) {
            // Reload job details to update icons
            setTimeout(() => loadJobDetails(jobFolderName), 500);
        }
    } catch (error) {
        console.error('Failed to generate section:', error);
        showToast(`Failed to generate ${section}`, 'error');
    }
}

function viewFile(jobFolderName, fileName) {
    // Open the file viewer modal
    openFileViewer(jobFolderName, fileName);
}

// File viewer modal state
let currentFileData = {
    jobFolderName: null,
    fileName: null,
    originalContent: null
};

function setupFileViewerModal() {
    const modal = document.getElementById('file-viewer-modal');
    const closeBtn = document.getElementById('modal-close');
    const cancelBtn = document.getElementById('modal-cancel');
    const saveBtn = document.getElementById('modal-save');
    
    // Close modal handlers
    closeBtn.addEventListener('click', closeFileViewer);
    cancelBtn.addEventListener('click', closeFileViewer);
    
    // Click outside modal to close
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeFileViewer();
        }
    });
    
    // Save button
    saveBtn.addEventListener('click', saveFileContent);
    
    // ESC key to close
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('show')) {
            closeFileViewer();
        }
    });
}

async function openFileViewer(jobFolderName, fileName) {
    try {
        showToast(`Loading ${fileName}...`, 'info');
        
        const response = await fetch(`/api/file/${jobFolderName}/${fileName}`);
        const data = await response.json();
        
        if (!data.ok) {
            showToast(data.message, 'error');
            return;
        }
        
        // Store current file data
        currentFileData = {
            jobFolderName: jobFolderName,
            fileName: fileName,
            originalContent: data.content
        };
        
        // Update modal content
        document.getElementById('modal-filename').textContent = fileName;
        document.getElementById('file-content').value = data.content;
        
        // Show modal
        const modal = document.getElementById('file-viewer-modal');
        modal.classList.add('show');
        
        // Focus on textarea
        document.getElementById('file-content').focus();
        
    } catch (error) {
        console.error('Failed to load file:', error);
        showToast('Failed to load file', 'error');
    }
}

function closeFileViewer() {
    const modal = document.getElementById('file-viewer-modal');
    const content = document.getElementById('file-content').value;
    
    // Check if content changed
    if (content !== currentFileData.originalContent) {
        if (!confirm('You have unsaved changes. Are you sure you want to close?')) {
            return;
        }
    }
    
    modal.classList.remove('show');
    currentFileData = {
        jobFolderName: null,
        fileName: null,
        originalContent: null
    };
}

async function saveFileContent() {
    try {
        const content = document.getElementById('file-content').value;
        
        showToast('Saving file...', 'info');
        
        const response = await fetch(`/api/file/${currentFileData.jobFolderName}/${currentFileData.fileName}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content: content })
        });
        
        const data = await response.json();
        
        if (data.ok) {
            showToast(data.message, 'success');
            currentFileData.originalContent = content; // Update to prevent unsaved changes warning
            closeFileViewer();
            // Reload job details to reflect changes
            loadJobDetails(currentFileData.jobFolderName);
        } else {
            showToast(data.message, 'error');
        }
    } catch (error) {
        console.error('Failed to save file:', error);
        showToast('Failed to save file', 'error');
    }
}

async function batchProcessJobs() {
    const batchBtn = document.getElementById('batch-process');
    batchBtn.disabled = true;
    batchBtn.textContent = '⏳ Processing...';
    
    showToast('Starting batch processing...', 'info');
    
    try {
        const response = await fetch('/api/batch_process', { method: 'POST' });
        const data = await response.json();
        
        if (data.ok) {
            showToast(data.message, 'success');
            // Reload jobs to show updated status
            setTimeout(() => loadJobs(), 1000);
        } else {
            showToast(data.message, 'error');
        }
    } catch (error) {
        console.error('Batch processing failed:', error);
        showToast('Batch processing failed', 'error');
    } finally {
        batchBtn.disabled = false;
        batchBtn.textContent = '⚡ Process All Jobs in Queue';
    }
}

// Toast notifications
function showToast(message, level = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${level}`;
    toast.textContent = message;
    
    container.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// Copy logs to clipboard
async function copyLogsToClipboard() {
    const logsContent = document.getElementById('logs-content');
    const logsText = logsContent.textContent;
    
    try {
        await navigator.clipboard.writeText(logsText);
        showToast('Logs copied to clipboard', 'success');
    } catch (error) {
        console.error('Failed to copy logs:', error);
        showToast('Failed to copy logs to clipboard', 'error');
    }
}

// Job editor modal state
let currentJobData = {
    jobFolderName: null,
    originalData: null
};

function setupJobEditorModal() {
    const modal = document.getElementById('job-editor-modal');
    const closeBtn = document.getElementById('job-modal-close');
    const cancelBtn = document.getElementById('job-modal-cancel');
    const saveBtn = document.getElementById('job-modal-save');
    
    // Close modal handlers
    closeBtn.addEventListener('click', closeJobEditor);
    cancelBtn.addEventListener('click', closeJobEditor);
    
    // Click outside modal to close
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeJobEditor();
        }
    });
    
    // Save button
    saveBtn.addEventListener('click', saveJobData);
    
    // ESC key to close
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('show')) {
            closeJobEditor();
        }
    });
}

async function openJobEditor(jobFolderName) {
    try {
        showToast('Loading job details...', 'info');
        
        // Verify modal elements exist
        const modal = document.getElementById('job-editor-modal');
        if (!modal) {
            console.error('Job editor modal not found in DOM');
            showToast('Job editor not initialized', 'error');
            return;
        }
        
        // Fetch job details
        const response = await fetch(`/api/job/${jobFolderName}`);
        
        console.log('Job editor response status:', response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Job editor fetch failed:', response.status, errorText);
            showToast(`Failed to load job details: ${response.status}`, 'error');
            return;
        }
        
        const data = await response.json();
        console.log('Job editor data:', data);
        
        // Check for error response
        if (data.error) {
            console.error('Job editor error:', data.error);
            showToast(data.error, 'error');
            return;
        }
        
        // Check if we got job data
        if (!data.job) {
            console.error('No job data in response:', data);
            showToast('No job data received', 'error');
            return;
        }
        
        const jobData = data.job;
        console.log('Job data loaded successfully:', jobData);
        
        // Store current job data
        currentJobData = {
            jobFolderName: jobFolderName,
            originalData: JSON.parse(JSON.stringify(jobData))
        };
        
        // Populate form fields - check each element exists
        const fields = {
            'job-company': jobData.company || '',
            'job-title': jobData.title || '',
            'job-id': jobData.id || '',
            'job-date': jobData.date || '',
            'job-url': jobData.url || '',
            'job-location': jobData.location || '',
            'job-salary': jobData.salary || '',
            'job-source': jobData.source || '',
            'job-description': jobData.description || ''
        };
        
        for (const [fieldId, value] of Object.entries(fields)) {
            const element = document.getElementById(fieldId);
            if (!element) {
                console.error(`Form field not found: ${fieldId}`);
                showToast(`Form field missing: ${fieldId}`, 'error');
                return;
            }
            element.value = value;
        }
        
        // Handle tags (array to comma-separated string)
        const tagsElement = document.getElementById('job-tags');
        if (!tagsElement) {
            console.error('Tags field not found');
            showToast('Tags field missing', 'error');
            return;
        }
        const tags = jobData.tags || [];
        tagsElement.value = tags.join(', ');
        
        // Update modal title
        document.getElementById('job-modal-title').textContent = `Edit Job: ${jobData.company}`;
        
        // Show modal
        modal.classList.add('show');
        
        // Focus on first field
        document.getElementById('job-company').focus();
        
    } catch (error) {
        console.error('Failed to load job details - exception:', error);
        showToast(`Failed to load job details: ${error.message}`, 'error');
    }
}

function closeJobEditor() {
    const modal = document.getElementById('job-editor-modal');
    
    // Check if form has changes
    if (hasJobFormChanges()) {
        if (!confirm('You have unsaved changes. Are you sure you want to close?')) {
            return;
        }
    }
    
    modal.classList.remove('show');
    currentJobData = {
        jobFolderName: null,
        originalData: null
    };
}

function hasJobFormChanges() {
    if (!currentJobData.originalData) return false;
    
    const original = currentJobData.originalData;
    
    // Compare form values with original data
    if (document.getElementById('job-company').value !== (original.company || '')) return true;
    if (document.getElementById('job-title').value !== (original.title || '')) return true;
    if (document.getElementById('job-id').value !== (original.id || '')) return true;
    if (document.getElementById('job-date').value !== (original.date || '')) return true;
    if (document.getElementById('job-url').value !== (original.url || '')) return true;
    if (document.getElementById('job-location').value !== (original.location || '')) return true;
    if (document.getElementById('job-salary').value !== (original.salary || '')) return true;
    if (document.getElementById('job-source').value !== (original.source || '')) return true;
    if (document.getElementById('job-description').value !== (original.description || '')) return true;
    
    // Compare tags
    const originalTags = (original.tags || []).join(', ');
    const currentTags = document.getElementById('job-tags').value;
    if (currentTags !== originalTags) return true;
    
    return false;
}

async function saveJobData() {
    try {
        // Validate required fields
        const form = document.getElementById('job-editor-form');
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }
        
        showToast('Saving job details...', 'info');
        
        // Collect form data
        const jobData = {
            company: document.getElementById('job-company').value,
            title: document.getElementById('job-title').value,
            id: document.getElementById('job-id').value,
            date: document.getElementById('job-date').value,
            url: document.getElementById('job-url').value,
            location: document.getElementById('job-location').value,
            salary: document.getElementById('job-salary').value,
            source: document.getElementById('job-source').value,
            description: document.getElementById('job-description').value,
            // Parse tags from comma-separated string
            tags: document.getElementById('job-tags').value
                .split(',')
                .map(t => t.trim())
                .filter(t => t.length > 0),
            // Preserve subcontent_events from original data
            subcontent_events: currentJobData.originalData.subcontent_events || []
        };
        
        // Save via API
        const response = await fetch(`/api/job/${currentJobData.jobFolderName}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(jobData)
        });
        
        const result = await response.json();
        
        if (result.ok) {
            showToast('Job details saved successfully', 'success');
            currentJobData.originalData = jobData; // Update to prevent unsaved changes warning
            closeJobEditor();
            // Reload jobs to reflect changes
            loadJobs();
        } else {
            showToast(result.message || 'Failed to save job details', 'error');
        }
    } catch (error) {
        console.error('Failed to save job details:', error);
        showToast('Failed to save job details', 'error');
    }
}

// Lazy load job details using Intersection Observer
let jobDetailsObserver = null;
const loadedJobDetails = new Set();

function setupLazyLoadJobDetails() {
    // Disconnect previous observer if exists
    if (jobDetailsObserver) {
        jobDetailsObserver.disconnect();
    }
    
    // Clear loaded set when switching phases
    loadedJobDetails.clear();
    
    // Create intersection observer
    jobDetailsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const card = entry.target;
                const jobFolderName = card.dataset.job;
                
                // Only load once
                if (!loadedJobDetails.has(jobFolderName)) {
                    loadedJobDetails.add(jobFolderName);
                    loadJobDetails(jobFolderName);
                }
            }
        });
    }, {
        root: null,
        rootMargin: '50px', // Start loading 50px before card is visible
        threshold: 0.01
    });
    
    // Observe all job cards
    document.querySelectorAll('.job-card').forEach(card => {
        jobDetailsObserver.observe(card);
    });
}
