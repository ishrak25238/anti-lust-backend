import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json

class PatternLearningEngine:
    def __init__(self):
        self.scaler = StandardScaler()
        self.kmeans_model = None
        self.dbscan_model = None
    
    async def analyze_user_patterns(self, user_ids: List[int], db_session) -> Dict:
        patterns = []
        
        for user_id in user_ids:
            user_pattern = await self._extract_user_pattern(user_id, db_session)
            if user_pattern:
                patterns.append(user_pattern)
        
        if not patterns:
            return {'error': 'No patterns found'}
        
        clusters = await self.cluster_behavioral_patterns(patterns)
        insights = await self.generate_insights_from_clusters(clusters)
        
        return {
            'total_users_analyzed': len(user_ids),
            'patterns_extracted': len(patterns),
            'clusters_found': len(set(c['cluster_id'] for c in clusters)),
            'key_insights': insights,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def _extract_user_pattern(self, user_id: int, db_session) -> Optional[Dict]:
        from database import PreventedSite
        from sqlalchemy import select, func
        
        try:
            query = select(
                func.count(PreventedSite.id).label('total_blocks'),
                func.count(func.distinct(PreventedSite.category)).label('unique_categories'),
                func.avg(PreventedSite.attempt_count).label('avg_attempts_per_site')
            ).where(PreventedSite.user_id == user_id)
            
            result = await db_session.execute(query)
            row = result.first()
            
            if not row or row.total_blocks == 0:
                return None
            
            time_query = select(
                func.hour(PreventedSite.timestamp).label('hour')
            ).where(PreventedSite.user_id == user_id)
            
            time_result = await db_session.execute(time_query)
            hours = [r.hour for r in time_result.all()]
            
            peak_hours = self._calculate_peak_hours(hours)
            
            return {
                'user_id': user_id,
                'total_blocks': row.total_blocks,
                'unique_categories': row.unique_categories,
                'avg_attempts_per_site': float(row.avg_attempts_per_site or 0),
                'peak_hours': peak_hours,
                'pattern_vector': [
                    row.total_blocks,
                    row.unique_categories,
                    float(row.avg_attempts_per_site or 0),
                    len(peak_hours)
                ]
            }
        except:
            return None
    
    def _calculate_peak_hours(self, hours: List[int]) -> List[int]:
        if not hours:
            return []
        
        hour_counts = {}
        for hour in hours:
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
        
        max_count = max(hour_counts.values())
        return [h for h, count in hour_counts.items() if count >= max_count * 0.7]
    
    async def cluster_behavioral_patterns(self, patterns: List[Dict]) -> List[Dict]:
        if len(patterns) < 3:
            return [{'cluster_id': 0, 'pattern': p} for p in patterns]
        
        vectors = np.array([p['pattern_vector'] for p in patterns])
        
        scaled_vectors = self.scaler.fit_transform(vectors)
        
        n_clusters = min(5, len(patterns) // 2)
        self.kmeans_model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = self.kmeans_model.fit_predict(scaled_vectors)
        
        clustered_patterns = []
        for i, pattern in enumerate(patterns):
            clustered_patterns.append({
                'cluster_id': int(cluster_labels[i]),
                'pattern': pattern
            })
        
        return clustered_patterns
    
    async def generate_insights_from_clusters(self, clusters: List[Dict]) -> List[Dict]:
        cluster_groups = {}
        for item in clusters:
            cluster_id = item['cluster_id']
            if cluster_id not in cluster_groups:
                cluster_groups[cluster_id] = []
            cluster_groups[cluster_id].append(item['pattern'])
        
        insights = []
        
        for cluster_id, patterns in cluster_groups.items():
            avg_blocks = sum(p['total_blocks'] for p in patterns) / len(patterns)
            avg_categories = sum(p['unique_categories'] for p in patterns) / len(patterns)
            avg_attempts = sum(p['avg_attempts_per_site'] for p in patterns) / len(patterns)
            
            all_peak_hours = []
            for p in patterns:
                all_peak_hours.extend(p['peak_hours'])
            
            common_peak_hours = list(set([h for h in all_peak_hours if all_peak_hours.count(h) >= len(patterns) * 0.5]))
            
            insight = {
                'cluster_id': cluster_id,
                'user_count': len(patterns),
                'avg_blocks_per_user': round(avg_blocks, 2),
                'avg_unique_categories': round(avg_categories, 2),
                'avg_attempts_per_site': round(avg_attempts, 2),
                'common_peak_hours': sorted(common_peak_hours),
                'severity': self._categorize_severity(avg_blocks, avg_attempts),
                'recommendation': self._generate_recommendation(avg_blocks, common_peak_hours, avg_attempts)
            }
            
            insights.append(insight)
        
        return sorted(insights, key=lambda x: x['avg_blocks_per_user'], reverse=True)
    
    def _categorize_severity(self, avg_blocks: float, avg_attempts: float) -> str:
        if avg_blocks > 100 or avg_attempts > 5:
            return 'HIGH_RISK'
        elif avg_blocks > 50 or avg_attempts > 3:
            return 'MEDIUM_RISK'
        else:
            return 'LOW_RISK'
    
    def _generate_recommendation(self, avg_blocks: float, peak_hours: List[int], avg_attempts: float) -> str:
        recommendations = []
        
        if avg_blocks > 100:
            recommendations.append("Consider increasing block notification frequency")
        
        if avg_attempts > 5:
            recommendations.append("Users show persistent retry behavior - implement progressive blocking delays")
        
        if peak_hours:
            hours_str = ', '.join([f"{h}:00" for h in sorted(peak_hours)])
            recommendations.append(f"Peak risk hours: {hours_str} - suggest focus time scheduling")
        
        if not recommendations:
            recommendations.append("Current protection level appears adequate")
        
        return ' | '.join(recommendations)
    
    async def generate_insights_email(self, insights_data: Dict) -> str:
        email_body = f"""
<h2>Anti-Lust Guardian - Behavioral Pattern Research Insights</h2>
<p><strong>Analysis Date:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</p>
<p><strong>Users Analyzed:</strong> {insights_data.get('total_users_analyzed', 0)}</p>
<p><strong>Patterns Extracted:</strong> {insights_data.get('patterns_extracted', 0)}</p>

<h3>Key Findings:</h3>
<ol>
"""
        
        for idx, insight in enumerate(insights_data.get('key_insights', [])[:5], 1):
            email_body += f"""
<li>
    <strong>Pattern Group {idx}</strong> 
    ({insight['user_count']} users, {insight['severity']} severity)
    <ul>
        <li>Average Blocks: {insight['avg_blocks_per_user']}</li>
        <li>Category Diversity: {insight['avg_unique_categories']} types</li>
        <li>Retry Behavior: {insight['avg_attempts_per_site']} attempts/site</li>
        <li>Peak Hours: {', '.join([f'{h}:00' for h in insight['common_peak_hours']]) if insight['common_peak_hours'] else 'No clear pattern'}</li>
        <li><strong>Recommendation:</strong> {insight['recommendation']}</li>
    </ul>
</li>
"""
        
        email_body += """
</ol>

<h3>ML Pattern Analysis Summary:</h3>
<p>Users exhibit distinct behavioral clusters. The system has identified intervention points based on temporal patterns and retry behaviors.</p>

<p><em>This is an automated research insight generated by the ML Pattern Learning Engine.</em></p>
"""
        
        return email_body
