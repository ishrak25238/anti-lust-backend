# ML Pattern Analysis Workflow

## 📊 Overview

The Anti-Lust Guardian ML system provides comprehensive behavioral pattern analysis with persistent storage, actionable insights, and real-time notifications.

---

## 🔄 Data Flow

```
1. Threat Detection (ML Models)
   ↓
2. Pattern Event Storage (Database)
   ↓
3. Temporal Analysis (7/30 day windows)
   ↓
4. Behavioral Profiling (Long-term trends)
   ↓
5. Recommendation Generation (Actionable insights)
   ↓
6. Parent Notifications (Critical alerts)
```

---

## 🎯 Pattern Detection

### Event Types
1. **NSFW Detection**: Image-based threats (CLIP, ResNet50, EfficientNet)
2. **Text Classification**: Harmful text detection (5x BERT models)
3. **URL Analysis**: Malicious URL detection (ML + heuristics)

### Storage
Every detection event is stored in the database with:
- `device_id`: Which device triggered the event
- `event_type`: nsfw, text, or url
- `confidence`: Model confidence score (0-1)
- `threat_level`: Integer level (0-4)
- `threat_score`: Normalized threat score
- `context`: Additional metadata (JSON)
- `timestamp`: When it occurred

---

## 📈 Temporal Pattern Analysis

### Frequency Analysis
Categorizes usage into:
- **Low**: < 0.5 events/hour
- **Moderate**: 0.5-2 events/hour
- **High**: 2-5 events/hour
- **Critical**: > 5 events/hour

### Peak Detection
Identifies:
- **Peak Hours**: Top 3 hours of day with most activity
- **Peak Days**: Days of week with highest frequency
- **Hour Distribution**: Event count for each hour (0-23)

### Escalation Detection
Compares first half vs second half of period:
- **Delta**: Difference in average threat scores
- **Threshold**: Delta > 0.2 indicates escalation
- **Trend**: ESCALATING or STABLE

### Relapse Risk
Based on events in last 24 hours:
- **0-2 events**: LOW risk (score: 0.2)
- **3-5 events**: MODERATE risk (score: 0.4)
- **6-10 events**: HIGH risk (score: 0.7)
- **10+ events**: CRITICAL risk (score: 0.9)

---

## 👤 Behavioral Profiling

### Long-Term Metrics
Tracked for each device:
- **First/Last Event**: Lifetime activity span
- **Total Events**: All-time count
- **Average Daily Events**: Events per day
- **Peak Hours**: Consistent high-activity hours
- **Trend**: IMPROVING, STABLE, or WORSENING (comparing last 7 vs prev 7 days)
- **Habit Formation Score**: 0-1 score indicating habit strength

### Profile Updates
Automatically updated after each event:
- Recalculates all statistics
- Updates trend based on recent vs historical
- Persists to database

---

## 💡 Recommendation System

### Priority Levels (1-10)
- **10 (IMMEDIATE)**: Critical frequency detected
- **9 (IMMEDIATE)**: High relapse risk (10+ events/24h)
- **8 (WARNING)**: Behavioral escalation detected
- **6 (SUGGESTION)**: Schedule interventions at peak hours

### Recommendation Categories
1. **IMMEDIATE**: Requires action within hours
   - Example: "Enable Guardian Lock immediately - Critical usage frequency detected"

2. **WARNING**: Requires attention within days
   - Example: "Behavioral escalation detected (trend: ESCALATING) - Increase monitoring"

3. **SUGGESTION**: Recommended actions
   - Example: "Schedule positive activities at peak risk hour: 14:00"

### Storage
All recommendations stored in database:
- `device_id`: Target device
- `recommendation`: Text description
- `priority`: 1-10 urgency
- `category`: IMMEDIATE/WARNING/SUGGESTION
- `created_at`: When generated
- `acknowledged`: Parent acknowledged (0/1)
- `effective`: Whether it helped (tracked post-implementation)

---

## 📧 Parent Notifications

### Critical Alerts
**Trigger**: Threat level = CRITICAL (score > 0.8)

**Throttling**: Max 1 per hour per device

**Contains**:
- Threat type (NSFW/Text/URL)
- Threat level
- Confidence score
- Timestamp
- Device ID
- Recommended actions

### Daily Digest
**Timing**: Configurable (typically end of day)

**Contains**:
- Total events (24h)
- Relapse risk level
- Trend analysis
- Peak activity hours
- Top 5 recommendations

