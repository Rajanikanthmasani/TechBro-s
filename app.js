/**
 * Modern Mestri - Professional Application Logic (Powerplay Edition)
 */

// API Configuration
const getBaseURL = () => {
    // Robust backend detection: Always assume localhost:5000 for this local setup
    return 'http://localhost:5000/api';
};

const API_BASE_URL = getBaseURL();

// Global Namespace for script interoperability (Ensure this only runs once)
if (!window.ModernMestri) {
    window.ModernMestri = {
        API_BASE_URL: API_BASE_URL
    };
}

// Global state
window.currentPlan = null;
window.currentProject = null;

// DOM Elements (Populated on Init)
let elements = {};

// ========================================
// Initialization
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    // Populate elements
    elements = {
        hero: document.getElementById('hero'),
        resultsSection: document.getElementById('resultsSection'),
        form: document.getElementById('constructionForm'),
        generateBtn: document.getElementById('generateBtn'),
        resetBtn: document.getElementById('resetBtn'),
        headerCta: document.getElementById('startBtnHeader'),
        projectSummary: document.getElementById('projectSummary'),
        aiAnalysis: document.getElementById('aiAnalysis'),
        costDetails: document.getElementById('costDetails'),
        materialDetails: document.getElementById('materialDetails'),
        scheduleDetails: document.getElementById('scheduleDetails'),
        workforceDetails: document.getElementById('workforceDetails'),
        blueprintDisplay: document.getElementById('blueprintDisplay'),
        loadingOverlay: document.getElementById('loadingOverlay'),
        loadingMsg: document.getElementById('loadingMsg'),
        aiStatusBadge: document.getElementById('aiStatusBadge')
    };

    setupEventListeners();
    checkAIStatus();

    // Regular check
    setInterval(checkAIStatus, 10000);
});

async function checkAIStatus() {
    try {
        const response = await fetch(`${window.ModernMestri.API_BASE_URL}/health`);
        const data = await response.json();

        const badge = elements.aiStatusBadge;
        const text = badge.querySelector('.status-text');

        if (data.ai_available) {
            badge.className = 'ai-status-badge connected';
            text.textContent = 'AI Online';
        } else {
            badge.className = 'ai-status-badge offline';
            text.textContent = 'AI Offline';
        }
    } catch (e) {
        if (elements.aiStatusBadge) {
            elements.aiStatusBadge.className = 'ai-status-badge offline';
            elements.aiStatusBadge.querySelector('.status-text').textContent = 'Server Error';
        }
    }
}

function setupEventListeners() {
    console.log('⚡ Initializing Modern Mestri Event Listeners...');

    // Form submission
    if (elements.form) {
        elements.form.addEventListener('submit', handleFormSubmit);
    }

    // Header CTA
    if (elements.headerCta) {
        elements.headerCta.addEventListener('click', () => {
            if (elements.form) {
                window.scrollTo({ top: elements.form.offsetTop - 100, behavior: 'smooth' });
            }
        });
    }

    // Reset button
    if (elements.resetBtn) {
        elements.resetBtn.addEventListener('click', resetToInput);
    }
}

// ========================================
// Form Handling
// ========================================
async function handleFormSubmit(e) {
    e.preventDefault();

    const projectData = {
        area: parseFloat(document.getElementById('area').value),
        floors: parseInt(document.getElementById('floors').value),
        budget: parseFloat(document.getElementById('budget').value) || 0,
        timeline: parseInt(document.getElementById('timeline').value) || 0,
        complexity: document.querySelector('input[name="complexity"]:checked').value,
        facing: document.querySelector('input[name="facing"]:checked').value,
        custom_layout: window.customLayout || null
    };

    // Simple Validation (Based on Sq Yards)
    if (projectData.area < 25 || projectData.area > 2500) {
        alert('Please enter a realistic area (25 - 2,500 sq yards)');
        return;
    }

    window.currentProject = projectData;
    await generatePlan(projectData);
}

