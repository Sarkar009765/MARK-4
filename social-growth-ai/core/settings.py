"""
Core configuration and settings management for the Social Growth AI.
Uses pydantic-settings for type-safe environment/config handling.
"""
import os
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""
    
    # AI Provider Configuration
    ai_provider: str = Field(default="openai", alias="AI_PROVIDER")
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, alias="ANTHROPIC_API_KEY")
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="llama2", alias="OLLAMA_MODEL")
    
    # Database
    database_url: str = Field(default="sqlite:///social_growth.db", alias="DATABASE_URL")
    
    # Redis / Celery
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    
    # Instagram
    instagram_username: Optional[str] = Field(default=None, alias="INSTAGRAM_USERNAME")
    instagram_password: Optional[str] = Field(default=None, alias="INSTAGRAM_PASSWORD")
    
    # Facebook
    facebook_access_token: Optional[str] = Field(default=None, alias="FACEBOOK_ACCESS_TOKEN")
    facebook_page_id: Optional[str] = Field(default=None, alias="FACEBOOK_PAGE_ID")
    
    # Twitter
    twitter_api_key: Optional[str] = Field(default=None, alias="TWITTER_API_KEY")
    twitter_api_secret: Optional[str] = Field(default=None, alias="TWITTER_API_SECRET")
    twitter_access_token: Optional[str] = Field(default=None, alias="TWITTER_ACCESS_TOKEN")
    twitter_access_secret: Optional[str] = Field(default=None, alias="TWITTER_ACCESS_SECRET")
    
    # General Settings
    default_niche: str = Field(default="motivation", alias="DEFAULT_NICHE")
    max_posts_per_day: int = Field(default=3, alias="MAX_POSTS_PER_DAY")
    engagement_enabled: bool = Field(default=True, alias="ENGAGEMENT_ENABLED")
    auto_approve_posts: bool = Field(default=False, alias="AUTO_APPROVE_POSTS")
    safety_mode: str = Field(default="strict", alias="SAFETY_MODE")
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
