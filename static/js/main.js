// Main JavaScript file for Virtual IHC Analysis System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // File upload handling
    initializeFileUpload();
    
    // Image comparison functionality
    initializeImageComparison();
    
    // Auto-refresh for processing status
    initializeAutoRefresh();
    
    // Print functionality
    initializePrintHandlers();
});

/**
 * Initialize file upload functionality
 */
function initializeFileUpload() {
    const fileInput = document.querySelector('input[type="file"]');
    const uploadArea = document.querySelector('.file-upload-area');
    
    if (!fileInput || !uploadArea) return;

    // Drag and drop functionality
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelection(files[0]);
        }
    });

    // Click to select file
    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });

    // File selection handler
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            handleFileSelection(file);
        }
    });
}

/**
 * Handle file selection and validation
 */
function handleFileSelection(file) {
    const allowedTypes = ['image/png', 'image/jpeg', 'image/tiff'];
    const maxSize = 16 * 1024 * 1024; // 16MB

    // Validate file type
    if (!allowedTypes.includes(file.type)) {
        showAlert('Invalid file type. Please select PNG, JPEG, or TIFF images only.', 'error');
        return false;
    }

    // Validate file size
    if (file.size > maxSize) {
        showAlert('File size too large. Maximum allowed size is 16MB.', 'error');
        return false;
    }

    // Show file preview
    showFilePreview(file);
    return true;
}

/**
 * Show file preview
 */
function showFilePreview(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const preview = document.getElementById('imagePreview');
        const previewImg = document.getElementById('previewImg');
        const imageInfo = document.getElementById('imageInfo');
        
        if (preview && previewImg) {
            previewImg.src = e.target.result;
            preview.classList.remove('d-none');
            
            if (imageInfo) {
                const fileSize = (file.size / 1024 / 1024).toFixed(2);
                imageInfo.innerHTML = `
                    <small class="text-muted">
                        <strong>File:</strong> ${file.name}<br>
                        <strong>Size:</strong> ${fileSize} MB<br>
                        <strong>Type:</strong> ${file.type}
                    </small>
                `;
            }
        }
    };
    reader.readAsDataURL(file);
}

/**
 * Initialize image comparison functionality
 */
function initializeImageComparison() {
    const comparisons = document.querySelectorAll('.image-comparison');
    
    comparisons.forEach(function(comparison) {
        // Add mouse events for image comparison
        comparison.addEventListener('mousemove', function(e) {
            const rect = comparison.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const width = rect.width;
            const percentage = (x / width) * 100;
            
            // Update comparison slider if exists
            const slider = comparison.querySelector('.comparison-slider');
            if (slider) {
                slider.style.left = percentage + '%';
            }
        });
    });
}

/**
 * Initialize auto-refresh for processing status
 */
function initializeAutoRefresh() {
    const processingStatus = document.querySelector('[data-processing="true"]');
    
    if (processingStatus) {
        // Refresh page every 10 seconds if still processing
        const refreshInterval = setInterval(function() {
            window.location.reload();
        }, 10000);
        
        // Clear interval after 5 minutes to prevent infinite refreshing
        setTimeout(function() {
            clearInterval(refreshInterval);
        }, 300000);
    }
}

/**
 * Initialize print handlers
 */
function initializePrintHandlers() {
    const printButtons = document.querySelectorAll('[data-action="print"]');
    
    printButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            window.print();
        });
    });
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        <i data-feather="${type === 'error' ? 'alert-circle' : 'info'}"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertContainer, container.firstChild);
        
        // Re-initialize feather icons for the new alert
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
        
        // Auto-dismiss after 5 seconds
        setTimeout(function() {
            alertContainer.remove();
        }, 5000);
    }
}

/**
 * Format file size for display
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Format percentage for display
 */
function formatPercentage(value, decimals = 1) {
    return (value * 100).toFixed(decimals) + '%';
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() {
            showAlert('Copied to clipboard!', 'success');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showAlert('Copied to clipboard!', 'success');
    }
}

/**
 * Download file
 */
function downloadFile(url, filename) {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

/**
 * Validate form before submission
 */
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

/**
 * Show loading spinner
 */
function showLoading(element, text = 'Processing...') {
    if (typeof element === 'string') {
        element = document.getElementById(element);
    }
    
    if (element) {
        element.innerHTML = `
            <div class="d-flex align-items-center">
                <div class="spinner-border spinner-border-sm me-2" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                ${text}
            </div>
        `;
        element.disabled = true;
    }
}

/**
 * Hide loading spinner
 */
function hideLoading(element, originalText = 'Submit') {
    if (typeof element === 'string') {
        element = document.getElementById(element);
    }
    
    if (element) {
        element.innerHTML = originalText;
        element.disabled = false;
    }
}

// Export functions for use in other scripts
window.VirtualIHC = {
    showAlert,
    formatFileSize,
    formatPercentage,
    copyToClipboard,
    downloadFile,
    validateForm,
    showLoading,
    hideLoading
};
