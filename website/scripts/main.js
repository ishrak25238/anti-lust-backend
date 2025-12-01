// ===================================================================
// ANTI-LUST GUARDIAN - MAIN JAVASCRIPT
// Handles all interactive features and animations
// ===================================================================

// ===== GLOBAL STATE =====
const AppState = {
    isHeaderScrolled: false,
    currentPricingMode: 'monthly',
    stats: {
        streak: 0,
        threats: 142,
        clarity: 15
    },
    animationFrameId: null
};

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
    console.log('[ANTI-LUST GUARDIAN] Initializing...');

    initializeStarfield();
    initializeHeader();
    initializePricing();
    initializeDashboard();
    initializeCustomCursor();
    initializeScrollAnimations();
    initializeFormValidation();

    console.log('[ANTI-LUST GUARDIAN] System fully operational');
});

// ===== STARFIELD ANIMATION =====
function initializeStarfield() {
    const canvas = document.getElementById('starfield');
    if (!canvas) {
        console.warn('Starfield canvas not found');
        return;
    }

    const ctx = canvas.getContext('2d');
    let width, height;
    let stars = [];

    function

        resizeCanvas() {
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
        initStars();
    }

    function initStars() {
        stars = [];
        const starCount = Math.floor((width * height) / 10000);

        for (let i = 0; i < starCount; i++) {
            stars.push({
                x: Math.random() * width,
                y: Math.random() * height,
                z: Math.random() * 2 + 0.5,
                size: Math.random() * 2,
                speed: Math.random() * 0.5 + 0.1,
                opacity: Math.random() * 0.5 + 0.5
            });
        }
    }

    function animateStars() {
        ctx.fillStyle = '#030014';
        ctx.fillRect(0, 0, width, height);

        stars.forEach((star, index) => {
            // Move star
            star.y += star.speed * star.z;

            // Reset if out of bounds
            if (star.y > height) {
                star.y = 0;
                star.x = Math.random() * width;
            }

            // Calculate brightness
            const brightness = Math.min(1, star.z / 2) * star.opacity;

            // Draw star
            ctx.fillStyle = `rgba(255, 255, 255, ${brightness})`;
            ctx.beginPath();
            ctx.arc(star.x, star.y, star.size * (star.z / 2), 0, Math.PI * 2);
            ctx.fill();

            // Draw connection lines for nearby stars (Neural network effect)
            if (star.z > 1.5) {
                for (let j = index + 1; j < stars.length; j++) {
                    const otherStar = stars[j];

                    if (otherStar.z > 1.5) {
                        const dx = star.x - otherStar.x;
                        const dy = star.y - otherStar.y;
                        const dist = Math.sqrt(dx * dx + dy * dy);

                        if (dist < 100) {
                            const connectionOpacity = 0.1 * (1 - dist / 100);
                            ctx.strokeStyle = `rgba(0, 243, 255, ${connectionOpacity})`;
                            ctx.lineWidth = 0.5;
                            ctx.beginPath();
                            ctx.moveTo(star.x, star.y);
                            ctx.lineTo(otherStar.x, otherStar.y);
                            ctx.stroke();
                        }
                    }
                }
            }
        });

        AppState.animationFrameId = requestAnimationFrame(animateStars);
    }

    // Start animation
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();
    animateStars();

    console.log('[Starfield] Initialized with', stars.length, 'stars');
}

// ===== HEADER SCROLL EFFECT =====
function initializeHeader() {
    const header = document.getElementById('header');
    if (!header) return;

    let lastScrollY = window.scrollY;
    let ticking = false;

    function updateHeader() {
        const scrollY = window.scrollY;

        if (scrollY > 50 && !AppState.isHeaderScrolled) {
            header.classList.add('scrolled');
            AppState.isHeaderScrolled = true;
        } else if (scrollY <= 50 && AppState.isHeaderScrolled) {
            header.classList.remove('scrolled');
            AppState.isHeaderScrolled = false;
        }

        lastScrollY = scrollY;
        ticking = false;
    }

    function requestTick() {
        if (!ticking) {
            window.requestAnimationFrame(updateHeader);
            ticking = true;
        }
    }

    window.addEventListener('scroll', requestTick, { passive: true });
    console.log('[Header] Scroll detection initialized');
}

