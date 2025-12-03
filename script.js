// script.js - COMPLETE JAVASCRIPT CONTROLLER
// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme toggle
    initThemeToggle();
    
    // Initialize form validation
    initFormValidation();
    
    // Initialize student stats
    updateStudentStats();
    
    // Add animations to cards
    animateCards();
    
    // Initialize tooltips
    initTooltips();
});

// Theme Toggle Functionality
function initThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    
    // Check for saved theme preference or default to light
    const savedTheme = localStorage.getItem('theme') || 'light';
    body.classList.add(savedTheme + '-mode');
    themeToggle.checked = savedTheme === 'dark';
    
    // Toggle theme on switch change
    themeToggle.addEventListener('change', function() {
        const isDarkMode = this.checked;
        
        // Remove existing theme classes
        body.classList.remove('light-mode', 'dark-mode');
        
        // Add new theme class
        if (isDarkMode) {
            body.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark');
        } else {
            body.classList.add('light-mode');
            localStorage.setItem('theme', 'light');
        }
        
        // Dispatch theme change event
        const event = new CustomEvent('themeChange', { detail: { theme: isDarkMode ? 'dark' : 'light' } });
        document.dispatchEvent(event);
    });
}

// Form Validation
function initFormValidation() {
    const forms = document.querySelectorAll('.student-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            let isValid = true;
            const requiredFields = form.querySelectorAll('[required]');
            
            // Clear previous errors
            clearErrors(form);
            
            // Validate each required field
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    showError(field, 'This field is required');
                    isValid = false;
                } else if (field.type === 'email' && !isValidEmail(field.value)) {
                    showError(field, 'Please enter a valid email address');
                    isValid = false;
                } else if (field.type === 'tel' && !isValidPhone(field.value)) {
                    showError(field, 'Please enter a valid phone number');
                    isValid = false;
                } else if (field.type === 'number') {
                    const age = parseInt(field.value);
                    if (age < 10 || age > 25) {
                        showError(field, 'Age must be between 10 and 25');
                        isValid = false;
                    }
                }
            });
            
            // Prevent form submission if invalid
            if (!isValid) {
                event.preventDefault();
            }
        });
    });
    
    // Add input event listeners for real-time validation
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            clearError(this);
            
            if (this.type === 'email' && this.value) {
                if (!isValidEmail(this.value)) {
                    showError(this, 'Please enter a valid email address');
                }
            }
            
            if (this.type === 'tel' && this.value) {
                if (!isValidPhone(this.value)) {
                    showError(this, 'Please enter a valid phone number');
                }
            }
        });
        
        input.addEventListener('blur', function() {
            if (this.required && !this.value.trim()) {
                showError(this, 'This field is required');
            }
        });
    });
}

// Helper validation functions
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPhone(phone) {
    const phoneRegex = /^[0-9\-]+$/;
    return phoneRegex.test(phone);
}

// Error display functions
function showError(input, message) {
    const formGroup = input.closest('.form-group');
    if (!formGroup) return;
    
    // Remove existing error
    const existingError = formGroup.querySelector('.error-message');
    if (existingError) existingError.remove();
    
    // Add error class to input
    input.classList.add('error');
    
    // Create error message element
    const errorElement = document.createElement('div');
    errorElement.className = 'error-message';
    errorElement.style.color = '#e53e3e';
    errorElement.style.fontSize = '12px';
    errorElement.style.marginTop = '5px';
    errorElement.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
    
    formGroup.appendChild(errorElement);
}

function clearError(input) {
    input.classList.remove('error');
    const formGroup = input.closest('.form-group');
    if (formGroup) {
        const errorElement = formGroup.querySelector('.error-message');
        if (errorElement) errorElement.remove();
    }
}

function clearErrors(form) {
    const inputs = form.querySelectorAll('input, select');
    inputs.forEach(input => clearError(input));
}

// Update student statistics
function updateStudentStats() {
    const studentCards = document.querySelectorAll('.student-card');
    const totalStudents = document.querySelectorAll('#totalStudents');
    
    if (totalStudents.length > 0) {
        totalStudents.forEach(span => {
            span.textContent = studentCards.length;
        });
    }
    
    // Update grade distribution if needed
    updateGradeDistribution();
}

function updateGradeDistribution() {
    const gradeElements = document.querySelectorAll('[data-grade]');
    if (gradeElements.length > 0) {
        // You can add logic here to calculate and update grade distribution
    }
}

// Card animations
function animateCards() {
    const cards = document.querySelectorAll('.student-card, .stat-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });
    
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
}

// Tooltips
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = tooltipText;
            tooltip.style.position = 'absolute';
            tooltip.style.background = 'rgba(0, 0, 0, 0.8)';
            tooltip.style.color = 'white';
            tooltip.style.padding = '5px 10px';
            tooltip.style.borderRadius = '4px';
            tooltip.style.fontSize = '12px';
            tooltip.style.zIndex = '1000';
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + 'px';
            tooltip.style.top = (rect.top - 30) + 'px';
            
            document.body.appendChild(tooltip);
            
            this._tooltip = tooltip;
        });
        
        element.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                this._tooltip.remove();
                this._tooltip = null;
            }
        });
    });
}

// Auto-dismiss flash messages after 5 seconds
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash');
    
    flashMessages.forEach(flash => {
        setTimeout(() => {
            if (flash.parentElement) {
                flash.style.opacity = '0';
                flash.style.transform = 'translateX(-100%)';
                setTimeout(() => {
                    if (flash.parentElement) {
                        flash.remove();
                    }
                }, 300);
            }
        }, 5000);
    });
}

// Initialize flash messages when they exist
if (document.querySelector('.flash')) {
    initFlashMessages();
}

// Add CSS for errors
const errorStyles = `
    .error {
        border-color: #e53e3e !important;
    }
    
    .error:focus {
        box-shadow: 0 0 0 3px rgba(229, 62, 62, 0.1) !important;
    }
    
    .error-message i {
        margin-right: 5px;
    }
    
    .tooltip {
        pointer-events: none;
    }
`;

const styleSheet = document.createElement('style');
styleSheet.textContent = errorStyles;
document.head.appendChild(styleSheet);

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + N for new student
    if ((event.ctrlKey || event.metaKey) && event.key === 'n') {
        event.preventDefault();
        const addButton = document.querySelector('a[href*="add"]');
        if (addButton) addButton.click();
    }
    
    // Escape key to go back
    if (event.key === 'Escape') {
        const backButton = document.querySelector('.btn-back');
        if (backButton) backButton.click();
    }
});

// Add loading animation for form submission
document.addEventListener('submit', function(event) {
    const form = event.target;
    if (form.classList.contains('student-form')) {
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            submitButton.disabled = true;
        }
    }
});
