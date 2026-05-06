"""
Content Agent
Creates high-quality social media content: captions, hooks, hashtags.
The creative engine of the system.
"""
from typing import Dict, Any, List
from datetime import datetime

from agents.base_agent import BaseAgent


class ContentAgent(BaseAgent):
    """
    Generates social media posts, captions, and content ideas.
    Functions:
    - Caption generation with viral hooks
    - Hashtag research and optimization
    - Image/video prompt generation (for AI image tools)
    - Content batching (creates multiple posts at once)
    """
    
    def __init__(self):
        super().__init__(
            name="ContentAgent",
            description="Creates viral social media content"
        )
        self.max_actions_per_hour = 30
        self.tone_options = ["motivational", "educational", "entertaining", "professional"]
    
    async def run(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute content creation cycle."""
        strategy = context.get("strategy_output", {}) if context else {}
        themes = strategy.get("content_themes", [])
        niche = context.get("niche", "general") if context else "general"
        
        self.log_action("running_content_cycle", {"themes_count": len(themes)})
        
        if not themes:
            themes = [{"theme": f"Daily {niche} tips", "type": "evergreen", "format": "carousel"}]
        
        posts = []
        for i, theme in enumerate(themes):
            post = await self._create_post(theme, niche, strategy)
            posts.append(post)
        
        result = {
            "status": "success",
            "posts": posts,
            "created_at": datetime.now().isoformat()
        }
        
        self.log_action("content_created", {"posts": len(posts)})
        return result
    
    async def _create_post(self, theme: Dict, niche: str, strategy: Dict) -> Dict[str, Any]:
        """Create a single complete post."""
        tone = self._determine_tone(theme)
        
        # Generate caption with hook
        caption = await self._generate_caption(theme, niche, tone)
        
        # Generate hashtags
        hashtags = await self._generate_hashtags(theme, niche)
        
        # Generate image prompt for AI image generation
        image_prompt = await self._generate_image_prompt(theme, niche)
        
        post = {
            "theme": theme["theme"],
            "type": theme.get("type", "evergreen"),
            "format": theme.get("format", "single_image"),
            "tone": tone,
            "caption": caption,
            "hashtags": hashtags,
            "image_prompt": image_prompt,
            "status": "draft",  # draft | approved | published
            "scheduled_time": None
        }
        
        self.log_action("post_created", {"theme": theme["theme"], "format": post["format"]})
        return post
    
    def _determine_tone(self, theme: Dict) -> str:
        """Pick appropriate tone based on content type."""
        if theme.get("type") == "trending":
            return "entertaining"
        elif "tip" in theme.get("theme", "").lower() or "how" in theme.get("theme", "").lower():
            return "educational"
        return "motivational"
    
    async def _generate_caption(self, theme: Dict, niche: str, tone: str) -> str:
        """Generate engaging caption with viral structure."""
        prompt = f"""Create an engaging Instagram caption for this theme:

Niche: {niche}
Theme: {theme['theme']}
Content Idea: {theme.get('content_idea', '')}
Tone: {tone}
Format: {theme.get('format', 'post')}

The caption MUST follow this viral structure:
1. HOOK (first line): Attention-grabbing, create curiosity. Use power words.
2. VALUE: Deliver the actual content/tips. Use line breaks and emojis.
3. STORY/PROOF: Brief relatable story or example (optional but effective).
4. CTA: Clear call-to-action (comment, save, share, tag friend).

Rules:
- Use emojis strategically (not overkill)
- Short paragraphs (1-2 sentences each)
- Avoid generic advice, be specific
- Include at least one power word in the hook
- Make the first line so compelling people HAVE to read the rest

Return ONLY the caption text, nothing else."""
        
        try:
            caption = self.think(prompt)
            return caption.strip()
        except Exception:
            # Fallback caption
            return f"Stop scrolling if you want to level up your {niche} game! 🔥\n\nThis one tip changed everything for me...\n\nWhat's your biggest {niche} struggle? Drop it below! 👇"
    
    async def _generate_hashtags(self, theme: Dict, niche: str) -> List[str]:
        """Generate optimized hashtag set."""
        prompt = f"""Generate 15-20 Instagram hashtags for this post:

Niche: {niche}
Topic: {theme['theme']}

Requirements:
- Mix: 3-5 broad (1M+ posts), 5-7 medium (100K-1M), rest niche-specific
- Include trending formats like #{niche}tips #{niche}daily
- No banned or overly spammy hashtags
- All lowercase, no spaces

Return JSON: {{"hashtags": ["tag1", "tag2", ...]}}"""
        
        try:
            response = self.think(prompt, json_mode=True)
            tags = response.get("hashtags", [])
            # Ensure niche is included
            if f"#{niche}" not in tags and niche.replace(" ", "") not in [t.replace("#", "") for t in tags]:
                tags.append(f"#{niche.replace(' ', '')}")
            return tags[:20]
        except Exception:
            return [
                f"#{niche.replace(' ', '')}",
                f"#{niche.replace(' ', '')}tips",
                f"#{niche.replace(' ', '')}daily",
                "#growth",
                "#success",
                "#mindset",
                "#motivation",
                "#viral",
                "#trending"
            ]
    
    async def _generate_image_prompt(self, theme: Dict, niche: str) -> str:
        """Generate AI image generation prompt."""
        prompt = f"""Create a detailed prompt for an AI image generator (Midjourney/DALL-E) 
for an Instagram {theme.get('format', 'post')} about: {theme['theme']}

Niche: {niche}
Style: Aesthetic, modern, Instagram-worthy, high engagement potential

Make it detailed with:
- Visual composition
- Color palette
- Mood/atmosphere
- Any text overlay suggestion

Return ONLY the image generation prompt."""
        
        try:
            return self.think(prompt).strip()
        except Exception:
            return f"Aesthetic Instagram {theme.get('format', 'post')} about {theme['theme']}, modern minimalist design, vibrant colors, professional photography style, 4k"
    
    def batch_create_variations(self, base_post: Dict, count: int = 3) -> List[Dict]:
        """Create multiple variations of a post for A/B testing."""
        variations = []
        for i in range(count):
            variation = base_post.copy()
            variation["variant_id"] = f"v{i+1}"
            # Could vary hook, CTA, hashtags
            variations.append(variation)
        return variations