// ===== CUSTOM CURSOR =====
function initializeCustomCursor() {
    const cursor = document.getElementById('cursor');
    const cursorDot = document.getElementById('cursor-dot');

    if (!cursor || !cursorDot) {
        console.warn('Custom cursor elements not found');
        return;
    }

    // Activate custom cursor
    document.body.classList.add('custom-cursor-active');

    let mouseX = 0;
    let mouseY = 0;
    let cursorX = 0;
    let cursorY = 0;

    // Track mouse position
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;

        // Dot follows instantly
        cursorDot.style.left = mouseX + 'px';
        cursorDot.style.top = mouseY + 'px';
    });

    // Smooth cursor animation
    function animateCursor() {
        const speed = 0.15;

        cursorX += (mouseX - cursorX) * speed;
        cursorY += (mouseY - cursorY) * speed;

        cursor.style.left = cursorX + 'px';
        cursor.style.top = cursorY + 'px';

        requestAnimationFrame(animateCursor);
    }

    animateCursor();

    // Hover effects
    const hoverElements = document.querySelectorAll('a, button, .card, .pricing-card, .btn');
    hoverElements.forEach(el => {
        el.addEventListener('mouseenter', () => cursor.classList.add('hovered'));
        el.addEventListener('mouseleave', () => cursor.classList.remove('hovered'));
    });

    console.log('[Cursor] Custom cursor initialized');
}

// ===== PRICING TOGGLE =====
function initializePricing() {
    const toggle = document.getElementById('pricing-switch');
    const monthlyLabel = document.getElementById('monthly-label');
    const lifetimeLabel = document.getElementById('lifetime-label');
    const cardMonthly = document.getElementById('card-monthly');
    const cardLifetime = document.getElementById('card-lifetime');

    if (!toggle) {
        console.warn('Pricing toggle not found');
        return;
    }

    toggle.addEventListener('change', () => {
        if (toggle.checked) {
            // Lifetime selected
            AppState.currentPricingMode = 'lifetime';
            monthlyLabel.classList.remove('active');
            lifetimeLabel.classList.add('active');

            if (cardMonthly && cardLifetime) {
                cardMonthly.style.opacity = '0.5';
                cardMonthly.style.transform = 'scale(0.95)';
                cardLifetime.style.opacity = '1';
                cardLifetime.style.transform = 'scale(1.05)';
                cardLifetime.classList.add('featured');
                cardMonthly.classList.remove('featured');
            }
        } else {
            // Monthly selected
            AppState.currentPricingMode = 'monthly';
            lifetimeLabel.classList.remove('active');
            monthlyLabel.classList.add('active');

            if (cardMonthly && cardLifetime) {
                cardLifetime.style.opacity = '0.5';
                cardLifetime.style.transform = 'scale(0.95)';
                cardMonthly.style.opacity = '1';
                cardMonthly.style.transform = 'scale(1.05)';
                cardMonthly.classList.add('featured');
                cardLifetime.classList.remove('featured');
            }
        }

        console.log('[Pricing] Switched to', AppState.currentPricingMode);
    });

    // Initialize monthly as default
    if (cardMonthly) {
        cardMonthly.classList.add('featured');
    }
    if (cardLifetime) {
        cardLifetime.style.opacity = '0.5';
        cardLifetime.style.transform = 'scale(0.95)';
    }

    console.log('[Pricing] Toggle initialized');
}

// ===== DASHBOARD STATS =====
function initializeDashboard() {
    const streakDisplay = document.getElementById('streak-display');
    const threatsDisplay = document.getElementById('threats-display');
    const clarityDisplay = document.getElementById('clarity-display');
    const resetBtn = document.getElementById('reset-streak-btn');

    if (!streakDisplay) {
        console.warn('Dashboard elements not found');
        return;
    }

    // Load stats from localStorage
    function loadStats() {
        let stats = JSON.parse(localStorage.getItem('anti_lust_stats'));

        if (!stats) {
            stats = {
                streak: 0,
                threats: 142,
                clarity: 15
            };
            localStorage.setItem('anti_lust_stats', JSON.stringify(stats));
        }

        AppState.stats = stats;
        updateDisplays();
    }

    function updateDisplays() {
        if (streakDisplay) streakDisplay.textContent = AppState.stats.streak;
        if (threatsDisplay) threatsDisplay.textContent = AppState.stats.threats;
        if (clarityDisplay) clarityDisplay.textContent = AppState.stats.clarity + '%';
    }

    function saveStats() {
        localStorage.setItem('anti_lust_stats', JSON.stringify(AppState.stats));
    }

    // Reset button
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            if (confirm('WARNING: Are you sure you want to reset your streak? This action cannot be undone.')) {
                AppState.stats.streak = 0;
                AppState.stats.threats = 142;
                AppState.stats.clarity = 15;
                saveStats();
                updateDisplays();

                showNotification('Streak reset. Begin again, Commander.', 'warning');
                console.log('[Dashboard] Streak reset');
            }
        });
    }

    // Simulate live updates
    setInterval(() => {
        if (Math.random() > 0.8) {
            AppState.stats.threats += 1;
            if (AppState.stats.clarity < 95) {
                AppState.stats.clarity += Math.floor(Math.random() * 2);
            }
            saveStats();
            updateDisplays();
        }
    }, 3000);

    loadStats();
    console.log('[Dashboard] Initialized with stats:', AppState.stats);
}

