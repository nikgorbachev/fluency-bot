# 🌍 Language Penpal Bot
 
A Telegram bot that pairs you with a fictional local persona to practice a foreign language — no tutor fees, no scheduling, no awkward small talk. Just a conversation.
 
---
 
## What it does
 
Pick a language, and the bot conjures a penpal: a made-up person with a name, a character, and a city that fits the culture. They introduce themselves, share a little about their life, and ask you questions. You write back — in the target language or in English — and they respond naturally, correcting your mistakes along the way.
 
It feels more like texting a friend than drilling flashcards.
 
**Supported interaction modes:**
 
| Mode | When it triggers |
|---|---|
| `presentation` | First message — the persona introduces itself |
| `interaction` | Every reply — correction + natural conversation |
| `exit` | You say bye — the persona wraps up gracefully |
 
---
 
## Getting started
 
### 1. Clone and install
 
```bash
git clone https://github.com/your-username/language-penpal-bot
cd language-penpal-bot
pip install -r requirements.txt
```
 
### 2. Set environment variables
 
```bash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openrouter_api_key   # OpenRouter uses this header name
```
 
### 3. Run
 
```bash
python bot.py
```
 
---
 
## How to use it
 
1. Open the bot on Telegram and send `/start`
2. Type the language you want to practice (e.g. `French`, `Italian`, `Japanese`)
3. Your penpal introduces themselves — reply in the target language or English
4. To end the session, say something like `bye`, `ciao`, or `see you`
The bot also nudges you if you've gone quiet for a few hours, so it doesn't feel like a tool you opened and forgot.
 
---
 
## Stack
 
- **[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)** — async Telegram polling
- **[OpenRouter](https://openrouter.ai)** (`openrouter/free`) — LLM routing, free tier
- **[httpx](https://www.python-httpx.org/)** — async HTTP client
- **Railway** — deployment
---
 
## Project structure
 
```
├── bot.py          # Telegram handlers and job queue
├── llm_client.py   # Session management and OpenRouter calls
└── requirements.txt
```
 
---
 
## Limitations
 
This is a proof of concept. A few things to keep in mind:
 
- Sessions are **in-memory only** — restarting the bot clears all conversations
- The free OpenRouter tier has rate limits and occasional model changes
- No persistent user profiles or progress tracking (yet)
---
 
## Why this exists
 
Language tutors are expensive. Language apps feel like chores and are often very abstract. This is an experiment in a middle path: a low-commitment, low-cost conversation partner that adapts to you, and keeps the target cultural context
