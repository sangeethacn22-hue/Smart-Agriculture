// Smart Agriculture Platform - Main JavaScript File
// API Configuration
const CONFIG = {
    API_BASE: 'http://localhost:8006/api',
    FRONTEND_PORT: 3007,
    BACKEND_PORT: 8006
};

// Utility Functions
const Utils = {
    // Format numbers with commas
    formatNumber: (num) => {
        return num.toLocaleString();
    },

    // Format date
    formatDate: (date) => {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },

    // Show loading spinner
    showLoading: (elementId) => {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = '<div class="loading"><div class="spinner"></div><p>Loading...</p></div>';
        }
    },

    // Show error message
    showError: (elementId, message) => {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `<div class="alert alert-danger">${message}</div>`;
        }
    },

    // Show success message
    showSuccess: (elementId, message) => {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `<div class="alert alert-success">${message}</div>`;
        }
    },

    // Debounce function for search/filter
    debounce: (func, wait) => {
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
};

// API Service
const API = {
    // Generic fetch wrapper
    async fetch(endpoint, options = {}) {
        try {
            const response = await fetch(`${CONFIG.API_BASE}${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    // Get dashboard summary
    async getDashboardSummary() {
        return await this.fetch('/dashboard/summary');
    },

    // Get crop data
    async getCrops() {
        return await this.fetch('/data/crops');
    },

    // Get weather data
    async getWeather() {
        return await this.fetch('/data/weather');
    },

    // Get soil data
    async getSoil() {
        return await this.fetch('/data/soil');
    },

    // Get yield trends
    async getYields() {
        return await this.fetch('/data/yields');
    },

    // Get AI advisory
    async getAdvisory(crop, season, region = 'General') {
        return await this.fetch('/ai/advisory', {
            method: 'POST',
            body: JSON.stringify({ crop, season, region })
        });
    },

    // Upload data file
    async uploadData(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${CONFIG.API_BASE}/data/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Upload failed! status: ${response.status}`);
        }

        return await response.json();
    }
};

// Chart Helper
const ChartHelper = {
    // Default chart colors
    colors: {
        primary: 'rgba(102, 126, 234, 0.8)',
        secondary: 'rgba(118, 75, 162, 0.8)',
        success: 'rgba(39, 174, 96, 0.8)',
        danger: 'rgba(231, 76, 60, 0.8)',
        warning: 'rgba(243, 156, 18, 0.8)',
        info: 'rgba(52, 152, 219, 0.8)'
    },

    // Create bar chart
    createBarChart(canvasId, labels, data, label = 'Data') {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: data,
                    backgroundColor: this.colors.primary,
                    borderColor: this.colors.primary,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    },

    // Create line chart
    createLineChart(canvasId, labels, datasets) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                tension: 0.4
            }
        });
    },

    // Create pie/doughnut chart
    createDoughnutChart(canvasId, labels, data) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        const colors = Object.values(this.colors);

        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: colors
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
};

// Data Processor
const DataProcessor = {
    // Group data by key
    groupBy(array, key) {
        return array.reduce((result, item) => {
            const group = item[key];
            if (!result[group]) {
                result[group] = [];
            }
            result[group].push(item);
            return result;
        }, {});
    },

    // Calculate average
    average(array, key) {
        if (array.length === 0) return 0;
        const sum = array.reduce((acc, item) => acc + (item[key] || 0), 0);
        return sum / array.length;
    },

    // Calculate sum
    sum(array, key) {
        return array.reduce((acc, item) => acc + (item[key] || 0), 0);
    },

    // Get unique values
    unique(array, key) {
        return [...new Set(array.map(item => item[key]))];
    },

    // Filter data
    filter(array, filters) {
        return array.filter(item => {
            return Object.keys(filters).every(key => {
                if (filters[key] === 'all' || filters[key] === '') return true;
                return item[key] === filters[key];
            });
        });
    },

    // Sort data
    sort(array, key, order = 'asc') {
        return [...array].sort((a, b) => {
            if (order === 'asc') {
                return a[key] > b[key] ? 1 : -1;
            } else {
                return a[key] < b[key] ? 1 : -1;
            }
        });
    }
};

