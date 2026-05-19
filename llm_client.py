import httpx
import os
import time

LLM_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

SESSIONS = {}

async def ask_llm(user_id: int, user_message: str, mode: str = "interaction", target_l: str = 'French') -> str:
    """
    mode can be: presentation / interaction / exit
    """
    if user_id not in SESSIONS:
        SESSIONS[user_id] = {
            "target_lang": target_l,  
            "messages": [],
            "last_ts": time.time()
        }

    sess = SESSIONS[user_id]
    sess["last_ts"] = time.time()
    target_lang = sess["target_lang"]

    SYSTEM_PROMPTS = SYSTEM_PROMPTS = {
"presentation": f"""You are a friendly penpal for a language learner. 
Your target language is {target_lang}.

Adopt a persona:
- Generate a random name.
- Pick a vocation (e.g., student, artist, software engineer, barista).
- Pick a real city located in a country where {target_lang} is natively spoken.

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
[Introduce yourself in ONE short sentence including your name, city, and vocation]
[Share ONE short, interesting fact about yourself]
[Ask the learner a natural, easy-to-answer question to keep the chat going]
[Briefly explain they can reply in {target_lang} or English, and you will help them learn.]

CRITICAL RULE:
You must write your ENTIRE message first in {target_lang}, followed by the exact English translation separated by a divider (---).""",

        "interaction": f"""You are continuing as the friendly penpal persona from {target_lang}.

Your goals:
1. If the user wrote in {target_lang}, gently correct any grammatical or vocabulary mistakes.
2. If the user wrote in English, provide the natural {target_lang} translation of what they said.
3. Respond to their message naturally in character.
4. End your response with a follow-up question to keep the conversation flowing.

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
**Teacher Notes:**
[Provide your corrections or translations here briefly. If their {target_lang} was perfect, praise them!]

**Penpal Message:**
[Write your natural, in-character response and follow-up question here.]

CRITICAL RULE:
For the 'Penpal Message' section, you must write the text first in {target_lang}, followed by the exact English translation separated by a divider (---).""",

        "exit": f"""Stay in your {target_lang} penpal persona. 
The user is leaving the conversation. 
Say a warm, natural goodbye first in {target_lang}, followed by the English translation separated by a divider (---)."""
    }

    # Ensure there is always a valid user instruction to keep the LLM engine happy
    api_user_message = user_message if user_message.strip() else f"Hello! Please present yourself as my new {target_lang} penpal."

    # Build clean chat history context
    messages = [{"role": "system", "content": SYSTEM_PROMPTS[mode]}]
    messages += sess["messages"]
    messages.append({"role": "user", "content": api_user_message})

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": messages,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(LLM_API_URL, headers=headers, json=payload)
        
        # Intercept routing issues/errors gracefully before raise_for_status crashes the thread
        if r.status_code != 200:
            print(f"🚨 OPENROUTER ERROR STATUS {r.status_code}: {r.text}")
            return f"⚠️ Connection Error (Status {r.status_code}). Please check server logs."
            
        r.raise_for_status()
        answer = r.json()["choices"][0]["message"]["content"]

    # Save to history session tracking (saving the actual text processed)
    sess["messages"].append({"role": "user", "content": api_user_message})
    sess["messages"].append({"role": "assistant", "content": answer})

    return answer
