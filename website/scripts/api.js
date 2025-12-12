const API_URL = '/api';

const api = {
    async get(endpoint) {
        try {
            const response = await fetch(`${API_URL}${endpoint}`);
            return await response.json();
        } catch (error) {
            console.error('API GET Error:', error);
            return null;
        }
    },

    async post(endpoint, data) {
        // CSRF Protection
        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;

        try {
            const headers = {
                'Content-Type': 'application/json'
            };
            if (csrfToken) {
                headers['X-CSRF-Token'] = csrfToken;
            }

            const response = await fetch(`${API_URL}${endpoint}`, {
                method: 'POST',
                headers: headers,
                credentials: 'include', // Send cookies
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error('API POST Error:', error);
            return null;
        }
    },

    // Security Utilities
    utils: {
        sanitize(input) {
            if (typeof input !== 'string') return input;
            return input.replace(/[<>\"'&]/g, '');
        },
        escapeHtml(unsafe) {
            if (typeof unsafe !== 'string') return unsafe;
            return unsafe
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        },
        rateLimiter: {
            calls: {},
            isAllowed(key, maxCalls = 3, windowMs = 60000) {
                const now = Date.now();
                if (!this.calls[key]) this.calls[key] = [];
                this.calls[key] = this.calls[key].filter(time => now - time < windowMs);
                if (this.calls[key].length >= maxCalls) return false;
                this.calls[key].push(now);
                return true;
            }
        }
    },

    stats: {
        async getToday() {
            return await api.get('/stats/today');
        },
        async getWeekly() {
            return await api.get('/stats/weekly');
        }
    },

    parent: {
        async getStatus() {
            return await api.get('/parent/status');
        },
        async pair(code) {
            return await api.post('/parent/pair', { code });
        },
        async generateCode() {
            return await api.post('/parent/generate-code', {});
        },
        async getChildren() {
            return await api.get('/parent/children');
        }
    },

    emergency: {
        async toggle(enabled) {
            return await api.post('/emergency-mode', { enabled });
        }
    },

    settings: {
        async update(settings) {
            return await api.post('/settings', settings);
        },
        async get() {
            return await api.get('/settings');
        }
    },

    reports: {
        async generateMonthly() {
            return await api.post('/reports/monthly', {});
        },
        async getLatest() {
            return await api.get('/reports/latest');
        }
    }
};
