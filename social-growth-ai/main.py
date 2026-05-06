"""
Main Entry Point - Social Growth AI
Run with: python main.py
"""
import asyncio
import sys
from datetime import datetime, timedelta
from loguru import logger

from core.settings import settings
from core.scheduler import scheduler
from agents.orchestrator import Orchestrator
from platforms.manager import PlatformManager


# Configure logging
logger.add(
    "logs/app.log",
    rotation="1 day",
    retention="7 days",
    level=settings.log_level
)
logger.add(sys.stderr, level=settings.log_level)


async def run_full_cycle():
    """Run one complete cycle of the system."""
    logger.info("=" * 50)
    logger.info("Starting Social Growth AI")
    logger.info("=" * 50)
    
    orchestrator = Orchestrator(
        niche=settings.default_niche,
        platforms=["instagram"]
    )
    
    logger.info("Running full cycle...")
    results = await orchestrator.run_cycle(mode="full")
    
    logger.info("=" * 50)
    logger.info("Cycle Results:")
    logger.info("=" * 50)
    
    for agent_name, result in results.items():
        if isinstance(result, dict):
            status = result.get("status", "unknown")
            logger.info(f"  {agent_name}: {status}")
            if status == "success":
                if agent_name == "strategy":
                    logger.info(f"    Trends found: {len(result.get('trends', []))}")
                    logger.info(f"    Themes: {len(result.get('content_themes', []))}")
                elif agent_name == "content":
                    logger.info(f"    Posts created: {len(result.get('posts', []))}")
                elif agent_name == "growth":
                    logger.info(f"    Engagement: {result.get('engagement_count', 0)}")
                elif agent_name == "reply":
                    logger.info(f"    Processed: {result.get('processed', 0)}")
                elif agent_name == "analytics":
                    logger.info(f"    Engagement rate: {result.get('metrics_summary', {}).get('engagement_rate', 0)}%")
    
    logger.info("=" * 50)
    logger.info("Cycle Complete!")
    logger.info("=" * 50)
    
    return results


async def run_content_only():
    """Run only content creation."""
    logger.info("Running content-only mode...")
    orchestrator = Orchestrator(niche=settings.default_niche)
    return await orchestrator.run_cycle(mode="content_only")


async def run_engage_only():
    """Run only engagement/growth activities."""
    logger.info("Running engage-only mode...")
    orchestrator = Orchestrator(niche=settings.default_niche)
    return await orchestrator.run_cycle(mode="engage_only")


async def quick_post(prompt: str):
    """Emergency: Create and post immediately."""
    logger.info(f"Quick post mode: {prompt}")
    orchestrator = Orchestrator(niche=settings.default_niche)
    return await orchestrator.run_cycle(mode="quick_post")


async def schedule_posts(times: list, niche: str, platforms: list):
    """Schedule posts at specific times."""
    logger.info(f"Scheduling daily posts at {times} for {niche}")
    
    orchestrator = Orchestrator(niche=niche, platforms=platforms)
    
    for time_str in times:
        content_result = await orchestrator.run_cycle(mode="content_only")
        posts = content_result.get("content", {}).get("posts", [])
        
        for post in posts:
            scheduler.schedule_daily(
                content=post,
                time=time_str,
                platforms=platforms
            )
    
    logger.info(f"Scheduled {len(posts) * len(times)} posts")
    return {"status": "scheduled", "count": len(posts) * len(times)}


def show_status():
    """Show system status."""
    logger.info("=" * 40)
    logger.info("Social Growth AI - Status")
    logger.info("=" * 40)
    
    orchestrator = Orchestrator()
    status = orchestrator.get_system_status()
    
    print(f"\n[Status] Niche: {status['orchestrator']['niche']}")
    print(f"[Platforms] {', '.join(status['orchestrator']['platforms'])}")
    print(f"\n[Agents]:")
    for name, agent in status['agents'].items():
        safety = "OK" if agent['safety_ok'] else "WARNING"
        print(f"  - {name}: {agent['total_actions']} actions | Safety: {safety}")
    
    print(f"\n[Scheduler] {scheduler.get_status()}")
    print("=" * 40)


