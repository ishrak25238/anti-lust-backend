// ============================================
// DASHBOARD LOGIC
// Handles real data fetching and UI updates
// ============================================

import { signOutUser, getUserProfile } from './auth.js';

document.addEventListener('DOMContentLoaded', async () => {
    console.log('🛡️ Dashboard initializing...');

    // 1. Initialize User Info
    await initializeUser();

    // 2. Load Real Stats
    await loadDashboardStats();

    // 3. Initialize Controls
    initializeControls();

    console.log('✅ Dashboard ready');
});

// ===== USER INITIALIZATION =====
async function initializeUser() {
    // Wait for auth to be ready (handled by auth.js requireAuth, but double check)
    const userEmailEl = document.getElementById('userEmail');

    // We can get the user profile from auth.js global or wait for it
    // auth.js sets window.currentUser when auth changes

    // Simple polling to wait for auth if needed, though requireAuth should handle redirect
    const checkAuth = setInterval(async () => {
        if (window.auth && window.auth.currentUser) {
            clearInterval(checkAuth);
            const user = window.auth.currentUser;
            if (userEmailEl) {
                userEmailEl.textContent = user.email;
            }

            // Load profile from Firestore
            try {
                const profile = await window.getUserProfile(user.uid);
                if (profile && profile.subscriptionStatus === 'active') {
                    document.querySelector('.status-indicator').style.background = '#00FF94'; // Green
                    document.querySelector('.subtitle').textContent = 'Premium Protection Active';
                }
            } catch (e) {
                console.error('Error loading profile:', e);
            }
        }
    }, 500);
}

// ===== STATS LOADING =====
async function loadDashboardStats() {
    try {
        // Fetch real stats from backend API
        // Note: api.js is loaded globally in dashboard.html

        const todayStats = await api.stats.getToday();

        if (todayStats) {
            updateStat('threatsBlocked', todayStats.threats_blocked || 0);
            updateStat('timeSaved', todayStats.time_saved_minutes || 0);
            updateStat('currentStreak', todayStats.streak_days || 0);
            updateStat('aiConfidence', (todayStats.ai_confidence || 99.5) + '%');
        } else {
            // Fallback if API fails (or is offline)
            console.warn('Could not fetch stats, using local cache or defaults');
            const cached = JSON.parse(localStorage.getItem('anti_lust_stats'));
            if (cached) {
                updateStat('threatsBlocked', cached.threats);
                updateStat('currentStreak', cached.streak);
            }
        }

    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function updateStat(id, value) {
    const el = document.getElementById(id);
    if (el) {
        // Animate number
        el.textContent = value;
        el.classList.add('pulse-text');
        setTimeout(() => el.classList.remove('pulse-text'), 500);
    }
}

// ===== CONTROLS =====
function initializeControls() {
    // Parent Link Button
    window.showParentLink = () => {
        document.getElementById('parent').scrollIntoView({ behavior: 'smooth' });
    };

    // Emergency Mode
    window.toggleEmergencyMode = async () => {
        const btn = document.querySelector('button[onclick="toggleEmergencyMode()"]');
        const status = document.getElementById('emergencyStatus');

        if (!btn || !status) return;

        const isCurrentlyOn = status.textContent === 'ON';
        const newState = !isCurrentlyOn;

        // Call API
        const result = await api.emergency.toggle(newState);

        if (result && result.success) {
            status.textContent = newState ? 'ON' : 'OFF';
            status.style.color = newState ? '#FF2A6D' : '#94A3B8';
            btn.classList.toggle('active', newState);

            if (newState) {
                alert('🚨 EMERGENCY MODE ACTIVATED 🚨\nStrict filtering enabled. All non-essential traffic blocked.');
            }
        } else {
            alert('Failed to toggle Emergency Mode. Check connection.');
        }
    };

    // Generate Report
    window.generateReport = async () => {
        const btn = document.querySelector('button[onclick="generateReport()"]');
        const originalText = btn.innerHTML;

        btn.innerHTML = '<div class="btn-label">Generating...</div>';
        btn.disabled = true;

        try {
            await api.reports.generateMonthly();
            alert('Report generated and sent to your email.');
        } catch (e) {
            console.error(e);
            alert('Error generating report.');
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    };

    // Sign Out
    // Add sign out button to nav if not present
    const navLinks = document.querySelector('.nav-links');
    if (navLinks && !document.getElementById('logoutBtn')) {
        const logoutLink = document.createElement('a');
        logoutLink.href = "#";
        logoutLink.className = "nav-link";
        logoutLink.id = "logoutBtn";
        logoutLink.textContent = "Sign Out";
        logoutLink.onclick = async (e) => {
            e.preventDefault();
            await signOutUser();
        };
        navLinks.appendChild(logoutLink);
    }
}

// ===== PARENTAL CONTROLS =====
window.generatePairingCode = async () => {
    // Security: Rate Limiting
    if (!api.utils.rateLimiter.isAllowed('generateCode', 3, 60000)) {
        alert('Too many requests. Please wait 1 minute.');
        return;
    }

    const display = document.getElementById('generatedCode');
    display.textContent = 'Generating...';

    const result = await api.parent.generateCode();
    if (result && result.code) {
        display.textContent = result.code;
        display.classList.add('active');
    } else {
        display.textContent = 'Error';
    }
};

window.pairAccount = async () => {
    const input = document.getElementById('pairingCode');
    let code = input.value.trim();

    if (!code) return alert('Please enter a code');

    // Security: Validate and Sanitize
    // Assuming 6-char alphanumeric code (adjust regex if backend differs)
    // if (!/^[A-Z0-9]{6}$/.test(code)) return alert('Invalid code format');

    code = api.utils.sanitize(code);

    const result = await api.parent.pair(code);
    if (result && result.success) {
        alert('✅ Account linked successfully!');
        input.value = '';
        // Refresh child list
        loadChildren();
    } else {
        alert('❌ Linking failed. Invalid code.');
    }
};

async function loadChildren() {
    const list = document.getElementById('childAccounts');
    if (!list) return;

    const children = await api.parent.getChildren();
    if (children && children.length > 0) {
        list.innerHTML = children.map(child => `
            <div class="child-item glass">
                <span>${api.utils.escapeHtml(child.email)}</span>
                <span class="status-badge active">Protected</span>
            </div>
        `).join('');
    } else {
        list.innerHTML = '<div class="empty-state">No accounts linked</div>';
    }
}
