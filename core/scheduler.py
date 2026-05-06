"""
Post Scheduler - Automated scheduling and publishing of content.
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Callable
from loguru import logger

from core.settings import settings


class PostScheduler:
    """
    Manages scheduled posts with automatic execution.
    Uses asyncio for non-blocking scheduling.
    """
    
    def __init__(self):
        self.scheduled_posts: List[Dict[str, Any]] = []
        self.is_running = False
        logger.info("PostScheduler initialized")
    
    def schedule_post(self, content: Dict[str, Any], 
                     scheduled_time: datetime,
                     platforms: List[str] = None) -> str:
        """Schedule a post for future publishing."""
        post_id = f"post_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        scheduled = {
            "id": post_id,
            "content": content,
            "scheduled_time": scheduled_time,
            "platforms": platforms or ["instagram"],
            "status": "pending",
            "created_at": datetime.now()
        }
        
        self.scheduled_posts.append(scheduled)
        logger.info(f"Scheduled post {post_id} for {scheduled_time}")
        
        return post_id
    
    def schedule_daily(self, content: Dict[str, Any],
                      time: str,  # "08:00"
                      platforms: List[str] = None) -> str:
        """Schedule a post to run daily at a specific time."""
        hour, minute = map(int, time.split(":"))
        
        now = datetime.now()
        scheduled_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # If time has passed today, schedule for tomorrow
        if scheduled_time <= now:
            scheduled_time += timedelta(days=1)
        
        return self.schedule_post(content, scheduled_time, platforms)
    
    def schedule_weekly(self, content: Dict[str, Any],
                       day_of_week: int,  # 0=Monday, 6=Sunday
                       time: str,
                       platforms: List[str] = None) -> str:
        """Schedule a post to run weekly on a specific day and time."""
        import calendar
        
        now = datetime.now()
        days_ahead = day_of_week - now.weekday()
        
        if days_ahead <= 0:
            days_ahead += 7
        
        scheduled_time = now + timedelta(days=days_ahead)
        hour, minute = map(int, time.split(":"))
        scheduled_time = scheduled_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        return self.schedule_post(content, scheduled_time, platforms)
    
    async def start(self, publish_callback: Callable):
        """
        Start the scheduler loop.
        
        Args:
            publish_callback: Async function to call when it's time to publish
        """
        self.is_running = True
        logger.info("Scheduler started")
        
        while self.is_running:
            await self._check_and_publish(publish_callback)
            await asyncio.sleep(60)  # Check every minute
    
    async def _check_and_publish(self, publish_callback: Callable):
        """Check if any posts need to be published."""
        now = datetime.now()
        
        for post in self.scheduled_posts:
            if post["status"] == "pending" and post["scheduled_time"] <= now:
                logger.info(f"Publishing scheduled post: {post['id']}")
                
                try:
                    result = await publish_callback(post["content"], post["platforms"])
                    post["status"] = "published"
                    post["published_at"] = now
                    post["result"] = result
                    logger.info(f"Post {post['id']} published successfully")
                except Exception as e:
                    post["status"] = "failed"
                    post["error"] = str(e)
                    logger.error(f"Failed to publish {post['id']}: {e}")
    
    def stop(self):
        """Stop the scheduler."""
        self.is_running = False
        logger.info("Scheduler stopped")
    
    def get_pending_posts(self) -> List[Dict[str, Any]]:
        """Get all pending scheduled posts."""
        return [p for p in self.scheduled_posts if p["status"] == "pending"]
    
    def cancel_post(self, post_id: str) -> bool:
        """Cancel a scheduled post."""
        for post in self.scheduled_posts:
            if post["id"] == post_id and post["status"] == "pending":
                post["status"] = "cancelled"
                logger.info(f"Cancelled post: {post_id}")
                return True
        return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get scheduler status."""
        return {
            "is_running": self.is_running,
            "total_scheduled": len(self.scheduled_posts),
            "pending": len([p for p in self.scheduled_posts if p["status"] == "pending"]),
            "published": len([p for p in self.scheduled_posts if p["status"] == "published"]),
            "failed": len([p for p in self.scheduled_posts if p["status"] == "failed"])
        }


# Global scheduler instance
scheduler = PostScheduler()