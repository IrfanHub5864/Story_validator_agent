from engine.tfs_client import run_wiql


def fetch_user_stories_today():
    query = """
    SELECT [System.Id]
    FROM WorkItems
    WHERE
        [System.TeamProject] = @project
        AND [System.WorkItemType] = 'Issue'
        AND [System.CreatedDate] >= @Today
    ORDER BY [System.CreatedDate] DESC
    """
    return run_wiql(query)


def fetch_user_stories_yesterday():
    query = """
    SELECT [System.Id]
    FROM WorkItems
    WHERE
        [System.TeamProject] = @project
        AND [System.WorkItemType] = 'Issue'
        AND [System.CreatedDate] >= @Today - 1
        AND [System.CreatedDate] < @Today
    ORDER BY [System.CreatedDate] DESC
    """
    return run_wiql(query)


def fetch_user_stories_custom(date_str):
    """
    date_str format: YYYY-MM-DD
    """
    query = f"""
    SELECT [System.Id]
    FROM WorkItems
    WHERE
        [System.TeamProject] = @project
        AND [System.WorkItemType] = 'Issue'
        AND [System.CreatedDate] >= '{date_str}T00:00:00Z'
        AND [System.CreatedDate] <= '{date_str}T23:59:59Z'
    ORDER BY [System.CreatedDate] DESC
    """
    return run_wiql(query)
