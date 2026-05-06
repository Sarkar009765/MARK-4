"""
Facebook Platform Handler
Manages Facebook Page operations: posts, comments, insights.
"""
import asyncio
from typing import Dict, Any, List
from datetime import datetime

from platforms.base_handler import BasePlatformHandler
from core.settings import settings


class FacebookHandler(BasePlatformHandler):
    """
    Facebook Graph API handler for Pages.
    Requires: Facebook Page + App with appropriate permissions.
    """
    
    def __init__(self):
        super().__init__("facebook")
        self.access_token = settings.facebook_access_token
        self.page_id = settings.facebook_page_id
        self.api_version = "v18.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
    
    async def authenticate(self) -> bool:
        """Verify Facebook access token."""
        import httpx
        
        if not self.access_token or not self.page_id:
            logger.warning("Facebook credentials not configured")
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/me",
                    params={"access_token": self.access_token}
                )
                data = response.json()
                
                if "error" in data:
                    logger.error(f"Facebook auth error: {data['error']}")
                    return False
                
                self.is_authenticated = True
                logger.info(f"Facebook authenticated: {data.get('name')}")
                return True
        except Exception as e:
            logger.error(f"Facebook auth failed: {e}")
            return False
    
    async def publish_post(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Publish a post to Facebook Page."""
        import httpx
        
        if not self.is_authenticated:
            await self.authenticate()
        
        if not self.check_rate_limit("post"):
            return {"status": "error", "message": "Rate limit exceeded"}
        
        post_data = {
            "message": content.get("caption", ""),
            "access_token": self.access_token
        }
        
        # Add media if available
        if content.get("image_url"):
            post_data["url"] = content.get("image_url")
            endpoint = f"{self.base_url}/{self.page_id}/photos"
        else:
            endpoint = f"{self.base_url}/{self.page_id}/feed"
        
        logger.info(f"Publishing Facebook post...")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(endpoint, data=post_data)
                result = response.json()
                
                if "error" in result:
                    logger.error(f"FB post error: {result['error']}")
                    return {"status": "error", "message": result['error']['message']}
                
                return {
                    "status": "published",
                    "platform": "facebook",
                    "post_id": result.get("id"),
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Facebook post failed: {e}")
            return {"status": "error", "message": str(e)}
    
    async def publish_story(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Facebook Stories (limited API support)."""
        logger.info("Facebook Stories not fully supported via API")
        return {"status": "skipped", "message": "Use Facebook Creator Studio"}
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get Facebook Page insights."""
        import httpx
        
        if not self.is_authenticated:
            await self.authenticate()
        
        metrics = [
            "page_followers",
            "page_likes",
            "page_impressions",
            "page_engaged_users",
            "page_post_clicks"
        ]
        
        params = {
            "metrics": ",".join(metrics),
            "access_token": self.access_token
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/{self.page_id}/insights",
                    params=params
                )
                data = response.json()
                
                if "data" in data:
                    return {
                        "followers": self._find_metric(data["data"], "page_followers"),
                        "likes": self._find_metric(data["data"], "page_likes"),
                        "impressions": self._find_metric(data["data"], "page_impressions"),
                        "engagement": self._find_metric(data["data"], "page_engaged_users")
                    }
        except Exception as e:
            logger.error(f"FB metrics error: {e}")
        
        return {"followers": 0, "error": str(e)}
    
    def _find_metric(self, data: List, metric_name: str):
        for item in data:
            if item.get("name") == metric_name:
                values = item.get("values", [])
                if values:
                    return values[-1].get("value", 0)
        return 0
    
    async def comment(self, post_id: str, text: str) -> Dict[str, Any]:
        """Comment on a post."""
        import httpx
        
        if not self.check_rate_limit("comment"):
            return {"status": "error", "message": "Rate limit exceeded"}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/{post_id}/comments",
                    data={
                        "message": text,
                        "access_token": self.access_token
                    }
                )
                result = response.json()
                
                if "id" in result:
                    return {"status": "success", "comment_id": result["id"]}
                return {"status": "error", "message": result.get("error", {}).get("message", "Unknown")}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def send_dm(self, user_id: str, text: str) -> Dict[str, Any]:
        """Send direct message (requires page_messages permission)."""
        logger.warning("DM requires 'pages_messaging' permission")
        return {"status": "error", "message": "Requires additional permissions"}
    
    async def get_mentions(self) -> List[Dict[str, Any]]:
        """Get page mentions."""
        import httpx
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/{self.page_id}/mentions",
                    params={"access_token": self.access_token}
                )
                data = response.json()
                return data.get("data", [])
        except Exception as e:
            logger.error(f"FB mentions error: {e}")
            return []