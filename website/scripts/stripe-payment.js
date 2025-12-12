// ============================================
// STRIPE PAYMENT INTEGRATION
// Anti-Lust Guardian - Payment Processing
// ============================================

// 🔑 YOUR STRIPE PUBLISHABLE KEY (LIVE MODE)
const STRIPE_PUBLISHABLE_KEY = 'pk_live_51SYnV2Ad7fQadcPJE44b9Q9T5tGVQvn0L95GJsc6GtVihBQy8KwWHtRMNRUyS6kSLkgxU2koyV9zZ2HWYp7FC76K00yQiuMG8T';

// Initialize Stripe
let stripe;

// Load Stripe.js
function loadStripe() {
    const script = document.createElement('script');
    script.src = 'https://js.stripe.com/v3/';
    script.onload = () => {
        stripe = Stripe(STRIPE_PUBLISHABLE_KEY);
        console.log('✅ Stripe loaded successfully');
    };
    document.head.appendChild(script);
}

// Call this when page loads
loadStripe();

// ============================================
// PRICING CONFIGURATION
// ============================================

const PRICING = {
    monthly: {
        priceId: 'price_YOUR_MONTHLY_PRICE_ID', // Replace with actual Stripe Price ID
        amount: 1000, // $10.00 in cents
        currency: 'usd',
        interval: 'month',
        trialDays: 7
    },
    lifetime: {
        priceId: 'price_YOUR_LIFETIME_PRICE_ID', // Replace with actual Stripe Price ID
        amount: 15000, // $150.00 in cents
        currency: 'usd',
        interval: 'one_time'
    }
};

// ============================================
// CHECKOUT FUNCTIONS
// ============================================

/**
 * Start Monthly Subscription Checkout
 */
async function startMonthlyCheckout() {
    // Check if user is logged in
    if (!window.isAuthenticated || !window.isAuthenticated()) {
        // Redirect to login, then come back here
        window.location.href = '/login.html?redirect=' + window.location.pathname + '%23pricing';
        return;
    }

    const user = window.getCurrentUser();

    if (!stripe) {
        alert('Payment system is loading, please wait...');
        return;
    }

    try {
        showLoading('Redirecting to checkout...');

        // Use Payment Link (easier method)
        if (PAYMENT_LINKS.monthly) {
            // Add user email as query parameter for Stripe to prefill
            const checkoutUrl = new URL(PAYMENT_LINKS.monthly);
            checkoutUrl.searchParams.append('prefilled_email', user.email);
            checkoutUrl.searchParams.append('client_reference_id', user.uid);
            window.location.href = checkoutUrl.toString();
            return;
        }

        // Fallback: Use Checkout Session API (requires backend)
        const response = await fetch('/api/create-checkout-session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                priceId: PRICING.monthly.priceId,
                mode: 'subscription',
                customerEmail: user.email,
                clientReferenceId: user.uid,
                successUrl: `${window.location.origin}/success.html?session_id={CHECKOUT_SESSION_ID}`,
                cancelUrl: `${window.location.origin}/index.html#pricing`,
            })
        });

        const session = await response.json();
        const result = await stripe.redirectToCheckout({ sessionId: session.id });

        if (result.error) {
            alert(result.error.message);
        }
    } catch (error) {
        console.error('Checkout error:', error);
        alert('Payment error. Please try again.');
    } finally {
        hideLoading();
    }
}

/**
 * Start Lifetime License Checkout
 */
async function startLifetimeCheckout() {
    // Check if user is logged in
    if (!window.isAuthenticated || !window.isAuthenticated()) {
        // Redirect to login, then come back here
        window.location.href = '/login.html?redirect=' + window.location.pathname + '%23pricing';
        return;
    }

    const user = window.getCurrentUser();

    if (!stripe) {
        alert('Payment system is loading, please wait...');
        return;
    }

    try {
        showLoading('Redirecting to checkout...');

        // Use Payment Link (easier method)
        if (PAYMENT_LINKS.lifetime) {
            const checkoutUrl = new URL(PAYMENT_LINKS.lifetime);
            checkoutUrl.searchParams.append('prefilled_email', user.email);
            checkoutUrl.searchParams.append('client_reference_id', user.uid);
            window.location.href = checkoutUrl.toString();
            return;
        }

        // Fallback: Use Checkout Session API (requires backend)
        const response = await fetch('/api/create-checkout-session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                priceId: PRICING.lifetime.priceId,
                mode: 'payment',
                customerEmail: user.email,
                clientReferenceId: user.uid,
                successUrl: `${window.location.origin}/success.html?session_id={CHECKOUT_SESSION_ID}`,
                cancelUrl: `${window.location.origin}/index.html#pricing`,
            })
        });

        const session = await response.json();
        const result = await stripe.redirectToCheckout({ sessionId: session.id });

        if (result.error) {
            alert(result.error.message);
        }
    } catch (error) {
        console.error('Checkout error:', error);
        alert('Payment error. Please try again.');
    } finally {
        hideLoading();
    }
}

// ============================================
// SIMPLIFIED CHECKOUT (Payment Links - Easier!)
// ============================================

/**
 * Alternative: Use Stripe Payment Links (No backend needed!)
 * This is MUCH easier for beginners
 */
const PAYMENT_LINKS = {
    monthly: 'https://buy.stripe.com/aFabJ01xP1jKeGvaaSbEA01', // $10/month with 7-day trial
    lifetime: 'https://buy.stripe.com/4gM7sKa4l6E441RaaSbEA02' // $150 one-time
};

/**
 * Simplified checkout using Payment Links
 */
function quickCheckoutMonthly() {
    window.location.href = PAYMENT_LINKS.monthly;
}

function quickCheckoutLifetime() {
    window.location.href = PAYMENT_LINKS.lifetime;
}

// ============================================
// UI HELPERS
// ============================================

function showLoading(message = 'Processing...') {
    // Create loading overlay
    const overlay = document.createElement('div');
    overlay.id = 'payment-loading';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        color: #00F3FF;
        font-size: 24px;
        font-family: 'Orbitron', sans-serif;
    `;
    overlay.innerHTML = `
        <div style="text-align: center;">
            <div style="font-size: 48px; margin-bottom: 20px;">⚡</div>
            <div>${message}</div>
        </div>
    `;
    document.body.appendChild(overlay);
}

function hideLoading() {
    const overlay = document.getElementById('payment-loading');
    if (overlay) {
        overlay.remove();
    }
}

// ============================================
// TEST CARD INFORMATION (for testing)
// ============================================

/*
TEST CARDS (Use in Test Mode):
Success: 4242 4242 4242 4242
Decline: 4000 0000 0000 0002
3D Secure: 4000 0025 0000 3155

Expiry: Any future date (e.g., 12/34)
CVC: Any 3 digits (e.g., 123)
ZIP: Any 5 digits (e.g., 12345)
*/

console.log('💳 Stripe Payment Module Loaded');
console.log('📝 Remember to replace API keys before going live!');

/**
 * Unified subscription handler called from HTML
 */
function handleSubscription(plan) {
    if (plan === 'monthly') {
        startMonthlyCheckout();
    } else if (plan === 'lifetime') {
        startLifetimeCheckout();
    }
}

// Make globally available
window.handleSubscription = handleSubscription;
window.startMonthlyCheckout = startMonthlyCheckout;
window.startLifetimeCheckout = startLifetimeCheckout;
