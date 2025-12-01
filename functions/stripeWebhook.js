// ============================================
// STRIPE WEBHOOK HANDLER (Firebase Cloud Function)
// Handles successful payments and updates user subscriptions
// ============================================

const functions = require('firebase-functions');
const admin = require('firebase-admin');
const stripe = require('stripe')(functions.config().stripe.secret_key);

admin.initializeApp();

/**
 * Stripe Webhook Handler
 * Endpoint: /stripeWebhook
 */
exports.stripeWebhook = functions.https.onRequest(async (req, res) => {
    const sig = req.headers['stripe-signature'];
    const webhookSecret = functions.config().stripe.webhook_secret;

    let event;

    try {
        // Verify webhook signature
        event = stripe.webhooks.constructEvent(req.rawBody, sig, webhookSecret);
    } catch (err) {
        console.error('⚠️  Webhook signature verification failed:', err.message);
        return res.status(400).send(`Webhook Error: ${err.message}`);
    }

    // Handle the checkout.session.completed event
    if (event.type === 'checkout.session.completed') {
        const session = event.data.object;

        console.log('✅ Payment successful:', session.id);
        console.log('Customer:', session.customer);
        console.log('Client Reference ID (Firebase UID):', session.client_reference_id);

        // Get Firebase UID from client_reference_id
        const uid = session.client_reference_id;

        if (!uid) {
            console.error('❌ No Firebase UID provided');
            return res.status(400).send('No user ID');
        }

        // Determine plan type from session metadata or line items
        const lineItems = await stripe.checkout.sessions.listLineItems(session.id);
        const product = lineItems.data[0];
        const amount = product.amount_total; // in cents

        let plan = 'monthly';
        if (amount >= 15000) {
            // $150 or more = lifetime
            plan = 'lifetime';
        }

        // Update user's subscription in Firestore
        try {
            const userRef = admin.firestore().collection('users').doc(uid);

            const subscriptionData = {
                status: 'active',
                plan: plan,
                stripeCustomerId: session.customer,
                stripeSessionId: session.id,
                amount: amount / 100, // convert to dollars
                currency: session.currency,
                startDate: admin.firestore.FieldValue.serverTimestamp(),
            };

            // Add nextBilling for monthly subscriptions
            if (plan === 'monthly') {
                const nextBilling = new Date();
                nextBilling.setMonth(nextBilling.getMonth() + 1);
                subscriptionData.nextBilling = admin.firestore.Timestamp.fromDate(nextBilling);
                subscriptionData.subscriptionId = session.subscription;
            }

            await userRef.update({
                subscription: subscriptionData,
                'subscription.updatedAt': admin.firestore.FieldValue.serverTimestamp()
            });

            console.log('✅ User subscription updated:', uid, plan);

        } catch (error) {
            console.error('❌ Error updating subscription:', error);
            return res.status(500).send('Database error');
        }
    }

    // Handle subscription cancellation
    if (event.type === 'customer.subscription.deleted') {
        const subscription = event.data.object;

        // Find user by Stripe customer ID
        const usersRef = admin.firestore().collection('users');
        const querySnapshot = await usersRef
            .where('subscription.stripeCustomerId', '==', subscription.customer)
            .get();

        if (!querySnapshot.empty) {
            const userDoc = querySnapshot.docs[0];
            await userDoc.ref.update({
                'subscription.status': 'cancelled',
                'subscription.cancelledAt': admin.firestore.FieldValue.serverTimestamp()
            });
            console.log('✅ Subscription cancelled for user:', userDoc.id);
        }
    }

    // Return a 200 response to acknowledge receipt of the event
    res.json({ received: true });
});

// ============================================
// DEPLOYMENT INSTRUCTIONS
// ============================================

/*
1. Install Firebase CLI:
   npm install -g firebase-tools

2. Initialize Firebase Functions:
   firebase init functions

3. Install dependencies:
   cd functions
   npm install stripe firebase-admin firebase-functions

4. Set Stripe secrets:
   firebase functions:config:set stripe.secret_key="YOUR_STRIPE_SECRET_KEY"
   firebase functions:config:set stripe.webhook_secret="YOUR_WEBHOOK_SECRET"

5. Deploy:
   firebase deploy --only functions

6. Get the webhook URL from Firebase Console
   Look like: https://us-central1-YOUR-PROJECT.cloudfunctions.net/stripeWebhook

7. Add webhook endpoint in Stripe Dashboard:
   - Go to Developers → Webhooks
   - Add endpoint with the URL above
   - Select events: checkout.session.completed, customer.subscription.deleted
   - Copy the webhook signing secret
   - Update Firebase config with: firebase functions:config:set stripe.webhook_secret="whsec_..."

TESTING:
- Use Stripe CLI to test webhooks locally:
  stripe listen --forward-to localhost:5001/YOUR-PROJECT/us-central1/stripeWebhook
*/