// Table Builder
const TableBuilder = {
    // Create table HTML
    createTable(data, columns) {
        let html = '<table class="table"><thead><tr>';
        
        // Create header
        columns.forEach(col => {
            html += `<th>${col.label}</th>`;
        });
        html += '</tr></thead><tbody>';
        
        // Create rows
        data.forEach(row => {
            html += '<tr>';
            columns.forEach(col => {
                let value = row[col.key];
                if (col.format) {
                    value = col.format(value);
                }
                html += `<td>${value}</td>`;
            });
            html += '</tr>';
        });
        
        html += '</tbody></table>';
        return html;
    },

    // Update table body only
    updateTableBody(tableId, data, columns) {
        const tbody = document.querySelector(`#${tableId} tbody`);
        if (!tbody) return;

        let html = '';
        data.forEach(row => {
            html += '<tr>';
            columns.forEach(col => {
                let value = row[col.key];
                if (col.format) {
                    value = col.format(value);
                }
                html += `<td>${value}</td>`;
            });
            html += '</tr>';
        });

        tbody.innerHTML = html;
    }
};

// Report Generator
const ReportGenerator = {
    // Generate CSV
    generateCSV(data, filename = 'report.csv') {
        if (data.length === 0) return;

        const headers = Object.keys(data[0]);
        const csv = [
            headers.join(','),
            ...data.map(row => 
                headers.map(header => 
                    JSON.stringify(row[header] || '')
                ).join(',')
            )
        ].join('\n');

        this.downloadFile(csv, filename, 'text/csv');
    },

    // Generate text report
    generateTextReport(data, title) {
        let report = `${title}\n`;
        report += '='.repeat(60) + '\n\n';
        report += `Generated: ${new Date().toLocaleString()}\n\n`;

        Object.keys(data).forEach(section => {
            report += `${section.toUpperCase()}\n`;
            report += '-'.repeat(60) + '\n';
            
            if (Array.isArray(data[section])) {
                data[section].forEach(item => {
                    report += `${JSON.stringify(item)}\n`;
                });
            } else {
                report += `${data[section]}\n`;
            }
            
            report += '\n';
        });

        return report;
    },

    // Download file
    downloadFile(content, filename, type) {
        const blob = new Blob([content], { type: type });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        window.URL.revokeObjectURL(url);
    }
};

// Form Handler
const FormHandler = {
    // Get form data as object
    getFormData(formId) {
        const form = document.getElementById(formId);
        if (!form) return null;

        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        return data;
    },

    // Validate form
    validateForm(formId, rules) {
        const data = this.getFormData(formId);
        const errors = [];

        Object.keys(rules).forEach(field => {
            const value = data[field];
            const rule = rules[field];

            if (rule.required && (!value || value.trim() === '')) {
                errors.push(`${field} is required`);
            }

            if (rule.min && value && value.length < rule.min) {
                errors.push(`${field} must be at least ${rule.min} characters`);
            }

            if (rule.max && value && value.length > rule.max) {
                errors.push(`${field} must be less than ${rule.max} characters`);
            }

            if (rule.pattern && value && !rule.pattern.test(value)) {
                errors.push(`${field} format is invalid`);
            }
        });

        return {
            valid: errors.length === 0,
            errors: errors
        };
    },

    // Clear form
    clearForm(formId) {
        const form = document.getElementById(formId);
        if (form) {
            form.reset();
        }
    }
};

// Local Storage Helper
const Storage = {
    // Set item
    set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (e) {
            console.error('Storage error:', e);
            return false;
        }
    },

    // Get item
    get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (e) {
            console.error('Storage error:', e);
            return defaultValue;
        }
    },

    // Remove item
    remove(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (e) {
            console.error('Storage error:', e);
            return false;
        }
    },

    // Clear all
    clear() {
        try {
            localStorage.clear();
            return true;
        } catch (e) {
            console.error('Storage error:', e);
            return false;
        }
    }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        CONFIG,
        Utils,
        API,
        ChartHelper,
        DataProcessor,
        TableBuilder,
        ReportGenerator,
        FormHandler,
        Storage
    };
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    console.log('Smart Agriculture Platform initialized');
    
    // Check backend status
    fetch(CONFIG.API_BASE.replace('/api', ''))
        .then(response => response.json())
        .then(data => {
            console.log('✅ Backend connected:', data);
        })
        .catch(error => {
            console.error('❌ Backend connection failed:', error);
        });
});