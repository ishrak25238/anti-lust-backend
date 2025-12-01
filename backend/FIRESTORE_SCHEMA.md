# Firebase Firestore Data Model - Anti-Lust Guardian

## 📊 Complete Database Structure

### Collection: `users`
```javascript
users/{userId} {
  // Basic Info
  username: string,
  email: string,
  createdAt: timestamp,
  passwordHash: string (optional - Firebase Auth handles this),
  role: string, // "user" | "parent" | "admin"
  photoUrl: string,
  displayName: string,
  
  // ✨ Subscription Info (NEW - for Stripe integration)
  subscription: {
    status: string, // "active" | "inactive" | "trial" | "cancelled"
    plan: string, // "monthly" | "lifetime"
    stripeCustomerId: string,
    stripeSessionId: string,
    subscriptionId: string (for monthly),
    amount: number, // in dollars
    currency: string, // "usd"
    startDate: timestamp,
    nextBilling: timestamp (monthly only),
    trialEnds: timestamp (if trial),
    cancelledAt: timestamp (if cancelled),
    updatedAt: timestamp
  },
  
  // Settings
  settings: {
    theme: string, // "dark" | "light"
    notifications: boolean,
    emergencyContact: string,
    language: string
  },
  
  // Stats
  stats: {
    totalBlockedAttempts: number,
    currentStreak: number, // days clean
    longestStreak: number,
    lastActivityAt: timestamp
  },
  
  lastLogin: timestamp,
  isActive: boolean
}
```

---

### Collection: `devices`
```javascript
devices/{deviceId} {
  userId: string (reference to users/{userId}),
  deviceName: string, // "John's iPhone"
  deviceType: string, // "android" | "ios" | "windows" | "mac" | "linux"
  installationId: string,
  osVersion: string,
  appVersion: string,
  
  createdAt: timestamp,
  lastSeenAt: timestamp,
  isActive: boolean,
  
  // Device-specific settings
  settings: {
    strictMode: boolean,
    allowEmergencyMode: boolean,
    requirePinForUninstall: boolean
  }
}
```

---

### Collection: `filterPolicies`
```javascript
filterPolicies/{policyId} {
  userId: string,
  policyName: string, // "Strict Mode" | "Standard" | "Custom"
  createdAt: timestamp,
  updatedAt: timestamp,
  description: string,
  isDefault: boolean,
  isActive: boolean,
  
  // Quick stats
  activeRulesCount: number,
  appliedToDevices: array<string> // deviceIds
}
```

---

### Collection: `filterRules`
```javascript
filterRules/{ruleId} {
  policyId: string (reference to filterPolicies/{policyId}),
  userId: string,
  
  ruleType: string, // "url" | "keyword" | "category" | "image" | "vpn"
  value: string, // actual pattern/keyword/category
  action: string, // "block" | "warn" | "log"
  isActive: boolean,
  severity: string, // "low" | "medium" | "high" | "critical"
  
  createdAt: timestamp,
  triggeredCount: number,
  lastTriggeredAt: timestamp
}
```

---

### Collection: `emergencyModeSessions`
```javascript
emergencyModeSessions/{sessionId} {
  userId: string,
  deviceId: string,
  
  startedAt: timestamp,
  endedAt: timestamp,
  durationMinutes: number,
  status: string, // "active" | "completed" | "cancelled"
  reason: string,
  
  // Parent notification
  parentNotified: boolean,
  parentNotifiedAt: timestamp,
  parentEmail: string
}
```

---

### Collection: `blockedAttempts`
```javascript
blockedAttempts/{attemptId} {
  userId: string,
  deviceId: string,
  ruleId: string (which rule was triggered),
  
  attemptedUrl: string,
  blockedAt: timestamp,
  contentCategory: string, // "adult" | "violence" | "gambling" | etc.
  severity: string,
  
  // Evidence
  screenshotUrl: string (Cloud Storage path),
  pageTitle: string,
  detectedKeywords: array<string>,
  
  // ML Analysis
  aiConfidenceScore: number, // 0.0 to 1.0
  mlModelVersion: string,
  
  // Context
  timeOfDay: number, // hour 0-23
  dayOfWeek: number, // 0-6
  wasInEmergencyMode: boolean
}
```

---

### ✨ NEW Collections for Analytics & Reports