async def test_platform(platform: str):
    """Test platform connection."""
    logger.info(f"Testing {platform} connection...")
    
    manager = PlatformManager(platforms=[platform])
    handler = manager.get_handler(platform)
    
    if handler:
        auth_result = await handler.authenticate()
        if auth_result:
            metrics = await handler.get_metrics()
            logger.info(f"✅ {platform} connected successfully!")
            logger.info(f"   Metrics: {metrics}")
            return {"status": "connected", "metrics": metrics}
        else:
            logger.error(f"❌ {platform} authentication failed")
            return {"status": "failed", "message": "Authentication failed"}
    else:
        logger.error(f"❌ Platform {platform} not found")
        return {"status": "error", "message": "Platform not configured"}


def main():
    """Main entry point with CLI options."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Social Growth AI - Autonomous Social Media Growth Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py full                          Run full AI cycle
  python main.py content --niche fitness       Create content for fitness niche
  python main.py engage                        Run engagement/growth activities
  python main.py quick --prompt "motivation"   Quick post generation
  python main.py schedule --times 08:00 19:00  Schedule daily posts
  python main.py status                        Show system status
  python main.py test instagram                Test platform connection
  python main.py web                           Start web dashboard
        """
    )
    parser.add_argument(
        "mode",
        choices=["full", "content", "engage", "quick", "schedule", "status", "test", "web"],
        nargs="?",
        default="full",
        help="Run mode"
    )
    parser.add_argument(
        "--niche",
        type=str,
        default=settings.default_niche,
        help="Content niche/topic (default: motivation)"
    )
    parser.add_argument(
        "--platforms",
        type=str,
        nargs="+",
        default=["instagram"],
        help="Platforms to target (default: instagram)"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        help="Quick post prompt"
    )
    parser.add_argument(
        "--times",
        type=str,
        nargs="+",
        default=["08:00", "12:30", "19:00"],
        help="Schedule times (e.g., --times 08:00 19:00)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Web dashboard port"
    )
    
    args = parser.parse_args()
    
    # Execute based on mode
    if args.mode == "full":
        asyncio.run(run_full_cycle())
    
    elif args.mode == "content":
        asyncio.run(run_content_only())
    
    elif args.mode == "engage":
        asyncio.run(run_engage_only())
    
    elif args.mode == "quick":
        if not args.prompt:
            logger.error("--prompt required for quick mode")
            sys.exit(1)
        asyncio.run(quick_post(args.prompt))
    
    elif args.mode == "schedule":
        asyncio.run(schedule_posts(args.times, args.niche, args.platforms))
        logger.info("\n✅ Posts scheduled! Run 'python main.py' to start scheduler.")
    
    elif args.mode == "status":
        show_status()
    
    elif args.mode == "test":
        asyncio.run(test_platform(args.platforms[0] if args.platforms else "instagram"))
    
    elif args.mode == "web":
        logger.info(f"Starting web dashboard on port {args.port}")
        run_web_dashboard(port=args.port)


def run_web_dashboard(port: int):
    """Run a simple web dashboard using Streamlit."""
    try:
        import streamlit as st
        
        st.set_page_config(page_title="Social Growth AI", page_icon="📈")
        st.title("📈 Social Growth AI Dashboard")
        
        st.write("### System Status")
        st.write("Click the button below to run a cycle:")
        
        if st.button("🚀 Run Full Cycle"):
            with st.spinner("Running AI agents..."):
                result = asyncio.run(run_full_cycle())
                st.success("Cycle completed!")
                st.json(result)
        
        st.write("---")
        st.write("### Agent Status")
        orchestrator = Orchestrator()
        status = orchestrator.get_system_status()
        
        for agent_name, agent_status in status["agents"].items():
            with st.expander(f"Agent: {agent_name}"):
                st.write(f"**Description:** {agent_status.get('description')}")
                st.write(f"**Total Actions:** {agent_status.get('total_actions')}")
                st.write(f"**Memory Size:** {agent_status.get('memory_size')}")
                st.write(f"**Safety OK:** {agent_status.get('safety_ok')}")
        
    except ImportError:
        logger.error("Streamlit not installed. Run: pip install streamlit")
        sys.exit(1)


if __name__ == "__main__":
    main()