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
        try {
            const response = await fetch(`${API_URL}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error('API POST Error:', error);
            return null;
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
