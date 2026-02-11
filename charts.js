/**
 * Modern Mestri - Advanced Data Visualizations (Powerplay Edition)
 */

let costChartInstance = null;
let workforceChartInstance = null;

function initializeCharts(plan) {
    console.log('📊 Updating charts...');

    // Destroy existing charts if they exist
    if (costChartInstance) costChartInstance.destroy();
    if (workforceChartInstance) workforceChartInstance.destroy();

    const ctxCost = document.getElementById('costChart');
    const ctxWork = document.getElementById('workforceChart');

    if (ctxCost) {
        costChartInstance = createCostChart(ctxCost, plan.cost_estimate);
    }

    if (ctxWork) {
        workforceChartInstance = createWorkforceChart(ctxWork, plan.labor_plan);
    }
}

function createCostChart(ctx, data) {
    const labels = ['Materials', 'Labor', 'Plumbing', 'Electrical', 'Misc', 'Contingency'];
    const values = [
        data.material_cost,
        data.labor_cost,
        data.plumbing_cost,
        data.electrical_cost,
        data.miscellaneous_cost,
        data.contingency
    ];

    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: [
                    '#1D4ED8', // Primary Blue
                    '#4F46E5', // Indigo
                    '#3B82F6', // Info Blue
                    '#6366F1', // Light Indigo
                    '#94A3B8', // Slate
                    '#1E293B'  // Dark Slate
                ],
                borderWidth: 2,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        font: { family: 'Inter', size: 12 }
                    }
                }
            },
            cutout: '70%'
        }
    });
}

function createWorkforceChart(ctx, data) {
    const workforce = data.total_workforce;
    const labels = ['Masons', 'Helpers', 'Carpenters', 'Electricians', 'Plumbers', 'Supervisors'];
    const values = [
        workforce.masons,
        workforce.helpers,
        workforce.carpenters,
        workforce.electricians,
        workforce.plumbers,
        workforce.supervisors
    ];

    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Workers Assigned',
                data: values,
                backgroundColor: 'rgba(29, 78, 216, 0.8)',
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            indexAxis: 'y',
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { font: { family: 'Inter' } }
                },
                y: {
                    grid: { display: false },
                    ticks: { font: { family: 'Inter' } }
                }
            }
        }
    });
}

// Global Export
window.initializeCharts = initializeCharts;
