# Content Agent Prompts
# Prompt templates for generating social media content

# Caption Generation
CAPTION_GENERATION = """Create an engaging Instagram caption for this theme:

Niche: {{niche}}
Theme: {{theme}}
Content Idea: {{content_idea}}
Tone: {{tone}}
Format: {{format}}

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

# Hashtag Generation
HASHTAG_GENERATION = """Generate 15-20 Instagram hashtags for this post:

Niche: {{niche}}
Topic: {{topic}}

Requirements:
- Mix: 3-5 broad (1M+ posts), 5-7 medium (100K-1M), rest niche-specific
- Include trending formats like #{{niche}}tips #{{niche}}daily
- No banned or overly spammy hashtags
- All lowercase, no spaces

Return JSON: {{"hashtags": ["tag1", "tag2", ...]}}"""

# Image Prompt Generation
IMAGE_PROMPT = """Create a detailed prompt for an AI image generator (Midjourney/DALL-E) 
for an Instagram {{format}} about: {{theme}}

Niche: {{niche}}
Style: Aesthetic, modern, Instagram-worthy, high engagement potential

Make it detailed with:
- Visual composition
- Color palette
- Mood/atmosphere
- Any text overlay suggestion

Return ONLY the image generation prompt."""

# Thread/Thread Caption (Twitter)
THREAD_CAPTION = """Create a Twitter thread about this topic:

Topic: {{topic}}
Niche: {{niche}}

Structure:
- Tweet 1: Hook - grab attention
- Tweet 2-5: Main value points (each 280 chars max)
- Tweet 6: Summary + CTA

Rules:
- Each tweet must work standalone
- Use relevant hashtags in last tweet only
- Include a question to drive replies

Return as JSON:
{{
    "tweets": ["tweet1", "tweet2", ...]
}}"""