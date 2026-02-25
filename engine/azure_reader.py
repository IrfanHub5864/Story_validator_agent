from engine.tfs_client import get_work_item


def fetch_work_item(work_item_id):
    """
    Returns title + description of work item.
    """
    data = get_work_item(work_item_id)

    title = data["fields"].get("System.Title", "")
    description = data["fields"].get("System.Description", "")

    return title, description
