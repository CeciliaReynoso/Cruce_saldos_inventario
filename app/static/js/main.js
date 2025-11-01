// JavaScript principal para la aplicación de inventarios

// Variables globales
let uploadForm;
let submitBtn;
let progressContainer;
let progressBar;

// Inicialización cuando se carga el DOM
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    setupFileUpload();
    setupFormValidation();
});

// Inicializar variables y elementos
function initializeApp() {
    uploadForm = document.getElementById('uploadForm');
    submitBtn = document.getElementById('submitBtn');
    progressContainer = document.querySelector('.progress-container');
    progressBar = document.querySelector('.progress-bar');
    
    console.log('Aplicación de inventarios inicializada');
}

// Configurar todos los event listeners
function setupEventListeners() {
    // Event listener para el formulario
    if (uploadForm) {
        uploadForm.addEventListener('submit', handleFormSubmit);
    }

    // Event listeners para archivos
    setupFileInputListeners();
    
    // Event listeners para drag and drop
    setupDragAndDrop();
    
    // Event listeners para selección de formato
    setupFormatSelection();
}

// Configurar listeners para inputs de archivos
function setupFileInputListeners() {
    const fileInputs = document.querySelectorAll('.file-input');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            handleFileSelect(e.target);
        });
    });

    // Botones de remover archivo
    document.addEventListener('click', function(e) {
        if (e.target.closest('.remove-file')) {
            handleFileRemove(e.target.closest('.remove-file'));
        }
    });
}

// Configurar drag and drop
function setupDragAndDrop() {
    const uploadAreas = document.querySelectorAll('.upload-area');
    
    uploadAreas.forEach(area => {
        area.addEventListener('dragover', handleDragOver);
        area.addEventListener('dragleave', handleDragLeave);
        area.addEventListener('drop', handleFileDrop);
    });
}

// Manejar drag over
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.add('drag-over');
}

// Manejar drag leave
function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('drag-over');
}

// Manejar file drop
function handleFileDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    
    const uploadArea = e.currentTarget;
    const fileInput = uploadArea.querySelector('.file-input');
    const files = e.dataTransfer.files;
    
    uploadArea.classList.remove('drag-over');
    
    if (files.length > 0) {
        const file = files[0];
        
        // Validar tipo de archivo
        if (isValidFileType(file)) {
            fileInput.files = files;
            handleFileSelect(fileInput);
        } else {
            showError('Tipo de archivo no válido. Solo se permiten archivos CSV y Excel (.xlsx, .xls)');
        }
    }
}

// Manejar selección de archivo
function handleFileSelect(input) {
    const file = input.files[0];
    const uploadArea = input.closest('.upload-area');
    const placeholder = uploadArea.querySelector('.upload-placeholder');
    const fileInfo = uploadArea.querySelector('.file-info');
    const fileName = fileInfo.querySelector('.file-name');
    
    if (file) {
        // Validar archivo
        if (!isValidFileType(file)) {
            showError('Tipo de archivo no válido. Solo se permiten archivos CSV y Excel (.xlsx, .xls)');
            input.value = '';
            return;
        }
        
        if (!isValidFileSize(file)) {
            showError('El archivo es demasiado grande. Tamaño máximo: 10MB');
            input.value = '';
            return;
        }
        
        // Mostrar información del archivo
        fileName.textContent = file.name;
        placeholder.classList.add('d-none');
        fileInfo.classList.remove('d-none');
        uploadArea.classList.add('has-file');
        
        // Agregar animación
        fileInfo.classList.add('fade-in');
        
        console.log(`Archivo seleccionado: ${file.name} (${formatFileSize(file.size)})`);
    }
    
    validateForm();
}

// Manejar remoción de archivo
function handleFileRemove(button) {
    const uploadArea = button.closest('.upload-area');
    const fileInput = uploadArea.querySelector('.file-input');
    const placeholder = uploadArea.querySelector('.upload-placeholder');
    const fileInfo = uploadArea.querySelector('.file-info');
    
    // Limpiar input
    fileInput.value = '';
    
    // Mostrar placeholder y ocultar info
    fileInfo.classList.add('d-none');
    placeholder.classList.remove('d-none');
    uploadArea.classList.remove('has-file');
    
    validateForm();
}

