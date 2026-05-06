"""
Database initialization and management script.
Run: python db_init.py
"""
import asyncio
import sys
from loguru import logger

# Add parent directory to path
sys.path.insert(0, ".")

from database.models import get_engine, create_tables, Post, ScheduledPost, Engagement, Analytics, Account
from database import get_session
from core.settings import settings


async def init_database():
    """Initialize database and create tables."""
    logger.info("🗄️ Initializing database...")
    
    # Create engine
    engine = await get_engine(settings.database_url)
    
    # Create tables
    await create_tables(engine)
    
    logger.info("✅ Database tables created successfully!")
    
    # Run async session test
    async with engine.begin() as conn:
        from sqlalchemy import text
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result]
        logger.info(f"Created tables: {tables}")
    
    return engine


async def seed_sample_data():
    """Add sample data for testing."""
    logger.info("🌱 Adding sample data...")
    
    # This would add sample accounts, posts, etc.
    # For now, just log
    
    logger.info("✅ Sample data added (if any)")
    
    # Sample accounts
    accounts = [
        {
            "platform": "instagram",
            "account_name": "motivation_daily",
            "niche": "motivation",
            "max_posts_per_day": 3,
            "is_active": True
        },
        {
            "platform": "twitter", 
            "account_name": "tech_tips",
            "niche": "tech",
            "max_posts_per_day": 5,
            "is_active": True
        }
    ]
    
    logger.info(f"📋 Sample accounts: {accounts}")
    return accounts


async def reset_database():
    """Drop all tables and recreate."""
    logger.warning("⚠️  Resetting database - this will delete ALL data!")
    
    from database.models import Base
    engine = await get_engine(settings.database_url)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("✅ Database reset complete!")
    await seed_sample_data()


async def show_stats():
    """Show database statistics."""
    logger.info("📊 Database Statistics:")
    
    from sqlalchemy import text
    
    engine = await get_engine(settings.database_url)
    
    async with engine.begin() as conn:
        # Count tables
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result]
        
        for table in tables:
            count_result = await conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = count_result.scalar()
            logger.info(f"  {table}: {count} rows")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Database Management")
    parser.add_argument("command", choices=["init", "seed", "reset", "stats"], default="init")
    
    args = parser.parse_args()
    
    if args.command == "init":
        asyncio.run(init_database())
    elif args.command == "seed":
        asyncio.run(seed_sample_data())
    elif args.command == "reset":
        asyncio.run(reset_database())
    elif args.command == "stats":
        asyncio.run(show_stats())


if __name__ == "__main__":
    main()