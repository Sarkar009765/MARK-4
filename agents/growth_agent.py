"""
Growth Agent
Handles audience growth activities: smart engagement, follow strategies.
The 'marketing muscle' of the system.
"""
from typing import Dict, Any, List
import random
from datetime import datetime

from agents.base_agent import BaseAgent


class GrowthAgent(BaseAgent):
    """
    Manages growth activities to increase followers and reach.
    Functions:
    - Smart engagement (like/comment on target audience posts)
    - Follow/unfollow strategy
    - DM automation (welcome, responses)
    - Cross-promotion coordination
    """
    
    def __init__(self):
        super().__init__(
            name="GrowthAgent",
            description="Drives audience growth through engagement"
        )
        self.max_actions_per_hour = 40  # Conservative for safety
        self.engagement_pool: List[Dict] = []  # Posts to engage with
    
    async def run(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute growth cycle."""
        niche = context.get("niche", "general") if context else "general"
        
        self.log_action("running_growth_cycle", {"niche": niche})
        
        # 1. Discover posts to engage with
        targets = await self._discover_targets(niche)
        
        # 2. Smart engagement
        engagement_results = await self._engage_with_targets(targets)
        
        # 3. Check for new followers to welcome
        welcome_results = await self._welcome_new_followers()
        
        result = {
            "status": "success",
            "engagement_count": len(engagement_results),
            "welcome_count": len(welcome_results),
            "targets_found": len(targets),
            "executed_at": datetime.now().isoformat()
        }
        
        self.log_action("growth_cycle_complete", result)
        return result
    
    async def _discover_targets(self, niche: str) -> List[Dict]:
        """
        Discover posts/accounts to engage with.
        In production, this scrapes relevant hashtags, competitor followers, etc.
        """
        # Simulated target discovery
        sample_targets = [
            {"platform": "instagram", "type": "hashtag_post", "tag": niche, "priority": "high"},
            {"platform": "instagram", "type": "competitor_follower", "account": f"top_{niche}_page", "priority": "medium"},
            {"platform": "instagram", "type": "recent_post", "hashtag": f"{niche}community", "priority": "medium"}
        ]
        
        self.log_action("targets_discovered", {"count": len(sample_targets)})
        return sample_targets[:5]  # Limit targets per cycle
    
    async def _engage_with_targets(self, targets: List[Dict]) -> List[Dict]:
        """
        Engage with discovered targets.
        Uses AI to write contextual comments (not spam!).
        """
        results = []
        
        for target in targets:
            if not self.check_safety_limits():
                break
            
            action = random.choice(["like", "comment"])
            
            if action == "comment":
                comment_text = await self._generate_comment(target)
                result = {
                    "action": "comment",
                    "target": target,
                    "text": comment_text,
                    "status": "simulated"  # Change to "executed" when live
                }
            else:
                result = {
                    "action": "like",
                    "target": target,
                    "status": "simulated"
                }
            
            results.append(result)
            self.log_action(f"engaged_{action}", {"target_type": target.get("type")})
        
        return results
    
    async def _generate_comment(self, target: Dict) -> str:
        """Generate a contextual, non-spamy comment."""
        prompt = f"""Write a short, genuine Instagram comment for a post about {target.get('tag', 'this topic')}.

Rules:
- Must sound human and authentic (NOT generic like "Nice post!" or "Great content!")
- Add a tiny bit of value or personal touch
- 1-2 sentences max
- No emojis unless it feels natural
- NO self-promotion or "DM me" or "Check my page"

Examples of good comments:
- "This hits different today. Needed this reminder!"
- "How long did it take you to see results? Curious about the process"
- "The part about consistency is so true. Struggling with that right now"
- "Saving this for later 🔥 solid framework"

Return ONLY the comment text."""
        
        try:
            return self.think(prompt).strip().replace('"', '')
        except Exception:
            return "This is genuinely helpful. Thanks for sharing this!"
    
    async def _welcome_new_followers(self) -> List[Dict]:
        """
        Send welcome DMs to new followers.
        Only sends if enabled and within limits.
        """
        # In production: check database/API for new followers
        # For now: simulated
        welcomed = []
        
        # Safety: max 5 welcome DMs per cycle
        max_welcome = 5
        for _ in range(random.randint(0, max_welcome)):
            if not self.check_safety_limits():
                break
            
            welcome_msg = await self._generate_welcome_dm()
            welcomed.append({
                "action": "welcome_dm",
                "message": welcome_msg,
                "status": "simulated"
            })
            self.log_action("welcome_dm_sent", {})
        
        return welcomed
    
    async def _generate_welcome_dm(self) -> str:
        """Generate a non-spamy welcome message."""
        prompt = """Write a short, warm welcome DM for a new Instagram follower.

Rules:
- No sales pitch
- No links
- Acknowledge them personally
- 1-2 sentences
- Optional: ask one engaging question

Examples:
- "Hey! Thanks for following along. What brings you here?"
- "Appreciate the follow! What kind of content do you want to see more of?"
- "Welcome to the community! 🙌 What's your biggest goal right now?"

Return ONLY the message."""
        
        try:
            return self.think(prompt).strip()
        except Exception:
            return "Hey! Thanks for the follow. What brings you here?"
    
    def set_engagement_limits(self, max_comments_per_hour: int = 10, 
                             max_likes_per_hour: int = 30):
        """Adjust safety limits based on account age/trust score."""
        self.max_actions_per_hour = max_comments_per_hour + max_likes_per_hour
        self.log_action("limits_updated", {
            "max_comments": max_comments_per_hour,
            "max_likes": max_likes_per_hour
        })
