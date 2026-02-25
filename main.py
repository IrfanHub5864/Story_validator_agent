import os
import json
import hashlib
import re
from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel

from engine.azure_reader import fetch_work_item
from engine.azure_commenter import add_comment_to_work_item
from engine.ai_evaluator import evaluate_story


load_dotenv(override=True)

PROCESSED_FILE = "processed.json"


class PrivateNetworkHeaderMiddleware(BaseHTTPMiddleware):
    """Append the loopback header to every response output."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["Access-Control-Allow-Private-Network"] = "true"
        return response


app = FastAPI(title="User Story Validator API")

# ✅ CORS FIX - Allow Azure DevOps extension and loopback access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow Azure DevOps iframe
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(PrivateNetworkHeaderMiddleware)

PROMPT_TEXT = """
You are an Agile User Story Validator.

Your job is to evaluate the story ONLY based on the given rule report and Agile standards.

IMPORTANT:
- If the story is already strong, you MUST say "No major issues found".
- Do NOT invent random missing issues like security/logging unless they are truly required.
- If story contains validation rules, do not claim they are missing.

OUTPUT FORMAT (STRICT):

FINAL RESULT: PASS/FAIL
SCORE: <number>/100

ISSUES FOUND:
- If there are no real issues, write: None

RECOMMENDATIONS:
- If no improvements required, write: None

IMPROVED USER STORY:
- Only rewrite if FAIL or score < 80
- If PASS and score >= 90, return the same story with minimal improvements only (grammar/clarity),
  suggest improvements in recommendations but do not change the story if score is between 80 and 90
  or 90-95 suggest the recommendation it could be better if you add this in your user story.
  If the issue is some what big give in the issues but change the user story accordingly.

SCORING RULES:
- If story contains clear "As a / I want / So that" → +20(or grade accordingly if not perfectly clear)
- If acceptance criteria are in Given/When/Then → +20(or grade accordingly if not perfectly clear)
- If validations and error handling exist → +20(or grade accordingly if not perfectly clear)
- If business value is clear → +20(or grade accordingly if not perfectly clear)
- If security/access mentioned when relevant → +20(or grade accordingly if not perfectly clear)

Do NOT reduce score for missing security unless the story is related to authentication, login, or access control.
"""


class ReviewRequest(BaseModel):
    work_item_id: int
    story_text: str = None  # Make optional, will fetch if not provided
    force: bool = False


class ValidateRequest(BaseModel):
    workItemId: int
    storyText: str


def load_processed():
    try:
        with open(PROCESSED_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_processed(data):
    with open(PROCESSED_FILE, "w") as f:
        json.dump(data, f, indent=4)


def hash_story(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def get_story_text(title, description):
    story_text = ""
    if title:
        story_text += f"TITLE: {title}\n\n"
    if description:
        story_text += f"DESCRIPTION:\n{description}\n"
    return story_text.strip()


@app.post("/validate")
async def validate_story(request: ValidateRequest):
    """Endpoint for extension to call"""
    try:
        work_item_id = request.workItemId
        story_text = request.storyText
        
        print(f"🔍 Validating work item {work_item_id}")
        
        # Run AI evaluation
        result_text = evaluate_story(story_text, PROMPT_TEXT)
        
        # Add comment to Azure DevOps
        try:
            add_comment_to_work_item(work_item_id, result_text)
            print(f"✅ Comment added to work item {work_item_id}")
        except Exception as e:
            print(f"⚠️ Could not add comment: {e}")
        
        # Save to processed.json
        processed_data = load_processed()
        story_hash = hash_story(story_text)
        processed_data[str(work_item_id)] = story_hash
        save_processed(processed_data)
        
        return {
            "success": True,
            "validation": result_text
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@app.post("/review")
def review_story(payload: ReviewRequest):
    """Alternative endpoint for testing"""
    work_item_id = payload.work_item_id
    
    # Fetch work item if story_text not provided
    if not payload.story_text:
        title, description = fetch_work_item(work_item_id)
        story_text = get_story_text(title, description)
    else:
        story_text = payload.story_text
    
    # Run AI evaluation
    result_text = evaluate_story(story_text, PROMPT_TEXT)
    
    # Add comment
    add_comment_to_work_item(work_item_id, result_text)
    
    return {
        "status": "commented",
        "result": result_text
    }


@app.get("/")
def root():
    return {"message": "User Story Validator API is running on port 8000"}


@app.get("/test")
def test():
    return {"message": "API is working - ready for extension calls"}
