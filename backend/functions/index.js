const { onRequest } = require('firebase-functions/v2/https');
const { defineString } = require('firebase-functions/params');
const admin = require('firebase-admin');

admin.initializeApp();

// Define the params (but don't call .value() yet)
const stripeSecretKey = defineString('STRIPE_SECRET_KEY');
const stripeWebhookSecret = defineString('STRIPE_WEBHOOK_SECRET');

exports.stripeWebhook = onRequest(async (req, res) => {
    // Initialize Stripe inside the function
    const stripe = require('stripe')(stripeSecretKey.value());

    const sig = req.headers['stripe-signature'];
    const webhookSecret = stripeWebhookSecret.value();

    let event;
    try {
        event = stripe.webhooks.constructEvent(req.body, sig, webhookSecret);
    } catch (err) {
        console.error('Webhook error:', err.message);
        return res.status(400).send(`Webhook Error: ${err.message}`);
    }

    if (event.type === 'checkout.session.completed') {
        const session = event.data.object;
        const uid = session.client_reference_id;

        if (!uid) {
            return res.status(400).send('No user ID');
        }

        const lineItems = await stripe.checkout.sessions.listLineItems(session.id);
        const amount = lineItems.data[0].amount_total;
        const plan = amount >= 15000 ? 'lifetime' : 'monthly';

        await admin.firestore().collection('users').doc(uid).set({
            subscription: {
                status: 'active',
                plan: plan,
                stripeCustomerId: session.customer,
                amount: amount / 100,
                startDate: admin.firestore.FieldValue.serverTimestamp()
            }
        }, { merge: true });

        console.log('✅ Subscription updated:', uid, plan);
    }

    res.json({ received: true });
});
