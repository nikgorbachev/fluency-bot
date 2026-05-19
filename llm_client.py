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

    SYSTEM_PROMPTS = {
        "presentation": f"""You are a penpal for a language learner.
Your target language is {target_lang}.
Your job:
1. Present yourself in ONE SHORT SENTENCE including a random name, vocation, and city matching the target language.
2. Share ONE short interesting fact about yourself.
3. Ask the learner a natural question.
4. Explain they can write in {target_lang} or English.
5. Write your full message in BOTH {target_lang} and English.""",
        "interaction": f"""You are continuing as the same penpal persona in {target_lang}.
- First: highlight and correct any mistakes if they wrote in {target_lang}.
- If they wrote in English, translate to {target_lang} and reply.
- Respond naturally and end with a follow-up question.
- Always write your full reply in BOTH {target_lang} and English.""",
        "exit": f"""Stay in persona as the penpal. The user is leaving. Say goodbye naturally in {target_lang} and English."""
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
