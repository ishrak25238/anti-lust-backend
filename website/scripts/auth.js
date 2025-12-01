// ============================================
// FIREBASE AUTHENTICATION MODULE
// Anti-Lust Guardian - User Authentication
// ============================================

// 🔥 FIREBASE CONFIG - REPLACE WITH YOUR ACTUAL CONFIG
const firebaseConfig = {
    apiKey: "YOUR_API_KEY_HERE",
    authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_PROJECT_ID.appspot.com",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
};

// Initialize Firebase
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js';
import {
    getAuth,
    signInWithPopup,
    signOut,
    GoogleAuthProvider,
    onAuthStateChanged,
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword
} from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js';
import {
    getFirestore,
    doc,
    setDoc,
    getDoc,
    updateDoc,
    serverTimestamp
} from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const googleProvider = new GoogleAuthProvider();

console.log('🔥 Firebase initialized');

// ============================================
// AUTHENTICATION FUNCTIONS
// ============================================

/**
 * Sign in with Google
 */
async function signInWithGoogle() {
    try {
        const result = await signInWithPopup(auth, googleProvider);
        const user = result.user;

        console.log('✅ Signed in:', user.email);

        // Create/update user profile
        await createUserProfile(user);

        // Check if user came from pricing (plan parameter)
        const urlParams = new URLSearchParams(window.location.search);
        const plan = urlParams.get('plan');

        if (plan) {
            // User wants to subscribe - redirect to Stripe with their email
            const PAYMENT_LINKS = {
                monthly: 'https://buy.stripe.com/aFabJ01xP1jKeGvaaSbEA01',
                lifetime: 'https://buy.stripe.com/4gM7sKa4l6E441RaaSbEA02'
            };

            const paymentUrl = new URL(PAYMENT_LINKS[plan] || PAYMENT_LINKS.monthly);
            paymentUrl.searchParams.append('prefilled_email', user.email);
            paymentUrl.searchParams.append('client_reference_id', user.uid);

            console.log('🔗 Redirecting to payment:', plan);
            window.location.href = paymentUrl.toString();
            return user;
        }

        // No plan - just go to dashboard
        const redirect = urlParams.get('redirect') || '/dashboard.html';
        window.location.href = redirect;

        return user;
    } catch (error) {
        console.error('❌ Sign in error:', error);
        alert('Sign in failed: ' + error.message);
        throw error;
    }
}

/**
 * Sign in with Email and Password
 */
async function signInWithEmail(email, password) {
    try {
        const result = await signInWithEmailAndPassword(auth, email, password);
        const user = result.user;

        console.log('✅ Signed in:', user.email);

        // Check if user came from pricing (plan parameter)
        const urlParams = new URLSearchParams(window.location.search);
        const plan = urlParams.get('plan');

        if (plan) {
            // User wants to subscribe - redirect to Stripe
            const PAYMENT_LINKS = {
                monthly: 'https://buy.stripe.com/aFabJ01xP1jKeGvaaSbEA01',
                lifetime: 'https://buy.stripe.com/4gM7sKa4l6E441RaaSbEA02'
            };

            const paymentUrl = new URL(PAYMENT_LINKS[plan] || PAYMENT_LINKS.monthly);
            paymentUrl.searchParams.append('prefilled_email', user.email);
            paymentUrl.searchParams.append('client_reference_id', user.uid);

            console.log('🔗 Redirecting to payment:', plan);
            window.location.href = paymentUrl.toString();
            return user;
        }

        const redirect = urlParams.get('redirect') || '/dashboard.html';
        window.location.href = redirect;

        return user;
    } catch (error) {
        console.error('❌ Sign in error:', error);
        alert('Sign in failed: ' + error.message);
        throw error;
    }
}

/**
 * Register with Email and Password
 */
async function registerWithEmail(email, password) {
    try {
        const result = await createUserWithEmailAndPassword(auth, email, password);
        const user = result.user;

        console.log('✅ Registered:', user.email);

        // Create user profile
        await createUserProfile(user);

        const redirect = new URLSearchParams(window.location.search).get('redirect') || '/dashboard.html';
        window.location.href = redirect;

        return user;
    } catch (error) {
        console.error('❌ Registration error:', error);
        alert('Registration failed: ' + error.message);
        throw error;
    }
}

/**
 * Sign out
 */
async function signOutUser() {
    try {
        await signOut(auth);
        console.log('✅ Signed out');
        window.location.href = '/index.html';
    } catch (error) {
        console.error('❌ Sign out error:', error);
        alert('Sign out failed: ' + error.message);
    }
}

// ============================================
// USER PROFILE MANAGEMENT
// ============================================

/**
 * Create or update user profile in Firestore
 */
