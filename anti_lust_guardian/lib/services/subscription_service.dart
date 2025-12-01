import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';

/// Service to manage user subscriptions synced with Firestore
/// Allows cross-device subscription access
class SubscriptionService {
  final FirebaseFirestore _db = FirebaseFirestore.instance;
  final FirebaseAuth _auth = FirebaseAuth.instance;
  
  /// Check if user has an active subscription
  Future<bool> hasActiveSubscription(String userId) async {
    try {
      final doc = await _db.collection('subscriptions').doc(userId).get();
      
      if (!doc.exists) return false;
      
      final status = doc.data()?['status'];
      return status == 'active' || status == 'trialing';
    } catch (e) {
      // Error checking subscription
      return false;
    }
  }
  
  /// Get full subscription details for a user
  Future<Map<String, dynamic>?> getSubscription(String userId) async {
    try {
      final doc = await _db.collection('subscriptions').doc(userId).get();
      
      if (!doc.exists) return null;
      
      return doc.data();
    } catch (e) {
      // Error getting subscription
      return null;
    }
  }
  
  /// Get current user's subscription
  Future<Map<String, dynamic>?> getCurrentUserSubscription() async {
    final user = _auth.currentUser;
    if (user == null) return null;
    
    return await getSubscription(user.uid);
  }
  
  /// Check if current user has active subscription
  Future<bool> currentUserHasActiveSubscription() async {
    final user = _auth.currentUser;
    if (user == null) return false;
    
    return await hasActiveSubscription(user.uid);
  }
  
  /// Stream of subscription status for real-time updates
  Stream<bool> subscriptionStream(String userId) {
    return _db
      .collection('subscriptions')
      .doc(userId)
      .snapshots()
      .map((doc) {
        if (!doc.exists) return false;
        final status = doc.data()?['status'];
        return status == 'active' || status == 'trialing';
      });
  }
  
  /// Stream for current user's subscription
  Stream<bool> currentUserSubscriptionStream() {
    final user = _auth.currentUser;
    if (user == null) return Stream.value(false);
    
    return subscriptionStream(user.uid);
  }
  
  /// Get subscription plan type
  Future<String?> getSubscriptionPlan(String userId) async {
    final subscription = await getSubscription(userId);
    return subscription?['plan'];
  }
  
  /// Check if user is on trial
  Future<bool> isOnTrial(String userId) async {
    final subscription = await getSubscription(userId);
    if (subscription == null) return false;
    
    return subscription['status'] == 'trialing';
  }
  
  /// Get trial end date
  Future<DateTime?> getTrialEndDate(String userId) async {
    final subscription = await getSubscription(userId);
    if (subscription == null) return null;
    
    final trialEnd = subscription['trialEnd'];
    if (trialEnd == null) return null;
    
    if (trialEnd is Timestamp) {
      return trialEnd.toDate();
    }
    
    return null;
  }
}