### Weekly Summary
**Timing**: Weekly (typically Sunday evening)

**Contains**:
- 7-day event count
- Behavioral trend (IMPROVING/STABLE/WORSENING)
- Average daily events
- All-time statistics
- Behavioral insights
- Focus areas for the week

### Escalation Alerts
**Trigger**: Escalation detected in temporal analysis

**Contains**:
- Escalation confidence
- Trend direction
- Delta from previous period
- Immediate actions required

---

## 🔄 API Endpoints

### Get Pattern Analysis
```http
GET /api/patterns/analysis/{device_id}?days=7
X-API-Key: your-api-key

Response:
{
  "patterns": {
    "frequency": {...},
    "temporal": {...},
    "escalation": {...},
    "relapse_risk": {...}
  },
  "recommendations": [...],
  "profile": {...}
}
```

### Report False Positive
```http
POST /api/patterns/false-positive
X-API-Key: your-api-key

{
  "event_id": 123,
  "device_id": "device_001",
  "reason": "This was a medical image, not NSFW"
}

Response:
{
  "success": true,
  "report_id": 456
}
```

---

## 🔬 Machine Learning Feedback Loop

### False Positive Handling
1. Parent/child reports false positive via API
2. Event marked with `is_false_positive = 1`
3. Report stored for review
4. ML team periodically reviews reports
5. Models retrained with corrected labels
6. Confidence thresholds adjusted if needed

### Model Improvement
- FP reports tracked per model type
- High FP rate triggers manual review
- Models fine-tuned on corrected dataset
- A/B testing of new models
- Gradual rollout based on performance

---

## 📊 Database Schema

### Core Tables
1. **pattern_events**: Individual threat detections
2. **behavioral_profiles**: Long-term device profiles
3. **daily_pattern_summaries**: Aggregated daily stats
4. **intervention_recommendations**: Actionable suggestions
5. **false_positive_reports**: ML feedback

### Retention Policy
- **Pattern Events**: 90 days
- **Daily Summaries**: 365 days
- **Behavioral Profiles**: Lifetime
- **Recommendations**: 30 days after acknowledged
- **False Positive Reports**: Lifetime

---

## 🎯 Key Metrics

### Detection Accuracy
- **NSFW**: 95%+ (ensemble of CLIP, ResNet50, EfficientNet)
- **Text Toxicity**: 88%+ (ensemble of 5 BERT models)
- **URL Threats**: 97%+ (ML + heuristics)

### Response Time
- **Pattern Storage**: < 50ms
- **Temporal Analysis**: < 200ms
- **Recommendation Generation**: < 300ms
- **Notification Send**: < 1s

### Data Volume
- **Events/Day**: Varies by usage
- **Storage/Event**: ~1KB (JSON context)
- **Database Growth**: ~30MB/1M events

---

## 🚀 Best Practices

### For Parents
1. **Review notifications daily**: Don't ignore alerts
2. **Act on recommendations**: Prioritize by urgency
3. **Report false positives**: Improves accuracy
4. **Monitor trends**: Look for IMPROVING/WORSENING patterns
5. **Celebrate progress**: Acknowledge positive trends

### For Developers
1. **Keep models updated**: Retrain quarterly
2. **Monitor false positive rate**: < 5% target
3. **Optimize database**: Index on device_id, timestamp
4. **Archive old data**: Move to cold storage after retention period
5. **A/B test improvements**: Before full rollout

---

## 📝 Example Usage

### Python Client
```python
import requests

# Get pattern analysis
response = requests.get(
    "https://api.example.com/api/patterns/analysis/device_001?days=7",
    headers={"X-API-Key": "your-key"}
)

patterns = response.json()
risk_level = patterns['patterns']['relapse_risk']['level']

if risk_level in ['HIGH', 'CRITICAL']:
    print(f"⚠️ {risk_level} relapse risk detected!")
    
    # Send intervention
    for rec in patterns['recommendations']:
        if rec['priority'] >= 8:
            print(f"[{rec['category']}] {rec['recommendation']}")
```

---

## 🔮 Future Enhancements

1. **Cross-Device Correlation**: Detect patterns across multiple child devices
2. **Predictive Analytics**: Forecast relapse risk 7 days ahead
3. **Habit Formation Detection**: Identify habitual patterns
4. **Peer Comparison**: Anonymous benchmarking against age group
5. **Intervention Effectiveness**: A/B test different recommendations
6. **Real-Time ML**: Online learning with data drift detection
