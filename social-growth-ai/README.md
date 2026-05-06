# 🚀 Social Growth AI

**Autonomous AI Agent for Social Media Growth**

An intelligent multi-agent system that automates social media content creation, posting, engagement, and analytics. Inspired by OpenAgents architecture with Hermes-style function calling and Paperclip simplicity.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **5 AI Agents** | Strategy, Content, Growth, Reply, Analytics - working together |
| 📱 **Multi-Platform** | Instagram, Facebook, Twitter/X support |
| 📝 **Auto Content** | AI-generated captions, hashtags, image prompts |
| 💪 **Smart Engagement** | Auto-like, comment, follow, DM |
| 💬 **AI Replies** | Context-aware comment/DM responses |
| 📊 **Analytics** | Performance tracking & self-optimization |
| 📅 **Scheduler** | Automated posting schedule |
| 🌐 **Web Dashboard** | Streamlit-based UI |
| 🔌 **REST API** | FastAPI endpoints |
| 🐳 **Docker** | Ready to deploy |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│           ORCHESTRATOR (Main Brain)         │
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

## 🚀 Quick Start

### 1. Clone the Project
```bash
git clone https://github.com/Sarkar009765/MARK-4.git
cd MARK-4
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy example env file
cp .env.example .env

# Add your API keys in .env:
OPENAI_API_KEY=your_openai_key_here
```

### 4. Run Tests (Mock Mode - No API Key Needed!)
```bash
# Check system status
python main.py status

# Run full AI cycle
python main.py full
```

---

## 📖 Usage Examples

### CLI Commands

```bash
# Full cycle - run all agents
python main.py full

# Content only - create posts
python main.py content --niche fitness

# Engagement only - grow audience
python main.py engage

# Quick post - emergency content
python main.py quick --prompt "motivation"

# Schedule posts
python main.py schedule --times 08:00 19:00

# Check status
python main.py status

# Test platform connection
python main.py test instagram
```

### Web Dashboard
```bash
streamlit run dashboard.py
```
Then open: http://localhost:8501

### REST API Server
```bash
uvicorn server:app --reload
```
Then open: http://localhost:8000/docs

---

## 🛠️ Configuration

Edit `.env` file:

```env
# AI Provider (openai, anthropic, ollama)
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...

# Database
DATABASE_URL=sqlite:///social_growth.db

# Default Niche
DEFAULT_NICHE=motivation

# Safety Limits
MAX_POSTS_PER_DAY=3
SAFETY_MODE=strict
```

---

## 📁 Project Structure

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
│   ├── instagram.py    # Simulated handler
│   ├── instagram_api.py # Real API
│   ├── facebook.py     # Facebook Graph API
│   └── twitter.py      # Twitter API v2
│
├── core/
│   ├── settings.py     # Config management
│   └── scheduler.py   # Post scheduler
│
├── database/
│   └── models.py       # SQLAlchemy models
│
└── config/
    ├── accounts.yaml   # Account configs
    └── prompts/        # AI prompt templates
```

---

## 🔧 Connect Real APIs

### Instagram
1. Add credentials in `.env`:
```env
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

### Facebook
1. Create Facebook Developer Account
2. Create App → Get Page Access Token
3. Add in `.env`:
```env
FACEBOOK_ACCESS_TOKEN=your_token
FACEBOOK_PAGE_ID=your_page_id
```

### Twitter
1. Apply for Twitter Developer Account
2. Create App in Developer Portal
3. Add in `.env`:
```env
TWITTER_API_KEY=xxx
TWITTER_API_SECRET=xxx
```

---

## 🐳 Run with Docker

```bash
# Edit .env with your keys first
cp .env.example .env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

---

## 🤖 How the AI Agents Work

1. **Strategy Agent** - Analyzes trends, competitors, plans content themes
2. **Content Agent** - Generates captions, hashtags, image prompts
3. **Growth Agent** - Auto-engages: likes, comments, follows, DMs
4. **Reply Agent** - AI-powered responses to comments/DMs
5. **Analytics Agent** - Tracks performance, suggests optimizations

---

## 📊 Demo Results

```
✅ strategy: success - Trends found: 2, Themes: 3
✅ content: success - Posts created: 3  
✅ growth: success - Engagement: 3
✅ reply: success - Processed: 3
✅ analytics: success - Engagement rate: 5.2%
```

---

## ⚠️ Important Notes

- **Mock Mode**: System works without API keys (uses simulated responses)
- **Real AI**: Add OpenAI/Anthropic key for real AI generation
- **Rate Limits**: Built-in safety limits to prevent account restrictions
- **Ethical**: Designed for legitimate growth, not spam

---

## 📝 License

MIT License

---

## 👨‍💻 Created By

**Sarkar009765** - Using Kimi k2.6 (Moonshot AI)

---

## 🌟 Star this Project!

If you find this useful, please give it a ⭐!

---

**For questions/issues:** https://github.com/Sarkar009765/MARK-4/issues