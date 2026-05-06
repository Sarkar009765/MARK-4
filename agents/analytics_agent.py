"""
Analytics Agent
Tracks performance and optimizes strategy based on data.
The 'data scientist' of the system.
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta

from agents.base_agent import BaseAgent


class AnalyticsAgent(BaseAgent):
    """
    Analyzes performance metrics and recommends optimizations.
    Functions:
    - Track likes, comments, shares, follower growth
    - Determine best posting times
    - Identify top-performing content types
    - Generate weekly reports
    - Self-optimization recommendations
    """
    
    def __init__(self):
        super().__init__(
            name="AnalyticsAgent",
            description="Analyzes performance and optimizes strategy"
        )
        self.max_actions_per_hour = 20
    
    async def run(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute analytics cycle."""
        self.log_action("running_analytics_cycle", {})
        
        # 1. Collect current metrics (simulated)
        metrics = await self._collect_metrics()
        
        # 2. Analyze content performance
        content_analysis = await self._analyze_content_performance(metrics)
        
        # 3. Optimize posting schedule
        schedule_optimization = await self._optimize_schedule(metrics)
        
        # 4. Generate recommendations
        recommendations = await self._generate_recommendations(
            metrics, content_analysis, schedule_optimization
        )
        
        result = {
            "status": "success",
            "metrics_summary": metrics,
            "content_analysis": content_analysis,
            "schedule_optimization": schedule_optimization,
            "recommendations": recommendations,
            "generated_at": datetime.now().isoformat()
        }
        
        self.log_action("analytics_complete", {"score": metrics.get("engagement_rate", 0)})
        return result
    
    async def _collect_metrics(self) -> Dict[str, Any]:
        """
        Collect performance metrics from connected platforms.
        In production: connect to platform APIs.
        """
        # Simulated metrics
        metrics = {
            "followers": 1250,
            "follower_change": 45,
            "posts_today": 2,
            "total_posts": 45,
            "likes": 3250,
            "comments": 312,
            "shares": 89,
            "reach": 15400,
            "engagement_rate": 5.2,
            "best_post_type": "carousel",
            "best_posting_time": "12:30 PM"
        }
        
        self.log_action("metrics_collected", metrics)
        return metrics
    
    async def _analyze_content_performance(self, metrics: Dict) -> Dict[str, Any]:
        """Analyze which content types perform best."""
        prompt = f"""Based on this performance data:
{metrics}

Analyze and return JSON:
{{
    "top_performing": ["format1", "format2"],
    "worst_performing": ["format3"],
    "content_insights": [
        {{"type": "carousel", "score": 8.5, "why": "High save rate"}},
        {{"type": "video", "score": 6.2, "why": "Good reach but low saves"}}
    ],
    "hashtag_performance": {{"#motivation": 8.0, "#success": 7.5}},
    "optimal_caption_style": "medium with storytelling"
}}"""
        
        try:
            return self.think(prompt, json_mode=True)
        except Exception:
            return {
                "top_performing": ["carousel", "single_image"],
                "worst_performing": [],
                "content_insights": [
                    {"type": "carousel", "score": 8.5, "why": "High save rate"},
                    {"type": "video", "score": 6.0, "why": "Good reach"}
                ],
                "hashtag_performance": {"#growth": 7.5, "#motivation": 8.0},
                "optimal_caption_style": "medium"
            }
    
    async def _optimize_schedule(self, metrics: Dict) -> Dict[str, Any]:
        """Determine optimal posting schedule."""
        # In production: analyze actual engagement times from API
        return {
            "recommended_times": [
                {"time": "08:00", "day": "weekday", "reason": "Morning commute peak"},
                {"time": "12:30", "day": "any", "reason": "Lunch break"},
                {"time": "19:00", "day": "weekday", "reason": "Evening wind-down"},
                {"time": "21:00", "day": "weekend", "reason": "Relaxation time"}
            ],
            "posts_per_day_optimal": 2,
            "rest_day": "Sunday",
            "confidence": "medium"
        }
    
    async def _generate_recommendations(self, metrics: Dict, 
                                       content_analysis: Dict,
                                       schedule_opt: Dict) -> List[Dict]:
        """Generate actionable recommendations based on data."""
        prompt = f"""Based on this analysis:

Performance Metrics:
- Engagement Rate: {metrics.get('engagement_rate')}%
- Best Content: {metrics.get('best_post_type')}
- Follower Growth: {metrics.get('follower_change')}

Content Analysis:
- Top performing: {content_analysis.get('top_performing', [])}
- Worst performing: {content_analysis.get('worst_performing', [])}

Schedule Optimization:
- Best times: {[t['time'] for t in schedule_opt.get('recommended_times', [])[:3]]}

Generate 3-5 specific actionable recommendations in JSON:
{{
    "recommendations": [
        {{"priority": "high", "action": "Do X", "reason": "Because Y", "expected_impact": "+5% engagement"}}
    ]
}}

Focus on:
- Content format changes
- Posting time adjustments
- Engagement strategy tweaks
- Hashtag optimization"""
        
        try:
            response = self.think(prompt, json_mode=True)
            return response.get("recommendations", [])
        except Exception:
            return [
                {"priority": "high", "action": "Post more carousels", "reason": "Highest engagement format", "expected_impact": "+5% engagement"},
                {"priority": "medium", "action": "Post at 12:30 PM", "reason": "Best performing time", "expected_impact": "+3% reach"},
                {"priority": "medium", "action": "Add #growth and #motivation hashtags", "reason": "High-performing tags", "expected_impact": "+2% discovery"}
            ]
    
    def calculate_roi(self, time_invested_hours: float, metrics: Dict) -> Dict[str, float]:
        """Calculate return on time investment."""
        engagement_value = metrics.get("likes", 0) * 0.1 + metrics.get("comments", 0) * 0.5
        growth_value = metrics.get("follower_change", 0) * 2.0
        total_value = engagement_value + growth_value
        
        roi = ((total_value - time_invested_hours * 10) / (time_invested_hours * 10)) * 100 if time_invested_hours > 0 else 0
        
        return {
            "total_value_generated": total_value,
            "time_invested_hours": time_invested_hours,
            "roi_percentage": round(roi, 1),
            "break_even_hours": round(total_value / 10, 1) if total_value > 0 else 0
        }