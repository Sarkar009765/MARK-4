# Social Growth AI

[](#social-growth-ai)

> Autonomous AI Agent for Social Media Growth - Runs from `python main.py`, creates content, engages audience, and analyzes performance automatically.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/Sarkar009765/MARK-4?style=social)](https://github.com/Sarkar009765/MARK-4/stargazers)

---

## What Is It?

[](#what-is-it)

**Social Growth AI** is a multi-agent system that automates your social media presence. It combines 5 specialized AI agents that work together to:
- 📝 Generate viral content (captions, hashtags, image prompts)
- 💪 Auto-engage with your audience (likes, comments, follows)
- 💬 Reply to comments/DMs with AI-powered responses
- 📊 Track performance and self-optimize
- 📅 Schedule posts for optimal times

Built with **OpenAgents architecture** + **Hermes-style function calling** + **Paperclip simplicity**.

---

## Key Features

[](#key-features)

- 🤖 **5 AI Agents** - Strategy, Content, Growth, Reply, Analytics
- 📱 **Multi-Platform** - Instagram, Facebook, Twitter/X
- 🎯 **Auto Content** - AI generates captions, hashtags, image prompts  
- 💪 **Smart Engagement** - Auto-like, comment, follow, DM
- 💬 **AI Replies** - Context-aware comment/DM responses
- 📊 **Analytics** - Performance tracking & self-optimization
- 📅 **Scheduler** - Automated posting schedule
- 🌐 **Web Dashboard** - Streamlit-based UI
- 🔌 **REST API** - FastAPI endpoints
- 🐳 **Docker** - Ready to deploy

---

## Installation

[](#installation)

```bash
# Clone the project
git clone https://github.com/Sarkar009765/MARK-4.git
cd MARK-4

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Add your API keys (optional for testing)
# OPENAI_API_KEY=your_key_here
```

---

## Quick Start

[](#quick-start)

### Test Without API Key (Mock Mode)
```bash
# Check system status
python main.py status

# Run full AI cycle
python main.py full
```

### Run with Real AI
```bash
# Add your OpenAI key in .env
OPENAI_API_KEY=sk-...

# Run content generation
python main.py content --niche fitness
```

### Web Dashboard
```bash
streamlit run dashboard.py
```
Then open: http://localhost:8501

### REST API
```bash
uvicorn server:app --reload
```
Then open: http://localhost:8000/docs

---

## Architecture

[](#architecture)

```
┌─────────────────────────────────────────────┐
│           ORCHESTRATOR (Main Brain)        │
│     (Coordinates all agents)                │
└──────┬──────────┬──────────┬───────────┬────┘
       │          │          │           │
   ┌───▼───┐  ┌───▼───┐  ┌──▼────┐  ┌──▼────┐
   │Strategy│  │Content│  │Growth │  │Analytics│
   │ Agent │  │ Agent │  │ Agent │  │ Agent  │
   └───┬───┘  └───┬───┘  └──┬─────┘  └──┬─────┘
       │          │         │          │
   ┌───▼────────────────────────▼────────┐
   │         PLATFORM HANDLERS            │
   │   Instagram │ Facebook │ Twitter    │
   └──────────────────────────────────────┘
```

---

## Configuration

[](#configuration)

Edit `.env` file:

```env
# AI Provider (openai, anthropic, ollama)
AI_PROVIDER=openai
OPENAI_API_KEY=your_key_here

# Database
DATABASE_URL=sqlite:///social_growth.db

# Default Niche
DEFAULT_NICHE=motivation

# Safety Limits
MAX_POSTS_PER_DAY=3
SAFETY_MODE=strict
```

---

## Connect Real APIs

[](#connect-real-apis)

### Instagram
```env
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

### Facebook
```env
FACEBOOK_ACCESS_TOKEN=your_token
FACEBOOK_PAGE_ID=your_page_id
```

### Twitter
```env
TWITTER_API_KEY=xxx
TWITTER_API_SECRET=xxx
```

---

## Demo Results

[](#demo-results)

```
✅ strategy: success - Trends found: 2, Themes: 3
✅ content: success - Posts created: 3  
✅ growth: success - Engagement: 3
✅ reply: success - Processed: 3
✅ analytics: success - Engagement rate: 5.2%
```

---

## Docker

[](#docker)

```bash
# Edit .env with your keys first
cp .env.example .env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

---

## How It Works

[](#how-it-works)

1. **Strategy Agent** - Analyzes trends, competitors, plans content themes
2. **Content Agent** - Generates captions, hashtags, image prompts
3. **Growth Agent** - Auto-engages: likes, comments, follows, DMs
4. **Reply Agent** - AI-powered responses to comments/DMs
5. **Analytics Agent** - Tracks performance, suggests optimizations

---

## Project Structure

[](#project-structure)

```
MARK-4/
├── main.py              # CLI entry point
├── server.py            # FastAPI REST API
├── dashboard.py         # Streamlit Web UI
├── db_init.py           # Database setup
├── requirements.txt     # Dependencies
├── Dockerfile           # Docker container
├── docker-compose.yml   # Multi-container setup
│
├── agents/              # 5 AI Agents
│   ├── orchestrator.py # Central brain
│   ├── strategy_agent.py
│   ├── content_agent.py
│   ├── growth_agent.py
│   ├── reply_agent.py
│   └── analytics_agent.py
│
├── platforms/           # Platform integrations
│   ├── instagram.py
│   ├── instagram_api.py
│   ├── facebook.py
│   └── twitter.py
│
├── core/
│   ├── settings.py
│   └── scheduler.py
│
├── database/
│   └── models.py
│
└── config/
    ├── accounts.yaml
    └── prompts/
```

---

## Contributing

[](#contributing)

See [CONTRIBUTING.md](CONTRIBUTING.md). Pull requests welcome!

---

## License

[](#license)

[MIT License](LICENSE)

---

## Thanks

[](#thanks)

- **Kimi k2.6** - AI model powering this project
- **OpenAgents** - Architecture inspiration
- **Moonshot AI** - AI provider

---

## Star History

[](#star-history)

[![Star History Chart](https://api.star-history.com/svg?repos=Sarkar009765/MARK-4&type=date)](https://star-history.com/#Sarkar009765/MARK-4)

---

**For questions/issues:** https://github.com/Sarkar009765/MARK-4/issues