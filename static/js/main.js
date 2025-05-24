/**
 * Application principale JavaScript
 * Gestion Immobilière
 */

// Variables globales
let tooltipTriggerList = [];
let tooltipList = [];

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    initBootstrapComponents();
    initFormValidation();
    initImagePreview();
    initSearchFilters();
    initDatePickers();
    initConfirmDialogs();
    initAjaxForms();
});

/**
 * Initialise les composants Bootstrap
 */
function initBootstrapComponents() {
    // Initialiser les tooltips
    tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialiser les popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts après 5 secondes
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });
}

/**
 * Initialise la validation des formulaires
 */
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Validation en temps réel pour certains champs
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(function(input) {
        input.addEventListener('blur', validateEmail);
    });

    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(function(input) {
        input.addEventListener('input', formatPhoneNumber);
    });
}

/**
 * Valide une adresse email
 */
function validateEmail(event) {
    const input = event.target;
    const email = input.value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (email && !emailRegex.test(email)) {
        input.setCustomValidity('Veuillez entrer une adresse email valide');
    } else {
        input.setCustomValidity('');
    }
}

/**
 * Formate un numéro de téléphone
 */
function formatPhoneNumber(event) {
    const input = event.target;
    let value = input.value.replace(/\D/g, '');
    
    if (value.length >= 10) {
        value = value.replace(/(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})/, '$1 $2 $3 $4 $5');
    }
    
    input.value = value;
}

/**
 * Initialise la prévisualisation des images
 */
function initImagePreview() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    
    imageInputs.forEach(function(input) {
        input.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    showImagePreview(e.target.result, input);
                };
                reader.readAsDataURL(file);
            }
        });
    });
}

/**
 * Affiche la prévisualisation d'une image
 */
function showImagePreview(src, input) {
    let preview = input.parentNode.querySelector('.image-preview');
    
    if (!preview) {
        preview = document.createElement('div');
        preview.className = 'image-preview mt-2';
        input.parentNode.appendChild(preview);
    }
    
    preview.innerHTML = `
        <img src="${src}" class="img-thumbnail" style="max-width: 200px; max-height: 200px;">
        <button type="button" class="btn btn-sm btn-danger ms-2" onclick="removeImagePreview(this)">
            <i class="fas fa-trash"></i> Supprimer
        </button>
    `;
}

/**
 * Supprime la prévisualisation d'une image
 */
function removeImagePreview(button) {
    const preview = button.parentNode;
    const input = preview.parentNode.querySelector('input[type="file"]');
    
    input.value = '';
    preview.remove();
}

/**
 * Initialise les filtres de recherche
 */
function initSearchFilters() {
    const searchForm = document.querySelector('#searchForm');
    if (searchForm) {
        const inputs = searchForm.querySelectorAll('input, select');
        
        inputs.forEach(function(input) {
            input.addEventListener('change', function() {
                // Soumission automatique après un délai
                clearTimeout(input.searchTimeout);
                input.searchTimeout = setTimeout(function() {
                    searchForm.submit();
                }, 500);
            });
        });
    }

    // Recherche en temps réel
    const searchInput = document.querySelector('input[name="search"], input[name="q"]');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(this.searchTimeout);
            this.searchTimeout = setTimeout(function() {
                // Ici on pourrait implémenter une recherche AJAX
                console.log('Recherche pour:', searchInput.value);
            }, 300);
        });
    }
}

/**
 * Initialise les sélecteurs de date
 */
function initDatePickers() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    
    dateInputs.forEach(function(input) {
        // Définir la date d'aujourd'hui par défaut si c'est un champ de date de début
        if (input.name.includes('debut') && !input.value) {
            input.value = new Date().toISOString().split('T')[0];
        }
        
        // Validation des dates
        input.addEventListener('change', function() {
            validateDateRange(input);
        });
    });
}

/**
 * Valide les plages de dates
 */
function validateDateRange(input) {
    const form = input.closest('form');
    if (!form) return;
    
    const startDate = form.querySelector('input[name*="debut"]');
    const endDate = form.querySelector('input[name*="fin"]');
    
    if (startDate && endDate && startDate.value && endDate.value) {
        if (new Date(startDate.value) > new Date(endDate.value)) {
            endDate.setCustomValidity('La date de fin doit être postérieure à la date de début');
        } else {
            endDate.setCustomValidity('');
        }
    }
}

/**
 * Initialise les dialogues de confirmation
 */
