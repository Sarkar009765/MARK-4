# Strategy Agent Prompts
# Use these as base prompts, customize per your niche

# Trend Analysis Prompt
TREND_ANALYSIS = """Analyze current trending topics in the '{{niche}}' niche.
Consider: viral content themes, popular hashtags, current events related to {{niche}}.

Return JSON with this structure:
{{
    "trends": [
        {{
            "topic": "trend name",
            "why_hot": "brief reason",
            "content_idea": "specific post idea",
            "urgency": "high/medium/low"
        }}
    ]
}}"""

# Competitor Analysis Prompt
COMPETITOR_ANALYSIS = """Based on typical successful content in the '{{niche}}' niche on Instagram,
what formats and hooks work best right now?

Return JSON:
{{
    "top_performing_formats": ["format1", "format2"],
    "best_hooks": ["hook1", "hook2"],
    "optimal_caption_length": "short/medium/long",
    "key_elements": ["element1", "element2"]
}}"""

# Content Theme Selection
THEME_SELECTION = """Based on trends and competitor insights, select the best content themes for today.

Trending Topics:
{{trends}}

What Works:
{{competitor_insights}}

Return JSON:
{{
    "themes": [
        {{
            "theme": "theme name",
            "type": "trending/evergreen/educational",
            "format": "reel/carousel/image",
            "priority": 1-5
        }}
    ]
}}"""