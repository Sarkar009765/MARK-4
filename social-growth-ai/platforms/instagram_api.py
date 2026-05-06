"""
Instagram Real API Integration using instagrapi.
This provides actual Instagram automation capabilities.
"""
import os
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger

from platforms.base_handler import BasePlatformHandler


class InstagramAPIHandler(BasePlatformHandler):
    """
    Real Instagram handler using instagrapi library.
    Provides full Instagram automation capabilities.
    """
    
    def __init__(self, username: str = None, password: str = None):
        super().__init__("instagram_instagrapi")
        self.username = username or os.getenv("INSTAGRAM_USERNAME")
        self.password = password or os.getenv("INSTAGRAM_PASSWORD")
        self.client = None
        self.device_id = None
        
    async def authenticate(self) -> bool:
        """Login to Instagram using instagrapi."""
        try:
            from instagrapi import Client
            from instagrapi.exceptions import LoginException
            
            self.client = Client()
            
            # Try to load session first
            session_file = f"sessions/ig_{self.username}.json"
            if os.path.exists(session_file):
                self.client.load_settings(session_file)
                logger.info(f"Loaded existing session for {self.username}")
            
            # Login
            self.client.login(self.username, self.password)
            
            # Save session for next time
            os.makedirs("sessions", exist_ok=True)
            self.client.dump_settings(session_file)
            
            self.is_authenticated = True
            logger.info(f"✅ Instagram authenticated: {self.username}")
            return True
            
        except ImportError:
            logger.error("instagrapi not installed: pip install instagrapi")
            return False
        except Exception as e:
            logger.error(f"Instagram login failed: {e}")
            return False
    
    async def publish_post(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Publish photo or video post."""
        if not self.is_authenticated:
            await self.authenticate()
        
        if not self.client:
            return {"status": "error", "message": "Not authenticated"}
        
        try:
            from instagrapi import Client
            
            caption = content.get("caption", "")
            hashtags = content.get("hashtags", [])
            
            if hashtags:
                caption += "\n\n" + " ".join(hashtags)
            
            # Handle different media types
            if content.get("image_path"):
                # Local file
                media = self.client.photo_upload(
                    content["image_path"],
                    caption
                )
            elif content.get("image_url"):
                # Download from URL first
                import httpx
                async with httpx.AsyncClient() as client:
                    resp = await client.get(content["image_url"])
                    image_data = resp.content
                
                # Save temp file
                temp_path = f"temp_image_{datetime.now().timestamp()}.jpg"
                with open(temp_path, "wb") as f:
                    f.write(image_data)
                
                media = self.client.photo_upload(temp_path, caption)
                
                # Cleanup
                os.remove(temp_path)
            elif content.get("video_path"):
                media = self.client.video_upload(
                    content["video_path"],
                    caption
                )
            else:
                return {"status": "error", "message": "No media provided"}
            
            return {
                "status": "published",
                "platform": "instagram",
                "post_id": str(media.pk),
                "caption_preview": caption[:100],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Instagram post failed: {e}")
            return {"status": "error", "message": str(e)}
    
    async def publish_carousel(self, images: List[str], caption: str) -> Dict[str, Any]:
        """Publish carousel (album) post."""
        if not self.client:
            await self.authenticate()
        
        try:
            media = self.client.album_upload(images, caption)
            return {
                "status": "published",
                "type": "carousel",
                "post_id": str(media.pk)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def publish_story(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Publish story (photo or video)."""
        if not self.client:
            await self.authenticate()
        
        try:
            if content.get("image_path"):
                media = self.client.photo_upload_to_story(content["image_path"])
            elif content.get("video_path"):
                media = self.client.video_upload_to_story(content["video_path"])
            else:
                return {"status": "error", "message": "No media"}
            
            return {
                "status": "published",
                "type": "story",
                "story_id": str(media.pk)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get account insights."""
        if not self.client:
            await self.authenticate()
        
        try:
            # Get user info
            user_id = self.client.user_id
            user_info = self.client.user_info(user_id)
            
            return {
                "followers": user_info.follower_count,
                "following": user_info.following_count,
                "posts": user_info.media_count,
                "biography": user_info.biography,
                "username": user_info.username
            }
        except Exception as e:
            logger.error(f"Failed to get metrics: {e}")
            return {"error": str(e)}
    
    async def comment(self, post_id: str, text: str) -> Dict[str, Any]:
        """Comment on a post."""
        if not self.client:
            await self.authenticate()
        
        try:
            result = self.client.comment(post_id, text)
            return {
                "status": "success",
                "comment_id": str(result.pk)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def send_dm(self, user_id: str, text: str) -> Dict[str, Any]:
        """Send direct message."""
        if not self.client:
            await self.authenticate()
        
        try:
            # user_id can be username or user_id
            thread = self.client.send_direct_message(user_id, text)
            return {
                "status": "sent",
                "thread_id": str(thread.pk)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def get_mentions(self) -> List[Dict[str, Any]]:
        """Get recent comments and mentions."""
        if not self.client:
            await self.authenticate()
        
        try:
            # Get recent posts
            posts = self.client.user_medias(self.client.user_id, 10)
            
            mentions = []
            for post in posts:
                comments = self.client.media_comments(post.pk)
                for comment in comments:
                    mentions.append({
                        "type": "comment",
                        "post_id": str(post.pk),
                        "user": comment.user.username,
                        "text": comment.text,
                        "comment_id": str(comment.pk)
                    })
            
            return mentions
        except Exception as e:
            logger.error(f"Failed to get mentions: {e}")
            return []
    
    async def follow_user(self, username: str) -> Dict[str, Any]:
        """Follow a user."""
        if not self.client:
            await self.authenticate()
        
        try:
            user_id = self.client.user_id_from_username(username)
            self.client.user_follow(user_id)
            return {"status": "success", "username": username}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def unfollow_user(self, username: str) -> Dict[str, Any]:
        """Unfollow a user."""
        if not self.client:
            await self.authenticate()
        
        try:
            user_id = self.client.user_id_from_username(username)
            self.client.user_unfollow(user_id)
            return {"status": "success", "username": username}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def like_post(self, post_id: str) -> Dict[str, Any]:
        """Like a post."""
        if not self.client:
            await self.authenticate()
        
        try:
            self.client.media_like(post_id)
            return {"status": "success", "post_id": post_id}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def get_user_posts(self, username: str, count: int = 10) -> List[Dict]:
        """Get user's recent posts."""
        if not self.client:
            await self.authenticate()
        
        try:
            user_id = self.client.user_id_from_username(username)
            posts = self.client.user_medias(user_id, count)
            return [
                {
                    "id": str(p.pk),
                    "caption": p.caption,
                    "likes": p.like_count,
                    "comments": p.comment_count,
                    "type": p.media_type
                }
                for p in posts
            ]
        except Exception as e:
            return []