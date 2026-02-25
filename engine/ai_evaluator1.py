import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Create Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def evaluate_story(story_text, prompt_text):
    """
    Sends user story + prompt to Groq LLM and returns validation report.
    """

    full_prompt = f"""
{prompt_text}

--------------------------------------
USER STORY:
--------------------------------------
{story_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # best stable model currently
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()