// ========================================
// Plan Generation
// ========================================
async function generatePlan(projectData) {
    try {
        elements.loadingOverlay.classList.remove('hidden');
        elements.loadingMsg.textContent = 'Analyzing parameters...';

        const response = await fetch(`${window.ModernMestri.API_BASE_URL}/plan`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(projectData)
        });

        if (!response.ok) throw new Error('API Error');
        const data = await response.json();

        if (data.success) {
            window.currentPlan = data;
            displayResults(data);

            // Navigate to Results
            elements.hero.classList.add('hidden');
            elements.resultsSection.classList.remove('hidden');
            window.scrollTo({ top: 0, behavior: 'smooth' });

            // Re-initialize Charts
            if (window.initializeCharts) {
                window.initializeCharts(data);
            }
        }
    } catch (error) {
        console.error('CRITICAL: Plan Error:', error);
        alert(`❌ Connection Error: The website cannot talk to the backend.

Steps to Fix:
1. Double-click "start.bat" in the project folder.
2. Wait for the terminal to stay open.
3. Use the browser window that opens automatically.`);
    } finally {
        elements.loadingOverlay.classList.add('hidden');
    }
}

// ========================================
// Results Display
// ========================================
function displayResults(plan) {
    // Summary
    elements.projectSummary.innerHTML = `
        <div class="summary-item"><strong>Area:</strong> ${plan.project_summary.area} sq yards</div>
        <div class="summary-item"><strong>Floors:</strong> ${plan.project_summary.floors}</div>
        <div class="summary-item"><strong>Complexity:</strong> ${plan.project_summary.complexity.toUpperCase()}</div>
        <div class="summary-item" style="color: var(--accent);"><strong>Vastu Facing:</strong> ${plan.project_summary.facing.toUpperCase()}</div>
    `;

    // 3D Visualization
    const visImg = document.getElementById('output3DImage');
    const visMsg = document.getElementById('visualizationMsg');
    if (visImg && plan.visualization) {
        visImg.src = plan.visualization.image_path;
        visMsg.textContent = plan.visualization.message;
    }

    // Structural Analysis
    const structDiv = document.getElementById('structuralDetails');
    if (structDiv && plan.structural_analysis) {
        const s = plan.structural_analysis;
        structDiv.innerHTML = `
            <div style="background: var(--slate-50); padding: 0.75rem; border-radius: 8px;">
                <div style="font-size: 0.75rem; color: var(--slate-500);">Foundation</div>
                <div style="font-weight: 700;">${s.foundation}</div>
            </div>
            <div style="background: var(--slate-50); padding: 0.75rem; border-radius: 8px;">
                <div style="font-size: 0.75rem; color: var(--slate-500);">Column Support</div>
                <div style="font-weight: 700;">${s.pillars_count} Pillars</div>
            </div>
            <div style="background: var(--slate-50); padding: 0.75rem; border-radius: 8px;">
                <div style="font-size: 0.75rem; color: var(--slate-500);">Reinforcement</div>
                <div style="font-weight: 700;">${s.reinforcement}</div>
            </div>
            <div style="background: var(--slate-50); padding: 0.75rem; border-radius: 8px;">
                <div style="font-size: 0.75rem; color: var(--slate-500);">Slab Spec</div>
                <div style="font-weight: 700;">${s.slab_thickness}</div>
            </div>
        `;
    }

    // AI Analysis
    if (elements.aiAnalysis && plan.ai_analysis) {
        elements.aiAnalysis.innerHTML = `<div class="ai-text-block">${plan.ai_analysis.analysis.replace(/\n/g, '<br>')}</div>`;
    }

    // Cost
    elements.costDetails.innerHTML = `
        <div class="total-badge" style="background: var(--slate-100); padding: 1rem; border-radius: 8px; margin-top: 1rem; text-align: center;">
            <div style="font-size: 0.9rem; color: var(--slate-500);">Total Estimated Budget</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: var(--primary);">₹${formatNumber(plan.cost_estimate.total_cost)}</div>
        </div>
    `;

    // Materials
    let matHtml = '<div style="display: flex; flex-direction: column; gap: 0.75rem;">';
    Object.entries(plan.material_estimate.materials).forEach(([key, mat]) => {
        matHtml += `
            <div style="display: flex; justify-content: space-between; padding-bottom: 0.5rem; border-bottom: 1px solid var(--slate-100);">
                <span>${capitalize(key)}</span>
                <strong>${formatNumber(mat.quantity)} ${mat.unit}</strong>
            </div>
        `;
    });
    matHtml += '</div>';
    elements.materialDetails.innerHTML = matHtml;

    // Schedule
    elements.scheduleDetails.innerHTML = `
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <div style="font-size: 2rem; font-weight: 800; color: var(--primary);">${plan.schedule.total_weeks} Weeks</div>
            <div style="color: var(--slate-500);">Recommended Timeline</div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
            ${Object.entries(plan.schedule.phases).map(([k, p]) => `
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                    <span>${p.name}</span>
                    <span>${p.duration_days} days</span>
                </div>
            `).join('')}
        </div>
    `;

    // Workforce
    elements.workforceDetails.innerHTML = `
        <div style="background: var(--slate-900); color: white; padding: 1rem; border-radius: 8px; text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 1.5rem; font-weight: 800;">${plan.labor_plan.total_workforce.total_peak}</div>
            <div style="font-size: 0.8rem; opacity: 0.8;">Peak Worker Capacity</div>
        </div>
    `;

    // Blueprint Layout Initialization
    if (plan.blueprints) {
        setupBlueprintTabs(plan.blueprints);
        renderBlueprint('classic', plan.blueprints);
    }
}

