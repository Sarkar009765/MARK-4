"""
FastAPI Server - REST API for Social Growth AI
Run: uvicorn server:app --reload
"""
import asyncio
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from core.settings import settings
from agents.orchestrator import Orchestrator
from platforms.manager import PlatformManager
from core.scheduler import scheduler


# Configure logging
logger.add("logs/api.log", rotation="1 day")


# Initialize FastAPI
app = FastAPI(
    title="Social Growth AI API",
    description="Autonomous Social Media Growth Agent API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== Models ====================

class PostContent(BaseModel):
    caption: str
    hashtags: Optional[List[str]] = []
    image_url: Optional[str] = None
    image_path: Optional[str] = None
    format: Optional[str] = "image"


class ScheduleRequest(BaseModel):
    content: PostContent
    time: str  # "08:00"
    platforms: Optional[List[str]] = ["instagram"]


class RunCycleRequest(BaseModel):
    niche: Optional[str] = "motivation"
    platforms: Optional[List[str]] = ["instagram"]
    mode: Optional[str] = "full"  # full, content, engage


# ==================== Routes ====================

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Social Growth AI API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# --- System Status ---

@app.get("/status")
async def get_status():
    """Get overall system status."""
    orchestrator = Orchestrator()
    
    return {
        "orchestrator": orchestrator.get_system_status(),
        "scheduler": scheduler.get_status(),
        "settings": {
            "niche": settings.default_niche,
            "max_posts_per_day": settings.max_posts_per_day,
            "safety_mode": settings.safety_mode
        }
    }


# --- Agent Operations ---

@app.post("/run-cycle")
async def run_cycle(request: RunCycleRequest, background_tasks: BackgroundTasks):
    """
    Run an AI cycle (full, content-only, or engage-only).
    
    - full: Run all agents
    - content: Create content only
    - engage: Run engagement only
    """
    try:
        orchestrator = Orchestrator(
            niche=request.niche,
            platforms=request.platforms
        )
        
        result = await orchestrator.run_cycle(mode=request.mode)
        
        return {
            "status": "success",
            "mode": request.mode,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Cycle failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create-content")
async def create_content(niche: str = "motivation", platforms: List[str] = ["instagram"]):
    """Create new content without publishing."""
    try:
        orchestrator = Orchestrator(niche=niche, platforms=platforms)
        result = await orchestrator.run_cycle(mode="content_only")
        
        return {
            "status": "success",
            "posts": result.get("content", {}).get("posts", [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Publishing ---

@app.post("/publish")
async def publish_post(content: PostContent, platforms: List[str] = ["instagram"]):
    """Publish a post to specified platforms."""
    try:
        manager = PlatformManager(platforms=platforms)
        
        result = await manager.publish_to(
            platform=platforms[0],
            content=content.dict()
        )
        
        return {
            "status": "success",
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/publish-everywhere")
async def publish_everywhere(content: PostContent):
    """Publish same content to all connected platforms."""
    try:
        manager = PlatformManager()
        
        result = await manager.publish_everywhere(content.dict())
        
        return {
            "status": "success",
            "results": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Scheduling ---

@app.post("/schedule")
async def schedule_post(request: ScheduleRequest):
    """Schedule a post for future publishing."""
    try:
        from datetime import timedelta
        
        hour, minute = map(int, request.time.split(":"))
        
        now = datetime.now()
        scheduled_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        if scheduled_time <= now:
            scheduled_time += timedelta(days=1)
        
        post_id = scheduler.schedule_post(
            content=request.content.dict(),
            scheduled_time=scheduled_time,
            platforms=request.platforms
        )
        
        return {
            "status": "scheduled",
            "post_id": post_id,
            "scheduled_for": scheduled_time.isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/scheduled")
async def get_scheduled_posts():
    """Get all scheduled posts."""
    return {
        "pending": scheduler.get_pending_posts(),
        "status": scheduler.get_status()
    }


@app.delete("/schedule/{post_id}")
async def cancel_scheduled_post(post_id: str):
    """Cancel a scheduled post."""
    success = scheduler.cancel_post(post_id)
    
    if success:
        return {"status": "cancelled", "post_id": post_id}
    raise HTTPException(status_code=404, detail="Post not found")


# --- Platform Operations ---

@app.get("/platforms")
async def get_platforms():
    """Get connected platforms status."""
    manager = PlatformManager()
    return manager.get_status()


@app.get("/platforms/{platform}/metrics")
async def get_platform_metrics(platform: str):
    """Get metrics from a specific platform."""
    try:
        manager = PlatformManager(platforms=[platform])
        handler = manager.get_handler(platform)
        
        if not handler:
            raise HTTPException(status_code=404, detail="Platform not found")
        
        metrics = await handler.get_metrics()
        
        return {
            "platform": platform,
            "metrics": metrics
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/platforms/{platform}/test")
async def test_platform(platform: str):
    """Test platform connection."""
    try:
        manager = PlatformManager(platforms=[platform])
        handler = manager.get_handler(platform)
        
        if not handler:
            raise HTTPException(status_code=404, detail="Platform not found")
        
        auth_result = await handler.authenticate()
        
        return {
            "platform": platform,
            "authenticated": auth_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Engagement ---

@app.post("/engage")
async def engage(action: str, target_type: str, target_id: str, text: str = None):
    """
    Perform engagement action.
    
    - action: like, comment, follow, retweet
    - target_type: post, user
    - target_id: ID of the target
    - text: text for comment (optional)
    """
    try:
        manager = PlatformManager()
        
        target = {"post_id": target_id, "user_id": target_id}
        if text:
            target["text"] = text
        
        result = await manager.engage_all(action, target)
        
        return {
            "status": "success",
            "action": action,
            "results": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Quick Actions ---

@app.post("/quick-post")
async def quick_post(prompt: str, platform: str = "instagram"):
    """Quick AI-generated post."""
    try:
        orchestrator = Orchestrator(niche=settings.default_niche, platforms=[platform])
        result = await orchestrator.run_cycle(mode="quick_post")
        
        return {
            "status": "success",
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Server Info ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)