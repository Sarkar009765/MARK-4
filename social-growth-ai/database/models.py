"""
Database Models - SQLAlchemy ORM for data persistence.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class Post(Base):
    """Content post model."""
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    platform: Mapped[str] = mapped_column(String(50))
    content_type: Mapped[str] = mapped_column(String(50))  # image, video, carousel
    
    # Content
    caption: Mapped[str] = mapped_column(Text)
    hashtags: Mapped[Optional[str]] = mapped_column(Text)  # JSON string
    media_urls: Mapped[Optional[str]] = mapped_column(Text)  # JSON array
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft, approved, scheduled, published
    scheduled_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    published_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Metrics (after publishing)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    comments: Mapped[int] = mapped_column(Integer, default=0)
    shares: Mapped[int] = mapped_column(Integer=0)
    reach: Mapped[int] = mapped_column(Integer, default=0)
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Post {self.id} - {self.platform} - {self.status}>"


class ScheduledPost(Base):
    """Scheduled posts waiting to be published."""
    __tablename__ = "scheduled_posts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    platform: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(JSON)  # Full content dict
    
    scheduled_time: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, published, failed
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<ScheduledPost {self.id} - {self.platform} - {self.scheduled_time}>"


class Engagement(Base):
    """Track all engagement actions."""
    __tablename__ = "engagements"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    action_type: Mapped[str] = mapped_column(String(30))  # like, comment, follow, dm
    target_platform: Mapped[str] = mapped_column(String(50))
    target_id: Mapped[str] = mapped_column(String(100))  # post/user ID
    
    content: Mapped[Optional[str]] = mapped_column(Text)  # For comments/DMs
    
    status: Mapped[str] = mapped_column(String(20), default="success")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Engagement {self.id} - {self.action_type} - {self.target_platform}>"


class Analytics(Base):
    """Daily analytics snapshot."""
    __tablename__ = "analytics"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    platform: Mapped[str] = mapped_column(String(50))
    
    # Follower metrics
    followers: Mapped[int] = mapped_column(Integer)
    follower_change: Mapped[int] = mapped_column(Integer, default=0)
    
    # Content metrics
    posts_published: Mapped[int] = mapped_column(Integer, default=0)
    total_likes: Mapped[int] = mapped_column(Integer, default=0)
    total_comments: Mapped[int] = mapped_column(Integer, default=0)
    total_shares: Mapped[int] = mapped_column(Integer, default=0)
    
    # Engagement
    engagement_rate: Mapped[float] = mapped_column(Float, default=0.0)
    reach: Mapped[int] = mapped_column(Integer, default=0)
    
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Analytics {self.platform} - {self.date.date()}>"


class Account(Base):
    """Social media account configuration."""
    __tablename__ = "accounts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    platform: Mapped[str] = mapped_column(String(50))
    account_name: Mapped[str] = mapped_column(String(100))
    
    # Credentials (encrypted in production!)
    api_key: Mapped[Optional[str]] = mapped_column(Text)
    api_secret: Mapped[Optional[str]] = mapped_column(Text)
    access_token: Mapped[Optional[str]] = mapped_column(Text)
    
    # Settings
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    max_posts_per_day: Mapped[int] = mapped_column(Integer, default=3)
    niche: Mapped[str] = mapped_column(String(50), default="general")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Account {self.platform} - {self.account_name}>"


# Database connection helper
async def get_engine(database_url: str = "sqlite+aiosqlite:///social_growth.db"):
    """Create async database engine."""
    engine = create_async_engine(database_url, echo=False)
    return engine


async def create_tables(engine):
    """Create all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    """Get database session."""
    engine = await get_engine()
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        return session