async function createUserProfile(user) {
    const userRef = doc(db, 'users', user.uid);
    const userDoc = await getDoc(userRef);

    const userData = {
        email: user.email,
        displayName: user.displayName || user.email.split('@')[0],
        photoURL: user.photoURL || '',
        lastLogin: serverTimestamp()
    };

    if (!userDoc.exists()) {
        // New user - create profile
        userData.createdAt = serverTimestamp();
        userData.subscription = {
            type: null,
            status: 'none',
            stripeCustomerId: null,
            subscriptionId: null,
            startedAt: null
        };

        await setDoc(userRef, userData);
        console.log('✅ User profile created');
    } else {
        // Existing user - update last login
        await updateDoc(userRef, { lastLogin: serverTimestamp() });
        console.log('✅ User profile updated');
    }
}

/**
 * Get user profile data
 */
async function getUserProfile(uid) {
    const userRef = doc(db, 'users', uid);
    const userDoc = await getDoc(userRef);

    if (userDoc.exists()) {
        return userDoc.data();
    }
    return null;
}

/**
 * Update user subscription info
 */
async function updateUserSubscription(uid, subscriptionData) {
    const userRef = doc(db, 'users', uid);
    await updateDoc(userRef, {
        subscription: subscriptionData,
        'subscription.updatedAt': serverTimestamp()
    });
    console.log('✅ Subscription updated');
}

// ============================================
// AUTH STATE LISTENER
// ============================================

/**
 * Listen to auth state changes
 */
function onAuthChange(callback) {
    return onAuthStateChanged(auth, callback);
}

/**
 * Get current user
 */
function getCurrentUser() {
    return auth.currentUser;
}

/**
 * Check if user is authenticated
 */
function isAuthenticated() {
    return !!auth.currentUser;
}

/**
 * Require authentication (redirect if not logged in)
 */
function requireAuth(redirectTo = '/login.html') {
    onAuthStateChanged(auth, async (user) => {
        if (!user) {
            const currentPath = window.location.pathname;
            window.location.href = `${redirectTo}?redirect=${currentPath}`;
        } else {
            // User is logged in, check subscription
            await checkSubscription(user);
        }
    });
}

/**
 * Check if user has active subscription
 */
async function checkSubscription(user) {
    // Skip check for login page or pricing page
    if (window.location.pathname.includes('login.html') ||
        window.location.pathname.includes('index.html')) {
        return;
    }

    const userProfile = await getUserProfile(user.uid);

    // If no profile or no active subscription, redirect to pricing
    if (!userProfile ||
        !userProfile.subscription ||
        userProfile.subscription.status !== 'active') {

        console.log('⚠️ No active subscription found. Redirecting to pricing...');

        // Allow grace period or free tier if needed, but for now ENFORCE PAYMENT
        // Redirect to index.html#pricing
        window.location.href = '/index.html#pricing';
    }
}

// ============================================
// UI HELPERS
// ============================================

/**
 * Display user info in UI
 */
function displayUserInfo(elementId = 'userInfo') {
    const user = getCurrentUser();
    const element = document.getElementById(elementId);

    if (element && user) {
        element.innerHTML = `
            <div class="user-profile">
                ${user.photoURL ? `<img src="${user.photoURL}" alt="Profile" class="user-avatar">` : ''}
                <div>
                    <div class="user-name">${user.displayName || user.email}</div>
                    <div class="user-email">${user.email}</div>
                </div>
            </div>
        `;
    }
}

/**
 * Show loading state
 */
function showAuthLoading(message = 'Authenticating...') {
    const overlay = document.createElement('div');
    overlay.id = 'auth-loading';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        color: #00F3FF;
        font-size: 20px;
        font-family: 'Orbitron', sans-serif;
    `;
    overlay.innerHTML = `
        <div style="text-align: center;">
            <div style="font-size: 48px; margin-bottom: 20px; animation: pulse 1s infinite;">🔐</div>
            <div>${message}</div>
        </div>
    `;
    document.body.appendChild(overlay);
}

function hideAuthLoading() {
    const overlay = document.getElementById('auth-loading');
    if (overlay) overlay.remove();
}

// ============================================
// EXPORT FUNCTIONS
// ============================================

// Make functions available globally
window.auth = auth;
window.signInWithGoogle = signInWithGoogle;
window.signInWithEmail = signInWithEmail;
window.registerWithEmail = registerWithEmail;
window.signOutUser = signOutUser;
window.getCurrentUser = getCurrentUser;
window.getUserProfile = getUserProfile;
window.updateUserSubscription = updateUserSubscription;
window.isAuthenticated = isAuthenticated;
window.requireAuth = requireAuth;
window.onAuthChange = onAuthChange;
window.displayUserInfo = displayUserInfo;

console.log('✅ Auth module loaded');

// Auto-detect if we need authentication on this page
if (window.location.pathname.includes('dashboard')) {
    requireAuth();
}
