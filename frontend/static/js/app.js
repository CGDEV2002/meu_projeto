// Utilitários e configuração global
class API {
    constructor() {
        this.baseURL = '';
        this.token = localStorage.getItem('token');
    }

    setToken(token) {
        this.token = token;
        localStorage.setItem('token', token);
    }

    removeToken() {
        this.token = null;
        localStorage.removeItem('token');
    }

    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        return headers;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: this.getHeaders(),
            ...options,
        };

        try {
            const response = await fetch(url, config);
            
            if (response.status === 401) {
                this.removeToken();
                window.location.href = '/login';
                return null;
            }

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail || 'Erro na requisição');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    async get(endpoint) {
        return this.request(endpoint);
    }

    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    async delete(endpoint) {
        return this.request(endpoint, {
            method: 'DELETE',
        });
    }
}

// Instância global da API
const api = new API();

// Utilitários
const utils = {
    formatCurrency: (value) => {
        if (!value) return 'Preço a consultar';
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    },

    formatDate: (dateString) => {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleDateString('pt-BR');
    },

    formatPhone: (phone) => {
        if (!phone) return '';
        // Remove todos os caracteres não numéricos
        const cleaned = phone.replace(/\D/g, '');
        
        // Formata como (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
        if (cleaned.length === 11) {
            return cleaned.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
        } else if (cleaned.length === 10) {
            return cleaned.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
        }
        return phone;
    },

    getWhatsAppLink: (phone, message = '') => {
        const cleaned = phone.replace(/\D/g, '');
        const formattedPhone = cleaned.startsWith('55') ? cleaned : `55${cleaned}`;
        const encodedMessage = encodeURIComponent(message);
        return `https://wa.me/${formattedPhone}${message ? `?text=${encodedMessage}` : ''}`;
    },

    getStatusBadge: (status) => {
        const statusMap = {
            available: { class: 'status-available', text: 'Disponível' },
            sold: { class: 'status-sold', text: 'Vendido' },
            reserved: { class: 'status-reserved', text: 'Reservado' }
        };
        return statusMap[status] || { class: 'status-available', text: status };
    },

    getNegotiationStatusBadge: (status) => {
        const statusMap = {
            interested: { class: 'status-available', text: 'Interessado' },
            negotiating: { class: 'status-reserved', text: 'Negociando' },
            closed: { class: 'status-sold', text: 'Fechado' },
            lost: { class: 'status-sold', text: 'Perdido' }
        };
        return statusMap[status] || { class: 'status-available', text: status };
    }
};

// Gerenciador de modals
const modal = {
    show: (modalId) => {
        const modalElement = document.getElementById(modalId);
        if (modalElement) {
            modalElement.classList.add('show');
            document.body.style.overflow = 'hidden';
        }
    },

    hide: (modalId) => {
        const modalElement = document.getElementById(modalId);
        if (modalElement) {
            modalElement.classList.remove('show');
            document.body.style.overflow = 'auto';
        }
    },

    hideAll: () => {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.classList.remove('show');
        });
        document.body.style.overflow = 'auto';
    }
};

// Gerenciador de alertas
const alert = {
    show: (message, type = 'info') => {
        // Remove alertas existentes
        document.querySelectorAll('.alert').forEach(alert => alert.remove());

        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;

        // Adiciona no topo da página
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(alertDiv, container.firstChild);
        }

        // Remove automaticamente após 5 segundos
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    },

    success: (message) => alert.show(message, 'success'),
    error: (message) => alert.show(message, 'error'),
    info: (message) => alert.show(message, 'info')
};

// Loading helper
const loading = {
    show: (container) => {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'loading';
        loadingDiv.innerHTML = '<div class="spinner"></div>';
        loadingDiv.id = 'loading-indicator';
        
        if (typeof container === 'string') {
            container = document.querySelector(container);
        }
        
        if (container) {
            container.appendChild(loadingDiv);
        }
    },

    hide: () => {
        const loadingElement = document.getElementById('loading-indicator');
        if (loadingElement) {
            loadingElement.remove();
        }
    }
};

// Event listeners globais
document.addEventListener('DOMContentLoaded', function() {
    // Fechar modais clicando no fundo
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            modal.hideAll();
        }
    });

    // Fechar modais com ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            modal.hideAll();
        }
    });

    // Verificar autenticação em páginas protegidas
    const currentPage = window.location.pathname;
    const protectedPages = ['/dashboard', '/car/', '/client/'];
    const isProtectedPage = protectedPages.some(page => currentPage.startsWith(page));
    
    if (isProtectedPage && !api.token) {
        window.location.href = '/login';
    }

    // Configurar navegação
    setupNavigation();
});

// Configurar navegação
function setupNavigation() {
    // Logout
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            api.removeToken();
            window.location.href = '/login';
        });
    }

    // Botões de fechar modal
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', function() {
            modal.hideAll();
        });
    });
}

// Validação de formulários
const validation = {
    required: (value) => value && value.trim() !== '',
    email: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
    phone: (value) => /^[\d\s\(\)\-\+]{10,}$/.test(value),
    
    validateForm: (formData, rules) => {
        const errors = {};
        
        for (const [field, validators] of Object.entries(rules)) {
            const value = formData[field];
            
            for (const validator of validators) {
                if (typeof validator === 'string') {
                    // Validador pré-definido
                    if (!validation[validator](value)) {
                        errors[field] = `Campo ${field} é inválido`;
                        break;
                    }
                } else if (typeof validator === 'function') {
                    // Validador personalizado
                    const result = validator(value);
                    if (result !== true) {
                        errors[field] = result;
                        break;
                    }
                }
            }
        }
        
        return Object.keys(errors).length === 0 ? null : errors;
    },

    showFieldErrors: (errors) => {
        // Remove erros anteriores
        document.querySelectorAll('.field-error').forEach(el => el.remove());
        
        // Mostra novos erros
        for (const [field, message] of Object.entries(errors)) {
            const input = document.querySelector(`[name="${field}"]`);
            if (input) {
                const errorDiv = document.createElement('div');
                errorDiv.className = 'field-error';
                errorDiv.style.color = '#dc2626';
                errorDiv.style.fontSize = '0.8rem';
                errorDiv.style.marginTop = '0.25rem';
                errorDiv.textContent = message;
                
                input.parentNode.appendChild(errorDiv);
                input.style.borderColor = '#dc2626';
            }
        }
    },

    clearFieldErrors: () => {
        document.querySelectorAll('.field-error').forEach(el => el.remove());
        document.querySelectorAll('input, select, textarea').forEach(el => {
            el.style.borderColor = '';
        });
    }
};