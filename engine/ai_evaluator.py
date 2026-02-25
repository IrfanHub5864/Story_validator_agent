import os
from groq import Groq
from dotenv import load_dotenv
from engine.rule_validator import validate_user_story_rules

load_dotenv(override=True)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def evaluate_story(story_text, prompt_text):

    # Rule-based validation
    rule_score, rule_issues, rule_summary = validate_user_story_rules(story_text)

    rule_report = f"""
--- RULE BASED VALIDATION REPORT ---
RULE SCORE: {rule_score}/100

RULE ISSUES FOUND:
{chr(10).join([f"- {i}" for i in rule_issues]) if rule_issues else "None"}

RULE SUMMARY:
{rule_summary}

-----------------------------------
"""

    # Combine rule report + prompt + story
    full_prompt = f"""
{prompt_text}

{rule_report}

USER STORY:
{story_text}

IMPORTANT:
- Use rule-based report as supporting evidence
- Final decision must be based on Agile industry standards
- Output in strict format
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0
    )

    return response.choices[0].message.content