// Validar tipo de archivo
function isValidFileType(file) {
    const validTypes = ['text/csv', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
    const validExtensions = ['.csv', '.xls', '.xlsx'];
    
    return validTypes.includes(file.type) || validExtensions.some(ext => file.name.toLowerCase().endsWith(ext));
}

// Validar tamaño de archivo (10MB máximo)
function isValidFileSize(file) {
    const maxSize = 10 * 1024 * 1024; // 10MB en bytes
    return file.size <= maxSize;
}

// Formatear tamaño de archivo
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Configurar selección de formato
function setupFormatSelection() {
    const formatRadios = document.querySelectorAll('input[name="formato_salida"]');
    const formatCards = document.querySelectorAll('.format-card');
    const formatInfo = document.getElementById('formatInfo');
    const formatInfoText = document.getElementById('formatInfoText');
    
    // Inicializar estado
    updateFormatSelection();
    
    // Event listeners para cambios en la selección
    formatRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            updateFormatSelection();
            showFormatChangeAnimation();
        });
    });
    
    // Event listeners para clicks en las tarjetas
    formatCards.forEach(card => {
        card.addEventListener('click', function(e) {
            e.preventDefault();
            const radio = document.getElementById(this.getAttribute('for'));
            if (radio && !radio.checked) {
                radio.checked = true;
                updateFormatSelection();
                showFormatChangeAnimation();
            }
        });
    });
    
    function updateFormatSelection() {
        const selectedFormat = document.querySelector('input[name="formato_salida"]:checked');
        
        if (!selectedFormat) return;
        
        // Remover clases selected de todas las tarjetas
        formatCards.forEach(card => card.classList.remove('selected'));
        
        // Agregar clase selected a la tarjeta correspondiente
        const selectedCard = document.querySelector(`label[for="${selectedFormat.id}"]`);
        if (selectedCard) {
            selectedCard.classList.add('selected');
        }
        
        // Actualizar información del formato
        updateFormatInfo(selectedFormat.value);
    }
    
    function updateFormatInfo(format) {
        if (!formatInfoText) return;
        
        const formatMessages = {
            'CSV': {
                text: '<strong>CSV seleccionado:</strong> El archivo se generará en formato de texto plano (.csv) que puede abrirse en Excel, Google Sheets u otros programas de hojas de cálculo.',
                icon: 'fas fa-file-csv text-success'
            },
            'Excel': {
                text: '<strong>Excel seleccionado:</strong> El archivo se generará en formato nativo de Microsoft Excel (.xlsx) con formato y funcionalidades avanzadas.',
                icon: 'fas fa-file-excel text-success'
            }
        };
        
        const message = formatMessages[format] || formatMessages['CSV'];
        
        // Actualizar icono
        const icon = formatInfo.querySelector('i');
        if (icon) {
            icon.className = message.icon;
        }
        
        // Actualizar texto con animación
        formatInfoText.style.opacity = '0.5';
        setTimeout(() => {
            formatInfoText.innerHTML = message.text;
            formatInfoText.style.opacity = '1';
        }, 150);
    }
    
    function showFormatChangeAnimation() {
        if (formatInfo) {
            formatInfo.classList.remove('fade-in');
            setTimeout(() => {
                formatInfo.classList.add('fade-in');
            }, 10);
        }
    }
}

// Configurar validación del formulario
function setupFormValidation() {
    validateForm();
}

// Validar formulario completo
function validateForm() {
    const maestroInput = document.getElementById('maestro');
    const conteoInput = document.getElementById('conteo');
    
    const hasMaestro = maestroInput && maestroInput.files.length > 0;
    const hasConteo = conteoInput && conteoInput.files.length > 0;
    
    if (submitBtn) {
        submitBtn.disabled = !(hasMaestro && hasConteo);
        
        // Cambiar texto del botón
        if (hasMaestro && hasConteo) {
            submitBtn.innerHTML = '<i class="fas fa-cogs me-2"></i>Procesar Inventario';
            submitBtn.classList.remove('btn-secondary');
            submitBtn.classList.add('btn-primary');
        } else {
            submitBtn.innerHTML = '<i class="fas fa-upload me-2"></i>Seleccione ambos archivos';
            submitBtn.classList.remove('btn-primary');
            submitBtn.classList.add('btn-secondary');
        }
    }
}

// Manejar envío del formulario
function handleFormSubmit(e) {
    e.preventDefault();
    
    // Validar antes de enviar
    if (!validateBeforeSubmit()) {
        return false;
    }
    
    // Mostrar progreso
    showProgress();
    
    // Deshabilitar botón
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Procesando...';
        submitBtn.classList.add('loading');
    }
    
    // Simular progreso (opcional)
    simulateProgress();
    
    // Enviar formulario
    setTimeout(() => {
        uploadForm.submit();
    }, 500);
}