function initConfirmDialogs() {
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            const message = button.getAttribute('data-confirm') || 'Êtes-vous sûr de vouloir effectuer cette action ?';
            
            if (!confirm(message)) {
                event.preventDefault();
                return false;
            }
        });
    });
}

/**
 * Initialise les formulaires AJAX
 */
function initAjaxForms() {
    const ajaxForms = document.querySelectorAll('.ajax-form');
    
    ajaxForms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            submitFormAjax(form);
        });
    });
}

/**
 * Soumet un formulaire en AJAX
 */
function submitFormAjax(form) {
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    const originalText = submitButton.innerHTML;
    
    // Désactiver le bouton et montrer un loader
    submitButton.disabled = true;
    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Traitement...';
    
    fetch(form.action, {
        method: form.method || 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Opération réussie', 'success');
            if (data.redirect) {
                window.location.href = data.redirect;
            } else {
                form.reset();
            }
        } else {
            showNotification(data.message || 'Une erreur est survenue', 'danger');
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        showNotification('Une erreur est survenue', 'danger');
    })
    .finally(() => {
        // Réactiver le bouton
        submitButton.disabled = false;
        submitButton.innerHTML = originalText;
    });
}

/**
 * Affiche une notification
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-suppression après 5 secondes
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

/**
 * Calcule et affiche le total des montants
 */
function calculateTotal() {
    const loyerInput = document.querySelector('input[name="loyer_mensuel"], input[name="montant_loyer"]');
    const chargesInput = document.querySelector('input[name="charges_mensuelles"], input[name="montant_charges"]');
    const totalElement = document.querySelector('#total-montant');
    
    if (loyerInput && chargesInput && totalElement) {
        const loyer = parseFloat(loyerInput.value) || 0;
        const charges = parseFloat(chargesInput.value) || 0;
        const total = loyer + charges;
        
        totalElement.textContent = total.toFixed(2) + ' €';
    }
}

/**
 * Initialise le calcul automatique des totaux
 */
document.addEventListener('DOMContentLoaded', function() {
    const montantInputs = document.querySelectorAll('input[name*="loyer"], input[name*="charges"]');
    
    montantInputs.forEach(function(input) {
        input.addEventListener('input', calculateTotal);
    });
    
    // Calcul initial
    calculateTotal();
});

/**
 * Gestion du mode sombre (si implémenté)
 */
function toggleDarkMode() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

/**
 * Initialise le thème sauvegardé
 */
function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-bs-theme', savedTheme);
    }
}

// Appliquer le thème au chargement
initTheme();

/**
 * Utilitaires pour les tableaux
 */
function sortTable(columnIndex, tableId = null) {
    const table = tableId ? document.getElementById(tableId) : document.querySelector('table');
    if (!table) return;
    
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    rows.sort((a, b) => {
        const aVal = a.cells[columnIndex].textContent.trim();
        const bVal = b.cells[columnIndex].textContent.trim();
        
        // Essayer de comparer comme des nombres
        const aNum = parseFloat(aVal.replace(/[^\d.-]/g, ''));
        const bNum = parseFloat(bVal.replace(/[^\d.-]/g, ''));
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return aNum - bNum;
        }
        
        // Sinon, comparer comme des chaînes
        return aVal.localeCompare(bVal);
    });
    
    // Réinsérer les lignes triées
    rows.forEach(row => tbody.appendChild(row));
}

/**
 * Filtre les lignes d'un tableau
 */
function filterTable(searchTerm, tableId = null) {
    const table = tableId ? document.getElementById(tableId) : document.querySelector('table');
    if (!table) return;
    
    const tbody = table.querySelector('tbody');
    const rows = tbody.querySelectorAll('tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const matches = text.includes(searchTerm.toLowerCase());
        row.style.display = matches ? '' : 'none';
    });
}

/**
 * Export de données (pour les rapports)
 */
function exportToCSV(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const rows = table.querySelectorAll('tr');
    const csv = [];
    
    rows.forEach(row => {
        const cells = row.querySelectorAll('th, td');
        const rowData = Array.from(cells).map(cell => 
            '"' + cell.textContent.replace(/"/g, '""') + '"'
        );
        csv.push(rowData.join(','));
    });
    
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// Export des fonctions utiles
window.GestionImmobiliere = {
    showNotification,
    calculateTotal,
    toggleDarkMode,
    sortTable,
    filterTable,
    exportToCSV
};
