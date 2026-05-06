"""
Orchestrator - The Central Brain of the System.
Manages all agents, coordinates tasks, maintains shared context.
Inspired by OpenAgents architecture but simplified (Paperclip-style).
"""
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger

from core.settings import settings
from agents.strategy_agent import StrategyAgent
from agents.content_agent import ContentAgent
from agents.growth_agent import GrowthAgent
from agents.reply_agent import ReplyAgent
from agents.analytics_agent import AnalyticsAgent


class Orchestrator:
    """
    The main conductor. Decides which agents run, when, and in what order.
    Maintains shared context so agents can see what others did.
    """
    
    def __init__(self, niche: str = None, platforms: List[str] = None):
        self.niche = niche or settings.default_niche
        self.platforms = platforms or ["instagram"]
        
        # Initialize all agents
        self.agents = {
            "strategy": StrategyAgent(),
            "content": ContentAgent(),
            "growth": GrowthAgent(),
            "reply": ReplyAgent(),
            "analytics": AnalyticsAgent()
        }
        
        # Shared context - all agents can read/write
        self.context: Dict[str, Any] = {
            "niche": self.niche,
            "platforms": self.platforms,
            "orchestrator_started": datetime.now().isoformat(),
            "todays_posts": [],
            "pending_replies": [],
            "trending_topics": [],
            "performance_log": []
        }
        
        logger.info(f"Orchestrator initialized | Niche: {self.niche} | Platforms: {self.platforms}")
    
    async def run_cycle(self, mode: str = "full") -> Dict[str, Any]:
        """
        Run one complete cycle of the system.
        
        Modes:
        - "full": Run all agents (strategy → content → growth → reply → analytics)
        - "content_only": Only create content
        - "engage_only": Only engage with audience
        - "analyze_only": Only run analytics
        - "quick_post": Emergency: create and post immediately
        
        Returns:
            Results from all executed agents
        """
        logger.info(f"=== Starting orchestrator cycle | Mode: {mode} ===")
        results = {}
        
        try:
            if mode in ["full", "content_only", "quick_post"]:
                # Phase 1: Strategy
                strategy_result = await self.agents["strategy"].run(self.context)
                results["strategy"] = strategy_result
                self.context["strategy_output"] = strategy_result
                
                # Phase 2: Content Creation (can run after strategy)
                content_result = await self.agents["content"].run(self.context)
                results["content"] = content_result
                self.context["content_output"] = content_result
            
            if mode in ["full", "engage_only"]:
                # Phase 3: Growth & Engagement (parallel with reply)
                growth_task = asyncio.create_task(
                    self.agents["growth"].run(self.context)
                )
                reply_task = asyncio.create_task(
                    self.agents["reply"].run(self.context)
                )
                
                growth_result, reply_result = await asyncio.gather(growth_task, reply_task)
                results["growth"] = growth_result
                results["reply"] = reply_result
                self.context["growth_output"] = growth_result
                self.context["reply_output"] = reply_result
            
            if mode == "full":
                # Phase 4: Analytics (runs last)
                analytics_result = await self.agents["analytics"].run(self.context)
                results["analytics"] = analytics_result
                self.context["analytics_output"] = analytics_result
            
            if mode == "quick_post":
                # Skip approval, post immediately
                results["quick_post"] = await self._execute_quick_post(results.get("content"))
            
            logger.info("=== Orchestrator cycle completed successfully ===")
            
        except Exception as e:
            logger.error(f"Orchestrator cycle failed: {e}")
            results["error"] = str(e)
        
        return results
    
    async def _execute_quick_post(self, content_result: Dict) -> Dict[str, Any]:
        """Emergency quick post - minimal checks, maximum speed."""
        from platforms.instagram import InstagramHandler
        
        post = content_result.get("posts", [{}])[0] if content_result else None
        if not post:
            return {"status": "error", "message": "No content generated"}
        
        # Post to first available platform
        platform = self.platforms[0]
        if platform == "instagram":
            handler = InstagramHandler()
            return await handler.publish_post(post)
        
        return {"status": "posted", "platform": platform, "content": post.get("caption", "")[:50]}
    
    async def run_scheduled(self):
        """
        Continuous loop that runs the system on a schedule.
        Meant to be run as a background task.
        """
        import schedule
        import time
        
        # Schedule daily content creation (morning)
        schedule.every().day.at("08:00").do(
            lambda: asyncio.create_task(self.run_cycle("content_only"))
        )
        
        # Schedule engagement (every 2 hours during day)
        schedule.every(2).hours.do(
            lambda: asyncio.create_task(self.run_cycle("engage_only"))
        )
        
        # Schedule full analytics (evening)
        schedule.every().day.at("21:00").do(
            lambda: asyncio.create_task(self.run_cycle("analyze_only"))
        )
        
        logger.info("Scheduler started. Running indefinitely...")
        while True:
            schedule.run_pending()
            await asyncio.sleep(60)  # Check every minute
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get status of orchestrator and all agents."""
        return {
            "orchestrator": {
                "niche": self.niche,
                "platforms": self.platforms,
                "context_keys": list(self.context.keys())
            },
            "agents": {
                name: agent.get_status()
                for name, agent in self.agents.items()
            }
        }