// Validar antes del envío
function validateBeforeSubmit() {
    const maestroInput = document.getElementById('maestro');
    const conteoInput = document.getElementById('conteo');
    
    if (!maestroInput.files.length) {
        showError('Por favor, seleccione el archivo del inventario maestro');
        return false;
    }
    
    if (!conteoInput.files.length) {
        showError('Por favor, seleccione el archivo del conteo físico');
        return false;
    }
    
    // Validar que ambos archivos sean del mismo tipo
    const maestroFile = maestroInput.files[0];
    const conteoFile = conteoInput.files[0];
    
    const maestroExt = getFileExtension(maestroFile.name);
    const conteoExt = getFileExtension(conteoFile.name);
    
    if (maestroExt !== conteoExt) {
        showError('Ambos archivos deben tener el mismo formato (CSV o Excel)');
        return false;
    }
    
    return true;
}

// Obtener extensión de archivo
function getFileExtension(filename) {
    return filename.slice((filename.lastIndexOf('.') - 1 >>> 0) + 2).toLowerCase();
}

// Mostrar barra de progreso
function showProgress() {
    if (progressContainer) {
        progressContainer.classList.remove('d-none');
        progressContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

// Simular progreso de carga
function simulateProgress() {
    if (!progressBar) return;
    
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress >= 90) {
            progress = 90;
            clearInterval(interval);
        }
        
        progressBar.style.width = progress + '%';
        progressBar.setAttribute('aria-valuenow', progress);
    }, 200);
}

// Mostrar mensaje de error
function showError(message) {
    // Crear o actualizar alert de error
    let errorAlert = document.getElementById('errorAlert');
    
    if (!errorAlert) {
        errorAlert = document.createElement('div');
        errorAlert.id = 'errorAlert';
        errorAlert.className = 'alert alert-danger alert-dismissible fade show mt-3';
        errorAlert.innerHTML = `
            <i class="fas fa-exclamation-triangle me-2"></i>
            <span class="error-message"></span>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insertar después del formulario
        if (uploadForm) {
            uploadForm.parentNode.insertBefore(errorAlert, uploadForm.nextSibling);
        }
    }
    
    const errorMessage = errorAlert.querySelector('.error-message');
    errorMessage.textContent = message;
    
    // Auto-dismiss después de 5 segundos
    setTimeout(() => {
        if (errorAlert) {
            const bsAlert = new bootstrap.Alert(errorAlert);
            bsAlert.close();
        }
    }, 5000);
    
    console.error('Error:', message);
}

// Mostrar mensaje de éxito
function showSuccess(message) {
    const successAlert = document.createElement('div');
    successAlert.className = 'alert alert-success alert-dismissible fade show mt-3';
    successAlert.innerHTML = `
        <i class="fas fa-check-circle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    if (uploadForm) {
        uploadForm.parentNode.insertBefore(successAlert, uploadForm.nextSibling);
    }
    
    // Auto-dismiss después de 5 segundos
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(successAlert);
        bsAlert.close();
    }, 5000);
}

// Resetear formulario
function resetForm() {
    if (uploadForm) {
        uploadForm.reset();
    }
    
    // Limpiar áreas de upload
    const uploadAreas = document.querySelectorAll('.upload-area');
    uploadAreas.forEach(area => {
        const placeholder = area.querySelector('.upload-placeholder');
        const fileInfo = area.querySelector('.file-info');
        
        fileInfo.classList.add('d-none');
        placeholder.classList.remove('d-none');
        area.classList.remove('has-file');
    });
    
    // Ocultar progreso
    if (progressContainer) {
        progressContainer.classList.add('d-none');
    }
    
    // Resetear botón
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-upload me-2"></i>Seleccione ambos archivos';
        submitBtn.classList.remove('btn-primary', 'loading');
        submitBtn.classList.add('btn-secondary');
    }
    
    // Remover alertas
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (alert.id === 'errorAlert' || alert.classList.contains('alert-success')) {
            alert.remove();
        }
    });
    
    console.log('Formulario reseteado');
}

// Utilidades
const Utils = {
    // Debounce function
    debounce: function(func, wait, immediate) {
        let timeout;
        return function executedFunction() {
            const context = this;
            const args = arguments;
            const later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    },
    
    // Throttle function
    throttle: function(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};

// Función global para resetear (usada por el botón)
window.resetForm = resetForm;

// Manejo de errores globales
window.addEventListener('error', function(e) {
    console.error('Error JavaScript:', e.error);
});

// Manejo de promesas rechazadas
window.addEventListener('unhandledrejection', function(e) {
    console.error('Promesa rechazada:', e.reason);
});

console.log('Sistema de inventarios - JavaScript cargado correctamente');