### Collection: `dailyStats`
```javascript
dailyStats/{userId}_{date} {
  userId: string,
  date: string, // "2025-11-29"
  
  totalAttempts: number,
  blockedCount: number,
  warnedCount: number,
  
  // Time distribution
  peakHours: array<number>, // [14, 15, 20] (hours with most activity)
  
  // Categories
  categoriesBlocked: {
    adult: number,
    violence: number,
    gambling: number,
    other: number
  },
  
  // Behavior
  emergencyModeActivated: boolean,
  streakMaintained: boolean,
  
  createdAt: timestamp
}
```

---

### Collection: `parentChildLinks`
```javascript
parentChildLinks/{linkId} {
  parentUserId: string,
  childUserId: string,
  
  linkStatus: string, // "active" | "pending" | "revoked"
  createdAt: timestamp,
  acceptedAt: timestamp,
  
  // Parent permissions
  permissions: {
    viewReports: boolean,
    modifyFilters: boolean,
    lockDevice: boolean,
    viewScreenshots: boolean,
    receiveAlerts: boolean
  },
  
  // Child info (denormalized for quick access)
  childName: string,
  childEmail: string
}
```

---

### Collection: `reports`
```javascript
reports/{reportId} {
  userId: string,
  generatedAt: timestamp,
  reportType: string, // "weekly" | "monthly" | "custom"
  format: string, // "pdf" | "json"
  
  dateRange: {
    start: timestamp,
    end: timestamp
  },
  
  // Report data
  summary: {
    totalBlocked: number,
    averagePerDay: number,
    topCategories: array<object>,
    criticalIncidents: number,
    streakDays: number
  },
  
  // PDF file
  pdfUrl: string (Cloud Storage),
  fileSize: number,
  
  // Sharing
  sharedWith: array<string>, // parent emails
  expiresAt: timestamp
}
```

---

### Collection: `notifications`
```javascript
notifications/{notificationId} {
  userId: string,
  
  type: string, // "critical_block" | "emergency_mode" | "parent_alert" | "streak_milestone"
  title: string,
  message: string,
  
  createdAt: timestamp,
  readAt: timestamp,
  isRead: boolean,
  
  // Related data
  relatedAttemptId: string,
  relatedDeviceId: string,
  
  // Action
  actionUrl: string,
  actionLabel: string
}
```

---

### Collection: `appSettings` (Global App Config)
```javascript
appSettings/config {
  // ML Model versions
  mlModels: {
    imageModel: string, // "nudenet-v2.1"
    textModel: string, // "bert-v1.5"
    lastUpdated: timestamp
  },
  
  // Feature flags
  features: {
    vpnDetection: boolean,
    emergencyMode: boolean,
    parentMode: boolean,
    aiAnalysis: boolean
  },
  
  // Default policies
  defaultPolicies: {
    strict: object,
    standard: object,
    minimal: object
  }
}
```

---

## 🔐 Firestore Security Rules

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Users can only read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Devices belong to user
    match /devices/{deviceId} {
      allow read, write: if request.auth != null && 
        resource.data.userId == request.auth.uid;
    }
    
    // Filter policies belong to user
    match /filterPolicies/{policyId} {
      allow read, write: if request.auth != null && 
        resource.data.userId == request.auth.uid;
    }
    
    // Blocked attempts - user can read their own
    match /blockedAttempts/{attemptId} {
      allow read: if request.auth != null && 
        resource.data.userId == request.auth.uid;
      allow create: if request.auth != null;
    }
    
    // Parent can read child's data
    match /blockedAttempts/{attemptId} {
      allow read: if request.auth != null && 
        exists(/databases/$(database)/documents/parentChildLinks/$(request.auth.uid + '_' + resource.data.userId));
    }
  }
}
```

---

## 📝 Indexes Needed

Create these in Firebase Console → Firestore → Indexes:

1. **blockedAttempts**
   - userId (Ascending) + blockedAt (Descending)

2. **devices**
   - userId (Ascending) + lastSeenAt (Descending)

3. **dailyStats**
   - userId (Ascending) + date (Descending)

4. **emergencyModeSessions**
   - userId (Ascending) + startedAt (Descending)

---

## ✅ What's Included

✅ Your original schema (User, Device, FilterPolicy, etc.)  
✅ **Subscription tracking** (Stripe integration)  
✅ **Analytics & Reports** (PDF generation)  
✅ **Parent-Child controls** (parental monitoring)  
✅ **Notifications** (real-time alerts)  
✅ **Daily stats** (behavior tracking)  
✅ **Security rules** (data protection)

This structure supports your entire Anti-Lust Guardian app! 🛡️
