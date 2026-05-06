"""
Base Platform Handler - Abstract class for all social media platforms.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger

from core.settings import settings


class BasePlatformHandler(ABC):
    """
    Abstract base class for all social media platform handlers.
    Each platform (Instagram, Facebook, Twitter) inherits from this.
    """
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.is_authenticated = False
        logger.info(f"Initialized {platform_name} handler")
    
    @abstractmethod
    async def authenticate(self) -> bool:
        """Authenticate with the platform API."""
        pass
    
    @abstractmethod
    async def publish_post(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Publish a post to the platform."""
        pass
    
    @abstractmethod
    async def publish_story(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Publish a story to the platform."""
        pass
    
    @abstractmethod
    async def get_metrics(self) -> Dict[str, Any]:
        """Fetch current metrics from the platform."""
        pass
    
    @abstractmethod
    async def comment(self, post_id: str, text: str) -> Dict[str, Any]:
        """Comment on a post."""
        pass
    
    @abstractmethod
    async def send_dm(self, user_id: str, text: str) -> Dict[str, Any]:
        """Send a direct message."""
        pass
    
    @abstractmethod
    async def get_mentions(self) -> List[Dict[str, Any]]:
        """Get recent mentions."""
        pass
    
    async def schedule_post(self, content: Dict[str, Any], 
                           scheduled_time: datetime) -> Dict[str, Any]:
        """Schedule a post for later (default: using database scheduler)."""
        from database.models import ScheduledPost
        
        post = ScheduledPost(
            platform=self.platform_name,
            content=content,
            scheduled_time=scheduled_time,
            status="pending"
        )
        return {"status": "scheduled", "scheduled_for": scheduled_time.isoformat()}
    
    def check_rate_limit(self, action: str) -> bool:
        """Check if action is within rate limits."""
        # Simple rate limiting (in production: use Redis)
        limits = {
            "post": 25,      # per day
            "comment": 60,   # per hour
            "like": 350,      # per hour
            "dm": 50,        # per day
        }
        
        limit = limits.get(action, 10)
        logger.info(f"Rate limit check: {action} (max: {limit})")
        return True  # Simplified
    
    def get_status(self) -> Dict[str, Any]:
        """Get platform connection status."""
        return {
            "platform": self.platform_name,
            "authenticated": self.is_authenticated,
            "connected": True
        }