"""
Social Growth AI - Streamlit Dashboard
Run with: streamlit run dashboard.py
"""
import streamlit as st
import asyncio
import os
from datetime import datetime
from loguru import logger

# Page config
st.set_page_config(
    page_title="Social Growth AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 10px;
        padding: 10px 30px;
    }
    .success-box {
        background: rgba(0, 255, 0, 0.1);
        border: 1px solid #00ff00;
        border-radius: 10px;
        padding: 15px;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🚀 Social Growth AI")
st.markdown("### Autonomous Social Media Growth Agent")

# Sidebar
st.sidebar.title("⚙️ Configuration")

# Niche selector
niche = st.sidebar.selectbox(
    "Content Niche",
    ["motivation", "fitness", "tech", "business", "education", "entertainment"],
    index=0
)

# Platform selector
platforms = st.sidebar.multiselect(
    "Target Platforms",
    ["instagram", "facebook", "twitter"],
    default=["instagram"]
)

# Settings
st.sidebar.title("Settings")
auto_publish = st.sidebar.checkbox("Auto-publish (no approval)", value=False)
safety_mode = st.sidebar.select_slider("Safety Mode", ["strict", "medium", "relaxed"], value="strict")

# Main content
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>👥</h3>
        <h2>1,250</h2>
        <p>Followers</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>📝</h3>
        <h2>45</h2>
        <p>Total Posts</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(""""
    <div class="metric-card">
        <h3>💬</h3>
        <h2>312</h2>
        <p>Comments</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h3>📊</h3>
        <h2>5.2%</h2>
        <p>Engagement</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Action buttons
st.subheader("🎯 Actions")

action_col1, action_col2, action_col3, action_col4 = st.columns(4)

with action_col1:
    if st.button("🧠 Run Full Cycle", use_container_width=True):
        with st.spinner("Running AI agents..."):
            try:
                from agents.orchestrator import Orchestrator
                from core.settings import settings
                
                orchestrator = Orchestrator(niche=niche, platforms=platforms)
                result = asyncio.run(orchestrator.run_cycle(mode="full"))
                
                st.success("✅ Cycle completed!")
                st.json(result)
            except Exception as e:
                st.error(f"❌ Error: {e}")

with action_col2:
    if st.button("📝 Create Content", use_container_width=True):
        with st.spinner("Generating content..."):
            try:
                from agents.orchestrator import Orchestrator
                
                orchestrator = Orchestrator(niche=niche, platforms=platforms)
                result = asyncio.run(orchestrator.run_cycle(mode="content_only"))
                
                st.success("✅ Content created!")
                posts = result.get("content", {}).get("posts", [])
                
                for i, post in enumerate(posts):
                    with st.expander(f"Post {i+1}: {post.get('theme', 'Untitled')}"):
                        st.write(f"**Format:** {post.get('format')}")
                        st.write(f"**Tone:** {post.get('tone')}")
                        st.write("---")
                        st.write("**Caption:**")
                        st.write(post.get('caption', '')[:500])
                        st.write("---")
                        st.write("**Hashtags:**")
                        st.write(' '.join(post.get('hashtags', [])[:10]))
                        
                        if st.button(f"Approve & Publish #{i+1}", key=f"publish_{i}"):
                            st.info("Publishing would happen here!")
            except Exception as e:
                st.error(f"❌ Error: {e}")

with action_col3:
    if st.button("💪 Run Engagement", use_container_width=True):
        with st.spinner("Engaging with audience..."):
            try:
                from agents.orchestrator import Orchestrator
                
                orchestrator = Orchestrator(niche=niche, platforms=platforms)
                result = asyncio.run(orchestrator.run_cycle(mode="engage_only"))
                
                st.success("✅ Engagement complete!")
                st.json(result)
            except Exception as e:
                st.error(f"❌ Error: {e}")

with action_col4:
    if st.button("📊 Run Analytics", use_container_width=True):
        with st.spinner("Analyzing performance..."):
            try:
                from agents.orchestrator import Orchestrator
                
                orchestrator = Orchestrator(niche=niche, platforms=platforms)
                result = asyncio.run(orchestrator.run_cycle(mode="full"))
                
                st.success("✅ Analytics complete!")
                st.json(result.get("analytics", {}))
            except Exception as e:
                st.error(f"❌ Error: {e}")

st.markdown("---")

# Scheduled posts section
st.subheader("📅 Scheduled Posts")

col_left, col_right = st.columns(2)

with col_left:
    st.write("### Add New Schedule")
    schedule_time = st.time_input("Posting Time", datetime.now().replace(hour=12))
    schedule_platform = st.selectbox("Platform", platforms)
    
    if st.button("➕ Add to Schedule"):
        st.success(f"Added: {schedule_time} on {schedule_platform}")

with col_right:
    st.write("### Upcoming Posts")
    st.info("📅 08:00 - Instagram - Motivation post")
    st.info("📅 12:30 - Instagram - Educational content")
    st.info("📅 19:00 - Instagram - Evening motivation")

st.markdown("---")

# Quick post section
st.subheader("⚡ Quick Post")

quick_col1, quick_col2 = st.columns([3, 1])

with quick_col1:
    quick_caption = st.text_area("Caption", height=100, placeholder="Write your caption here...")

with quick_col2:
    quick_platform = st.selectbox("Platform", platforms)
    if st.button("🚀 Post Now"):
        if quick_caption:
            st.success("Post would be published here!")
        else:
            st.warning("Please write a caption")

# Footer
st.markdown("---")
st.caption("Social Growth AI v1.0 | Powered by Kimi k2.6 + OpenAgents Architecture")