// ===== SCROLL ANIMATIONS =====
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all cards and features
    const animateElements = document.querySelectorAll('.card, .feature-item, .pricing-card');
    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Add animate-in class styles
    const style = document.createElement('style');
    style.textContent = `
        .animate-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(style);

    console.log('[Animations] Scroll observer initialized for', animateElements.length, 'elements');
}

// ===== FORM VALIDATION =====
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();

            const inputs = form.querySelectorAll('input[required], textarea[required]');
            let isValid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.style.borderColor = '#FF2A6D';
                    showNotification(`Please fill in: ${input.name || 'required field'}`, 'error');
                } else {
                    input.style.borderColor = '';
                }
            });

            if (isValid) {
                showNotification('Form submitted successfully!', 'success');
                form.reset();
                console.log('[Form] Validation passed');
            }
        });
    });

    console.log('[Forms]', forms.length, 'forms validated');
}

// ===== NOTIFICATION SYSTEM =====
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? '#00FF88' : type === 'error' ? '#FF2A6D' : '#00F3FF'};
        color: #030014;
        padding: 16px 24px;
        border-radius: 8px;
        font-weight: 700;
        z-index: 10000;
        animation: slideInRight 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add notification animations
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(notificationStyles);

// ===== PERFORMANCE MONITORING =====
const performanceMonitor = {
    startTime: Date.now(),

    log() {
        const loadTime = Date.now() - this.startTime;
        console.log(`[Performance] Page fully loaded in ${loadTime}ms`);

        if (performance.memory) {
            console.log('[Performance] Memory usage:', {
                used: `${(performance.memory.usedJSHeapSize / 1048576).toFixed(2)} MB`,
                total: `${(performance.memory.totalJSHeapSize / 1048576).toFixed(2)} MB`,
                limit: `${(performance.memory.jsHeapSizeLimit / 1048576).toFixed(2)} MB`
            });
        }
    }
};

window.addEventListener('load', () => {
    performanceMonitor.log();
});

// ===== ANALYTICS (Placeholder for Google Analytics, etc.) =====
const Analytics = {
    track(event, data = {}) {
        console.log('[Analytics]', event, data);

        // Example: Send to Google Analytics
        // if (window.gtag) {
        //     gtag('event', event, data);
        // }
    },

    pageView(page) {
        this.track('page_view', { page });
    },

    buttonClick(buttonName) {
        this.track('button_click', { button: buttonName });
    }
};

// Track page view on load
window.addEventListener('load', () => {
    Analytics.pageView(window.location.pathname);
});

// ===== SMOOTH SCROLLING FOR ANCHOR LINKS =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');

        if (href === '#') return;

        e.preventDefault();
        const target = document.querySelector(href);

        if (target) {
            const headerOffset = 80;
            const elementPosition = target.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });

            Analytics.track('anchor_click', { target: href });
        }
    });
});

// ===== KEYBOARD SHORTCUTS =====
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K: Focus search (if exists)
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[type="search"]');
        if (searchInput) searchInput.focus();
    }

    // ESC: Close modals (if exists)
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.open');
        modals.forEach(modal => modal.classList.remove('open'));
    }
});

// ===== DARK MODE TOGGLE (Optional Future Feature) =====
const DarkMode = {
    toggle() {
        document.body.classList.toggle('light-mode');
        const isLight = document.body.classList.contains('light-mode');
        localStorage.setItem('theme', isLight ? 'light' : 'dark');
        console.log('[Theme] Switched to', isLight ? 'light' : 'dark', 'mode');
    },

    init() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'light') {
            document.body.classList.add('light-mode');
        }
    }
};

// ===== ERROR HANDLING =====
window.addEventListener('error', (e) => {
    console.error('[Global Error]', e.error);

    // Show user-friendly error in development
    if (window.location.hostname === 'localhost') {
        showNotification('An error occurred. Check console for details.', 'error');
    }
});

// ===== EXPORT FOR DEBUGGING =====
if (window.location.hostname === 'localhost') {
    window.AntiLustDebug = {
        AppState,
        Analytics,
        DarkMode,
        showNotification,
        performanceMonitor
    };
    console.log('[Debug] Debug utilities available at window.AntiLustDebug');
}

// ===== SERVICE WORKER REGISTRATION (For PWA) =====
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Uncomment when service worker is ready
        // navigator.serviceWorker.register('/sw.js')
        //     .then(reg => console.log('[ServiceWorker] Registered'))
        //     .catch(err => console.error('[ServiceWorker] Registration failed:', err));
    });
}

console.log('[ANTI-LUST GUARDIAN] All systems operational ✓');
