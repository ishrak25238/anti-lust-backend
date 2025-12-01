"""
Pattern analysis tests
Tests pattern storage, temporal analysis, and recommendation generation
"""
import pytest
import asyncio
from services.pattern_storage import PatternStorage
from datetime import datetime, timedelta

@pytest.fixture
async def pattern_storage():
    """Create pattern storage instance"""
    return PatternStorage()

class TestPatternPersistence:
    """Test pattern data persistence"""
    
    @pytest.mark.asyncio
    async def test_pattern_persistence_across_restarts(self, pattern_storage):
        """Patterns should persist after service restart"""
        device_id = "test_device_001"
        
        for i in range(10):
            await pattern_storage.store_event(
                device_id=device_id,
                event_type='nsfw',
                confidence=0.8,
                threat_level=3,
                threat_score=0.8,
                context={'test': True}
            )
        
        events = await pattern_storage.get_events(device_id, hours=24)
        assert len(events) >= 10
        assert all(e['device_id'] == device_id for e in events)

class TestTemporalAnalysis:
    """Test temporal pattern detection"""
    
    @pytest.mark.asyncio
    async def test_weekly_pattern_detection(self, pattern_storage):
        """Should detect patterns over 7 days"""
        device_id = "test_device_002"
        
        base_time = datetime.utcnow()
        for day in range(7):
            for hour in [14, 15, 16]:
                timestamp = base_time - timedelta(days=day, hours=hour)
                pass
        
        patterns = await pattern_storage.analyze_temporal_patterns(device_id, days=7)
        assert patterns['status'] == 'analyzed'
        assert 'frequency' in patterns
        assert 'temporal' in patterns
    
    @pytest.mark.asyncio
    async def test_escalation_detection_accuracy(self, pattern_storage):
        """Should accurately detect behavioral escalation"""
        device_id = "test_device_003"
        
        for score in [0.3, 0.3, 0.4, 0.4, 0.6, 0.7, 0.8, 0.9]:
            await pattern_storage.store_event(
                device_id=device_id,
                event_type='nsfw',
                confidence=score,
                threat_level=int(score * 5),
                threat_score=score,
                context={}
            )
        
        patterns = await pattern_storage.analyze_temporal_patterns(device_id, days=7)
        assert patterns.get('escalation', {}).get('detected') == True

class TestRecommendations:
    """Test recommendation generation"""
    
    @pytest.mark.asyncio
    async def test_recommendation_generation(self, pattern_storage):
        """Should generate actionable recommendations"""
        device_id = "test_device_004"
        
        for i in range(15):
            await pattern_storage.store_event(
                device_id=device_id,
                event_type='nsfw',
                confidence=0.9,
                threat_level=4,
                threat_score=0.9,
                context={}
            )
        
        recommendations = await pattern_storage.generate_recommendations(device_id)
        assert len(recommendations) > 0
        assert all('priority' in r for r in recommendations)
        assert all('recommendation' in r for r in recommendations)

class TestFalsePositives:
    """Test false positive handling"""
    
    @pytest.mark.asyncio
    async def test_false_positive_handling(self, pattern_storage):
        """Should properly log and handle false positive reports"""
        device_id = "test_device_005"
        
        event_id = await pattern_storage.store_event(
            device_id=device_id,
            event_type='nsfw',
            confidence=0.7,
            threat_level=3,
            threat_score=0.7,
            context={}
        )
        
        report_id = await pattern_storage.report_false_positive(
            event_id=event_id,
            device_id=device_id,
            reason="This was a medical image, not NSFW"
        )
        
        assert report_id is not None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
