import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

ORG_URL = os.getenv("AZURE_ORG_URL")   # Example: https://dev.azure.com/yourorg/
PROJECT = os.getenv("AZURE_PROJECT")   # Example: MyProject
PAT = os.getenv("AZURE_PAT")           # Your PAT token


def _get_auth_header():
    token = f":{PAT}"
    encoded_token = base64.b64encode(token.encode("utf-8")).decode("utf-8")
    return {"Authorization": f"Basic {encoded_token}"}


def run_wiql(query: str):
    """
    Runs WIQL query and returns list of work item IDs.
    """
    url = f"{ORG_URL}{PROJECT}/_apis/wit/wiql?api-version=7.0"

    headers = _get_auth_header()
    headers["Content-Type"] = "application/json"

    payload = {"query": query}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"WIQL query failed {response.status_code}: {response.text}")

    data = response.json()
    work_items = data.get("workItems", [])

    return [item["id"] for item in work_items]


def get_work_item(work_item_id: int):
    """
    Fetch complete work item JSON.
    """
    url = f"{ORG_URL}{PROJECT}/_apis/wit/workitems/{work_item_id}?api-version=7.0"

    headers = _get_auth_header()
    headers["Content-Type"] = "application/json"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch work item {work_item_id}. {response.status_code}: {response.text}")

    return response.json()
