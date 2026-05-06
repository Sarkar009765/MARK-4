"""
Reply Agent
Handles incoming comments and DMs with AI-powered responses.
The customer service department of the system.
"""
from typing import Dict, Any, List
import random

from agents.base_agent import BaseAgent


class ReplyAgent(BaseAgent):
    """
    Manages all incoming interactions: comments, DMs, mentions.
    Functions:
    - AI-powered comment replies
    - Sentiment analysis (positive/negative/neutral)
    - FAQ handling
    - Escalation to human for complex issues
    """
    
    def __init__(self):
        super().__init__(
            name="ReplyAgent",
            description="Manages audience conversations and replies"
        )
        self.max_actions_per_hour = 50
        self.faq_database = self._load_faq_database()
    
    async def run(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute reply cycle."""
        self.log_action("running_reply_cycle", {})
        
        # 1. Fetch pending interactions (simulated)
        pending = await self._fetch_pending_interactions()
        
        # 2. Process each interaction
        processed = []
        for interaction in pending[:15]:  # Max 15 per cycle
            result = await self._process_interaction(interaction)
            processed.append(result)
        
        result = {
            "status": "success",
            "processed": len(processed),
            "needs_human_attention": [p for p in processed if p.get("escalated")],
            "replies_sent": [p for p in processed if p.get("replied")]
        }
        
        self.log_action("reply_cycle_complete", result)
        return result
    
    async def _fetch_pending_interactions(self) -> List[Dict]:
        """
        Fetch comments/DMs that need replies.
        In production: connect to social media APIs.
        """
        # Simulated interactions
        samples = [
            {"type": "comment", "text": "This is amazing! Love this tip 🔥", "post_topic": "morning routine"},
            {"type": "comment", "text": "Does this actually work? Seems too simple", "post_topic": "productivity hack"},
            {"type": "dm", "text": "Hey can you promote my product?", "sender_type": "unknown"},
            {"type": "comment", "text": "Been following for 2 weeks, already seeing results!", "post_topic": "workout tips"},
            {"type": "comment", "text": "This is wrong and you're misleading people", "post_topic": "diet advice"}
        ]
        
        self.log_action("fetched_interactions", {"count": len(samples)})
        return random.sample(samples, min(3, len(samples)))
    
    async def _process_interaction(self, interaction: Dict) -> Dict:
        """
        Process a single interaction: analyze sentiment, generate reply or escalate.
        """
        text = interaction.get("text", "")
        sentiment = await self._analyze_sentiment(text)
        
        result = {
            "interaction": interaction,
            "sentiment": sentiment,
            "escalated": False,
            "replied": False
        }
        
        # Check if it's spam/promotion
        if self._is_spam_or_promo(text):
            result["action"] = "ignored_spam"
            self.log_action("spam_ignored", {"text_preview": text[:30]})
            return result
        
        # Check FAQ database first
        faq_match = self._check_faq(text)
        if faq_match:
            result["reply"] = faq_match
            result["replied"] = True
            result["reply_type"] = "faq"
            self.log_action("faq_reply_sent", {"question": text[:30]})
            return result
        
        # Negative sentiment or complex -> escalate to human
        if sentiment == "negative" or self._is_complex_query(text):
            result["escalated"] = True
            result["reason"] = "negative_sentiment" if sentiment == "negative" else "complex_query"
            self.log_action("escalated_to_human", {"reason": result["reason"]})
            return result
        
        # Generate AI reply
        reply = await self._generate_reply(interaction, sentiment)
        result["reply"] = reply
        result["replied"] = True
        result["reply_type"] = "ai_generated"
        
        self.log_action("ai_reply_sent", {"sentiment": sentiment})
        return result
    
    async def _analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of the incoming text."""
        prompt = f"""Analyze the sentiment of this social media comment/DM:
"{text}"

Return ONLY one word: positive, negative, or neutral.
Also consider context: questions are usually neutral unless rude."""
        
        try:
            sentiment = self.think(prompt).strip().lower()
            if sentiment not in ["positive", "negative", "neutral"]:
                return "neutral"
            return sentiment
        except Exception:
            # Simple fallback
            negative_words = ["hate", "terrible", "wrong", "misleading", "stupid", "bad", "worst", "don't"]
            positive_words = ["love", "amazing", "great", "best", "awesome", "thanks", "helpful"]
            
            text_lower = text.lower()
            if any(w in text_lower for w in negative_words):
                return "negative"
            elif any(w in text_lower for w in positive_words):
                return "positive"
            return "neutral"
    
    async def _generate_reply(self, interaction: Dict, sentiment: str) -> str:
        """Generate contextual reply based on interaction."""
        prompt = f"""Write a reply to this {interaction['type']} on Instagram:
Their message: "{interaction['text']}"
Topic of post: {interaction.get('post_topic', 'general')}
Detected sentiment: {sentiment}

Rules:
- Match their energy: positive be enthusiastic, neutral be helpful, negative be calm/professional
- Ask a follow-up question when possible (drives engagement)
- Keep it under 2 sentences
- No robotic language
- If it's praise: say thanks + ask a question
- If it's a question: answer directly + encourage discussion
- If it's vague: show curiosity

Return ONLY the reply text."""
        
        try:
            return self.think(prompt).strip().replace('"', '')
        except Exception:
            if sentiment == "positive":
                return "Thanks so much! What part resonated with you most?"
            elif sentiment == "negative":
                return "I appreciate your honesty. What would you suggest instead?"
            return "Great question! Let me know if you want me to dive deeper into this."
    
    def _is_spam_or_promo(self, text: str) -> bool:
        """Detect spam/promotional messages."""
        spam_signals = [
            "check out my", "follow my", "dm for", "promote my", 
            "collab?", "partnership?", "affiliate", "link in bio", 
            "earn money", "make money fast"
        ]
        text_lower = text.lower()
        return any(signal in text_lower for signal in spam_signals)
    
    def _is_complex_query(self, text: str) -> bool:
        """Detect if query needs human attention."""
        complex_signals = [
            "refund", "charge", "payment", " lawsuit", "legal", 
            "report", "harassment", "hack", "account issue"
        ]
        return any(signal in text.lower() for signal in complex_signals)
    
    def _check_faq(self, text: str) -> str | None:
        """Check if question matches FAQ database."""
        text_lower = text.lower()
        for pattern, answer in self.faq_database.items():
            if pattern in text_lower:
                return answer
        return None
    
    def _load_faq_database(self) -> Dict[str, str]:
        """Load common questions and answers."""
        return {
            "what camera": "I use my iPhone mostly! The best camera is the one you have with you.",
            "how often post": "I aim for daily content but quality over quantity always!",
            "phone or camera": "Mostly phone! Editing apps do the magic 💫",
            "what app": "I use a mix of apps - check my story highlights for recommendations!",
            "can you teach": "I share tips here regularly! Save the posts that help you most.",
            "coaching": "I appreciate the interest! Right now my focus is on free content here.",
        }
    
    def add_faq(self, pattern: str, answer: str):
        """Add new FAQ dynamically."""
        self.faq_database[pattern.lower()] = answer
        self.log_action("faq_added", {"pattern": pattern})
