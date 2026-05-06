"""
Platform Manager - Unified interface for all social media platforms.
Automatically handles platform selection and orchestration.
"""
from typing import Dict, Any, List, Optional
from loguru import logger

from platforms.instagram import InstagramHandler
from platforms.facebook import FacebookHandler
from platforms.twitter import TwitterHandler
from core.settings import settings


class PlatformManager:
    """
    Unified platform manager that handles all social media integrations.
    Use this instead of individual handlers for most operations.
    """
    
    def __init__(self, platforms: List[str] = None):
        self.platforms = platforms or ["instagram"]
        self.handlers: Dict[str, Any] = {}
        self._initialize_handlers()
    
    def _initialize_handlers(self):
        """Initialize all requested platform handlers."""
        for platform in self.platforms:
            if platform.lower() == "instagram":
                self.handlers["instagram"] = InstagramHandler()
            elif platform.lower() == "facebook":
                self.handlers["facebook"] = FacebookHandler()
            elif platform.lower() in ["twitter", "x"]:
                self.handlers["twitter"] = TwitterHandler()
            else:
                logger.warning(f"Unknown platform: {platform}")
        
        logger.info(f"Initialized platform handlers: {list(self.handlers.keys())}")
    
    async def publish_everywhere(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Publish the same content to all connected platforms."""
        results = {}
        
        for platform_name, handler in self.handlers.items():
            try:
                result = await handler.publish_post(content)
                results[platform_name] = result
                logger.info(f"Published to {platform_name}: {result.get('status')}")
            except Exception as e:
                logger.error(f"Failed to publish to {platform_name}: {e}")
                results[platform_name] = {"status": "error", "message": str(e)}
        
        return results
    
    async def publish_to(self, platform: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Publish to a specific platform."""
        if platform not in self.handlers:
            return {"status": "error", "message": f"Platform {platform} not configured"}
        
        return await self.handlers[platform].publish_post(content)
    
    async def get_all_metrics(self) -> Dict[str, Dict]:
        """Get metrics from all platforms."""
        results = {}
        
        for platform_name, handler in self.handlers.items():
            try:
                metrics = await handler.get_metrics()
                results[platform_name] = metrics
            except Exception as e:
                logger.error(f"Failed to get metrics from {platform_name}: {e}")
                results[platform_name] = {"error": str(e)}
        
        return results
    
    async def engage_all(self, action: str, target: Dict[str, Any]) -> Dict[str, Any]:
        """Perform engagement action on all platforms."""
        results = {}
        
        for platform_name, handler in self.handlers.items():
            try:
                if action == "like":
                    # Not all platforms support programmatic likes
                    results[platform_name] = {"status": "skipped"}
                elif action == "comment":
                    result = await handler.comment(target.get("post_id"), target.get("text"))
                    results[platform_name] = result
                elif action == "follow":
                    result = await handler.follow_user(target.get("user_id"))
                    results[platform_name] = result
            except Exception as e:
                results[platform_name] = {"status": "error", "message": str(e)}
        
        return results
    
    def get_handler(self, platform: str):
        """Get a specific platform handler."""
        return self.handlers.get(platform.lower())
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of all platforms."""
        return {
            "connected_platforms": list(self.handlers.keys()),
            "handlers": {
                name: handler.get_status()
                for name, handler in self.handlers.items()
            }
        }


# Quick utility function for publishing
async def quick_publish(caption: str, platforms: List[str] = None, image_url: str = None) -> Dict[str, Any]:
    """Quick publish to one or more platforms."""
    manager = PlatformManager(platforms=platforms)
    
    content = {
        "caption": caption,
        "image_url": image_url,
        "hashtags": []
    }
    
    return await manager.publish_everywhere(content)