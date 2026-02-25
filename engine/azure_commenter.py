import os
import base64
import html
import re
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

ORG_URL = os.getenv("AZURE_ORG_URL")
PROJECT = os.getenv("AZURE_PROJECT")
PAT = os.getenv("AZURE_PAT")


def get_auth_header():
    token = f":{PAT}"
    encoded_token = base64.b64encode(token.encode("utf-8")).decode("utf-8")
    return {
        "Authorization": f"Basic {encoded_token}",
        "Content-Type": "application/json-patch+json"
    }


def format_comment_html(comment_text):
    """
    Formats plain validator output into styled HTML for Azure DevOps comments.
    """
    heading_pattern = re.compile(r"^([A-Z][A-Z ]+):\s*(.*)$")
    lines = comment_text.splitlines()
    parts = []

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            parts.append("<div style='height:8px;'></div>")
            continue

        heading_match = heading_pattern.match(line)
        if heading_match:
            heading_text = html.escape(heading_match.group(1))
            heading_value = html.escape(heading_match.group(2))

            parts.append(
                "<div style='font-family: Segoe UI, Calibri, sans-serif; "
                "font-size: 14px; font-weight: 700; color: #145DA0; "
                "letter-spacing: 0.2px; margin: 10px 0 4px 0;'>"
                f"{heading_text}</div>"
            )

            if heading_value:
                parts.append(
                    "<div style='font-family: Segoe UI, Calibri, sans-serif; "
                    "font-size: 13px; color: #1F2937; margin: 0 0 8px 0;'>"
                    f"{heading_value}</div>"
                )
            continue

        if line.startswith("- "):
            bullet_text = html.escape(line[2:])
            parts.append(
                "<div style='font-family: Segoe UI, Calibri, sans-serif; "
                "font-size: 13px; color: #1F2937; margin: 0 0 6px 14px;'>"
                f"&#8226; {bullet_text}</div>"
            )
            continue

        parts.append(
            "<div style='font-family: Segoe UI, Calibri, sans-serif; "
            "font-size: 13px; color: #1F2937; margin: 0 0 6px 0;'>"
            f"{html.escape(line)}</div>"
        )

    return "".join(parts)


def add_comment_to_work_item(work_item_id, comment_text):
    """
    Adds comment into System.History field.
    Keeps formatting.
    """
    url = f"{ORG_URL}{PROJECT}/_apis/wit/workitems/{work_item_id}?api-version=7.1-preview.3"

    patch_data = [
        {
            "op": "add",
            "path": "/fields/System.History",
            "value": format_comment_html(comment_text)
        }
    ]

    response = requests.patch(url, headers=get_auth_header(), json=patch_data)

    if response.status_code not in [200, 201]:
        raise Exception(f"❌ Failed to add comment: {response.status_code} {response.text}")

    return True
