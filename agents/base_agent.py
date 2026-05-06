"""
Base Agent class that all specialized agents inherit from.
Provides common functionality: AI client access, logging, memory, and safety checks.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import json
import time
from datetime import datetime
from loguru import logger

from core.settings import settings
from utils.ai_client import AIClient


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the system.
    
    Every agent must:
    1. Have a name and description
    2. Implement the run() method
    3. Support memory/context of previous actions
    4. Follow safety limits
    """
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.ai = AIClient()
        self.memory: List[Dict[str, Any]] = []
        self.action_count = 0
        self.max_actions_per_hour = 60  # Safety limit
        self.last_action_time = time.time()
        logger.info(f"Agent '{name}' initialized | {description}")
    
    def log_action(self, action: str, details: Dict[str, Any] = None):
        """Log every action the agent takes for audit and memory."""
        entry = {
            "agent": self.name,
            "action": action,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        self.memory.append(entry)
        self.action_count += 1
        logger.info(f"[{self.name}] {action} | {details}")
        return entry
    
    def check_safety_limits(self) -> bool:
        """
        Check if the agent is within safety limits.
        Returns True if safe to proceed, False if limits hit.
        """
        current_time = time.time()
        hour_ago = current_time - 3600
        
        # Count actions in the last hour
        recent_actions = len([m for m in self.memory 
                             if datetime.fromisoformat(m["timestamp"]).timestamp() > hour_ago])
        
        if recent_actions >= self.max_actions_per_hour:
            logger.warning(f"[{self.name}] Hourly action limit reached ({self.max_actions_per_hour})")
            return False
        
        # Rate limiting: max 1 action per 5 seconds minimum
        if current_time - self.last_action_time < 5:
            time.sleep(5 - (current_time - self.last_action_time))
        
        self.last_action_time = time.time()
        return True
    
    def think(self, prompt: str, system_prompt: Optional[str] = None, 
              json_mode: bool = False) -> str | Dict[str, Any]:
        """
        Use the AI brain to think/process information.
        This is the agent's cognitive core.
        """
        if not self.check_safety_limits():
            raise RuntimeError(f"Agent {self.name} hit safety limits")
        
        try:
            response = self.ai.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                json_mode=json_mode
            )
            return response
        except Exception as e:
            logger.error(f"[{self.name}] AI thinking failed: {e}")
            raise
    
    def remember(self, key: str, value: Any):
        """Store something in agent's working memory."""
        self.memory.append({
            "type": "memory",
            "key": key,
            "value": value,
            "timestamp": datetime.now().isoformat()
        })
    
    def recall(self, key: str) -> Optional[Any]:
        """Recall something from agent's working memory."""
        for entry in reversed(self.memory):
            if entry.get("key") == key:
                return entry.get("value")
        return None
    
    @abstractmethod
    async def run(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main execution method for the agent.
        Must be implemented by every agent.
        
        Args:
            context: Shared context from the orchestrator
            
        Returns:
            Dict containing the agent's output/results
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Return current agent status for monitoring."""
        return {
            "name": self.name,
            "description": self.description,
            "total_actions": self.action_count,
            "memory_size": len(self.memory),
            "safety_ok": self.check_safety_limits()
        }