function setupBlueprintTabs(blueprints) {
    const tabs = document.querySelectorAll('.tab-btn');
    tabs.forEach(tab => {
        tab.onclick = () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            renderBlueprint(tab.dataset.variation, blueprints);
        };
    });
}

function renderBlueprint(variation, blueprints) {
    const blueprint = blueprints[variation];
    const display = document.getElementById('blueprintDisplay');
    const desc = document.getElementById('variationDesc');

    // Update Description based on Variation
    const variationsInfo = {
        'classic': '<strong>Classic Vastu Layout:</strong> Traditional design with clearly defined zones. Focuses on privacy with separate rooms and a standard flow ideal for large Indian families.',
        'modern_open': '<strong>Modern Open Concept:</strong> Removes unnecessary walls to merge Kitchen, Living, and Dining. Creates an airy, spacious feel with maximum natural light and better cross-ventilation.',
        'compact_luxury': '<strong>Compact Luxury:</strong> Prioritizes oversized "Master" suites and attached toilets for every bedroom. Features a grand entrance foyer and premium finishes layout.'
    };

    desc.innerHTML = variationsInfo[variation] || '';

    let blueHtml = '<div class="blueprint-floors" style="display: flex; flex-direction: column; gap: 2rem;">';
    blueprint.floor_layouts.forEach(floor => {
        blueHtml += `
            <div>
                <h4 style="margin-bottom: 1rem; color: var(--primary);">${floor.floor_type} (${blueprint.variation_name})</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 1rem;">
                    ${floor.rooms.map(room => `
                        <div style="background: var(--slate-50); border: 1px solid var(--slate-200); padding: 0.75rem; border-radius: 8px;">
                            <div style="font-weight: 700; font-size: 0.9rem;">${room.name}</div>
                            <div style="font-size: 0.8rem; color: var(--slate-500);">${room.length}' × ${room.width}'</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    });
    blueHtml += '</div>';
    display.innerHTML = blueHtml;
}

// ========================================
// Utilities
// ========================================
function resetToInput() {
    elements.resultsSection.classList.add('hidden');
    elements.hero.classList.remove('hidden');
    elements.form.reset();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function formatNumber(num) {
    return new Intl.NumberFormat('en-IN').format(Math.round(num));
}

function capitalize(str) {
    return str.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

// Global Exports
window.ModernMestri = {
    API_BASE_URL: API_BASE_URL
};
