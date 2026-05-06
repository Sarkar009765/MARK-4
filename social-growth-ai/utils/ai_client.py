"""
AI Client wrapper that supports multiple providers:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Local models via Ollama
"""
import os
import json
from typing import Optional, Dict, Any
from loguru import logger

try:
    import openai
except ImportError:
    openai = None

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import ollama
except ImportError:
    ollama = None

from core.settings import settings


class AIClient:
    """
    Unified AI client that routes to the configured provider.
    Supports function calling style (Hermes-inspired structured outputs).
    Also has a MOCK mode for testing without API keys.
    """
    
    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or settings.ai_provider
        self.mock_mode = False
        
        # Check if API key is available
        if self.provider == "openai" and not settings.openai_api_key:
            logger.warning("No OpenAI API key - using MOCK mode for testing!")
            self.mock_mode = True
        elif self.provider == "anthropic" and not settings.anthropic_api_key:
            logger.warning("No Anthropic API key - using MOCK mode for testing!")
            self.mock_mode = True
        
        if not self.mock_mode:
            self._init_client()
            logger.info(f"AIClient initialized with provider: {self.provider}")
        else:
            logger.info("AIClient initialized in MOCK mode (no API key)")
    
    def _init_client(self):
        """Initialize the specific AI client based on provider."""
        if self.provider == "openai":
            if openai is None:
                raise ImportError("OpenAI package not installed. Run: pip install openai")
            self.client = openai.OpenAI(api_key=settings.openai_api_key)
        
        elif self.provider == "anthropic":
            if anthropic is None:
                raise ImportError("Anthropic package not installed. Run: pip install anthropic")
            self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        
        elif self.provider == "ollama":
            if ollama is None:
                raise ImportError("Ollama package not installed. Run: pip install ollama")
            self.client = None  # Ollama uses module-level functions
        
        else:
            raise ValueError(f"Unknown AI provider: {self.provider}")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None,
                 json_mode: bool = False, max_tokens: int = 2000,
                 temperature: float = 0.7) -> str | Dict[str, Any]:
        """
        Generate text from the AI model.
        Falls back to MOCK mode if no API key is available.
        
        Args:
            prompt: The main user prompt
            system_prompt: System instructions for the AI
            json_mode: Whether to force JSON output
            max_tokens: Maximum tokens to generate
            temperature: Creativity level (0.0 to 1.0)
            
        Returns:
            Generated text or parsed JSON dict
        """
        # Use mock mode if no API key
        if self.mock_mode:
            return self._mock_generate(prompt, system_prompt, json_mode)
        
        try:
            if self.provider == "openai":
                return self._openai_generate(prompt, system_prompt, json_mode, max_tokens, temperature)
            elif self.provider == "anthropic":
                return self._anthropic_generate(prompt, system_prompt, json_mode, max_tokens, temperature)
            elif self.provider == "ollama":
                return self._ollama_generate(prompt, system_prompt, json_mode, max_tokens, temperature)
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            # Fallback to mock on error
            return self._mock_generate(prompt, system_prompt, json_mode)
    
    def _mock_generate(self, prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False) -> str | Dict[str, Any]:
        """
        MOCK mode: Returns simulated responses for testing without API key.
        """
        # Detect what kind of response is needed based on the prompt
        prompt_lower = prompt.lower()
        
        if "trends" in prompt_lower or "trend analysis" in prompt_lower:
            if json_mode:
                return {
                    "trends": [
                        {"topic": "Morning routine optimization", "why_hot": "High engagement on productivity", "content_idea": "5 AM routine for success", "urgency": "high"},
                        {"topic": "Mindset shifts", "why_hot": "Evergreen high-performing", "content_idea": "Growth mindset quotes", "urgency": "medium"}
                    ]
                }
            return "Here are the trending topics in your niche based on current engagement patterns."
        
        elif "competitor" in prompt_lower or "insights" in prompt_lower:
            if json_mode:
                return {
                    "top_performing_formats": ["carousel", "reel"],
                    "best_hooks": ["Stop scrolling if...", "Nobody talks about..."],
                    "optimal_caption_length": "medium",
                    "key_elements": ["strong hook", "value delivery", "CTA"]
                }
            return "Based on competitor analysis, carousels and reels are performing best."
        
        elif "caption" in prompt_lower or "create an engaging" in prompt_lower:
            return """Stop scrolling if you want to level up your life! 🚀

Most people think success is complicated. But it's actually simple:

1. Wake up early
2. Work on your craft
3. Stay consistent

That's it. Nothing fancy.

The problem? Most people want shortcuts. They want hacks. They want easy.

But the truth is: consistency beats talent when talent doesn't show up consistently.

So here's your challenge: Pick ONE thing and do it for 30 days straight.

No exceptions. No excuses.

Drop a "DONE" when you've started 👇

#motivation #success #mindset #growth #goals"""
        
        elif "hashtag" in prompt_lower:
            if json_mode:
                return {"hashtags": ["#motivation", "#success", "#mindset", "#growth", "#goals", "#inspiration", "#entrepreneur", "#hustle", "#successquotes", "#motivationquotes", "#growthmindset", "#dailyMotivation", "#successmindset"]}
            return "#motivation #success #mindset"
        
        elif "comment" in prompt_lower:
            return "This is amazing! Thanks for sharing this insight! 🔥"
        
        elif "sentiment" in prompt_lower:
            return "positive"
        
        elif "reply" in prompt_lower or "respond" in prompt_lower:
            return "Thanks so much! What part resonated with you most?"
        
        elif "recommendations" in prompt_lower or "analytics" in prompt_lower:
            if json_mode:
                return {
                    "recommendations": [
                        {"priority": "high", "action": "Post more carousels", "reason": "Highest engagement format", "expected_impact": "+5% engagement"},
                        {"priority": "medium", "action": "Post at 12:30 PM", "reason": "Best performing time", "expected_impact": "+3% reach"},
                        {"priority": "low", "action": "Add more hashtags", "reason": "Improve discoverability", "expected_impact": "+2% discovery"}
                    ]
                }
            return "Post more carousels at 12:30 PM for better engagement."
        
        # Default response
        if json_mode:
            return {"result": "success", "message": "Mock response"}
        return "This is a mock response for testing. Add your API key to get real AI responses!"
    
    def _openai_generate(self, prompt, system_prompt, json_mode, max_tokens, temperature):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        kwargs = {
            "model": "gpt-4",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        
        response = self.client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content
        
        if json_mode:
            return json.loads(content)
        return content
    
    def _anthropic_generate(self, prompt, system_prompt, json_mode, max_tokens, temperature):
        # Build system prompt for JSON mode
        if json_mode and system_prompt:
            system_prompt += "\nRespond ONLY with valid JSON."
        elif json_mode:
            system_prompt = "Respond ONLY with valid JSON."
        
        message = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt or "",
            messages=[{"role": "user", "content": prompt}]
        )
        content = message.content[0].text
        
        if json_mode:
            # Extract JSON if wrapped in markdown
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            return json.loads(content)
        return content
    
    def _ollama_generate(self, prompt, system_prompt, json_mode, max_tokens, temperature):
        response = ollama.chat(
            model=settings.ollama_model,
            messages=[
                {"role": "system", "content": system_prompt or "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            options={"temperature": temperature, "num_predict": max_tokens}
        )
        content = response["message"]["content"]
        
        if json_mode:
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Try to extract JSON from text
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                raise
        return content
    
    def function_call(self, prompt: str, functions: list, 
                     system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Hermes-style function calling: AI picks a function with arguments.
        
        Args:
            prompt: User request
            functions: List of function schemas
            system_prompt: Optional system instructions
            
        Returns:
            {"function": "name", "arguments": {...}}
        """
        func_schema = json.dumps(functions, indent=2)
        full_prompt = f"""You have access to these functions:
{func_schema}

User request: {prompt}

Respond with ONLY a JSON object in this exact format:
{{"function": "function_name", "arguments": {{...}}}}
"""
        response = self.generate(
            prompt=full_prompt,
            system_prompt=system_prompt,
            json_mode=True
        )
        return response


# Backward compatibility / direct utility
def quick_ai(prompt: str, **kwargs) -> str:
    """Quick one-off AI call without instantiating client."""
    client = AIClient()
    return client.generate(prompt, **kwargs)
