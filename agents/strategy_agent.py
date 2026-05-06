"""
Strategy Agent
Analyzes trends, competitors, and decides what content to create.
The brain's 'planning department'.
"""
from typing import Dict, Any, List
import asyncio
from datetime import datetime, timedelta

from agents.base_agent import BaseAgent


class StrategyAgent(BaseAgent):
    """
    Decides the content strategy for the day/week.
    Functions:
    - Trend analysis (what's hot in your niche)
    - Competitor monitoring
    - Content calendar planning
    - Best posting time calculation
    """
    
    def __init__(self):
        super().__init__(
            name="StrategyAgent",
            description="Analyzes trends and plans content strategy"
        )
        self.max_actions_per_hour = 20  # Lower limit for planning
    
    async def run(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute strategy planning cycle."""
        niche = context.get("niche", "general") if context else "general"
        
        self.log_action("running_strategy_cycle", {"niche": niche})
        
        # 1. Analyze trends
        trends = await self._analyze_trends(niche)
        
        # 2. Check what's working in the niche
        competitor_insights = await self._analyze_competitors(niche)
        
        # 3. Plan content themes for today
        content_themes = self._select_content_themes(trends, competitor_insights)
        
        # 4. Determine best posting times
        best_times = self._calculate_best_posting_times()
        
        result = {
            "status": "success",
            "trends": trends,
            "competitor_insights": competitor_insights,
            "content_themes": content_themes,
            "best_posting_times": best_times,
            "strategy_for": datetime.now().strftime("%Y-%m-%d")
        }
        
        self.log_action("strategy_complete", result)
        return result
    
    async def _analyze_trends(self, niche: str) -> List[Dict[str, str]]:
        """Find trending topics in the niche."""
        prompt = f"""Analyze current trending topics in the '{niche}' niche.
        Consider: viral content themes, popular hashtags, current events related to {niche}.
        
        Return JSON with this structure:
        {{
            "trends": [
                {{
                    "topic": "trend name",
                    "why_hot": "brief reason",
                    "content_idea": "specific post idea",
                    "urgency": "high/medium/low"
                }}
            ]
        }}"""
        
        try:
            response = self.think(prompt, json_mode=True)
            trends = response.get("trends", [])
            self.log_action("trend_analysis", {"count": len(trends)})
            return trends[:5]  # Top 5 trends
        except Exception as e:
            self.log_action("trend_analysis_failed", {"error": str(e)})
            return [{"topic": f"{niche} daily motivation", "why_hot": "evergreen", "content_idea": "inspirational quote carousel", "urgency": "medium"}]
    
    async def _analyze_competitors(self, niche: str) -> Dict[str, Any]:
        """Simulated competitor analysis. In production, scrape/analyze top pages."""
        prompt = f"""Based on typical successful content in the '{niche}' niche on Instagram,
        what formats and hooks work best right now?
        
        Return JSON:
        {{
            "top_performing_formats": ["format1", "format2"],
            "best_hooks": ["hook1", "hook2"],
            "optimal_caption_length": "short/medium/long",
            "key_elements": ["element1", "element2"]
        }}"""
        
        try:
            return self.think(prompt, json_mode=True)
        except Exception:
            return {
                "top_performing_formats": ["carousel", "reel"],
                "best_hooks": ["Stop scrolling if...", "Nobody talks about..."],
                "optimal_caption_length": "medium",
                "key_elements": ["strong hook", "value delivery", "CTA"]
            }
    
    def _select_content_themes(self, trends: List[Dict], insights: Dict) -> List[Dict]:
        """Mix trending topics with evergreen content."""
        themes = []
        
        # Take top 2 trends
        for trend in trends[:2]:
            themes.append({
                "theme": trend["topic"],
                "type": "trending",
                "content_idea": trend["content_idea"],
                "format": "reel" if trend.get("urgency") == "high" else "carousel"
            })
        
        # Add 1 evergreen post
        themes.append({
            "theme": "Evergreen value post",
            "type": "evergreen",
            "content_idea": "Educational carousel with actionable tips",
            "format": "carousel"
        })
        
        self.log_action("themes_selected", {"count": len(themes)})
        return themes
    
    def _calculate_best_posting_times(self) -> List[str]:
        """Calculate optimal posting times. Can be trained on analytics data."""
        # Default: morning, lunch, evening
        return ["08:00", "12:30", "19:00"]
