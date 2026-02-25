import re


def validate_user_story_rules(story_text: str):
    """
    Rule-based validator (soft rules).
    Returns:
        - rule_score (0-100)
        - issues list
        - summary dict
    """

    text = story_text.lower()

    issues = []
    score = 0

    # ----------------------------
    # RULE 1: Check User Story Format
    # ----------------------------
    has_as_a = bool(re.search(r"\bas an?\b|\bas a\b|\bbeing an?\b", text))
    has_i_want = bool(re.search(r"\bi want\b|\bi should\b|\bi need\b|\bi can\b", text))
    has_so_that = bool(re.search(r"\bso that\b|\bin order to\b|\bto ensure\b|\bto improve\b|\bbecause\b", text))

    if has_as_a:
        score += 10
    else:
        issues.append("Missing role/actor (e.g., 'As an Admin')")

    if has_i_want:
        score += 10
    else:
        issues.append("Missing intent/need statement (e.g., 'I want / I should / I need')")

    if has_so_that:
        score += 10
    else:
        issues.append("Business value missing (e.g., 'so that / in order to / because')")

    # ----------------------------
    # RULE 2: Acceptance Criteria Presence
    # ----------------------------
    has_acceptance = "acceptance criteria" in text or "acceptance" in text

    if has_acceptance:
        score += 15
    else:
        issues.append("Acceptance Criteria section missing")

    # ----------------------------
    # RULE 3: Behavior-based keywords
    # ----------------------------
    behavior_keywords = ["when", "then", "should", "must", "system", "validate", "error", "display", "reject"]
    behavior_found = sum(1 for k in behavior_keywords if k in text)

    if behavior_found >= 3:
        score += 15
    else:
        issues.append("Acceptance criteria not behavior-based (missing When/Then/Should style)")

    # ----------------------------
    # RULE 4: Validation Rules Presence
    # ----------------------------
    validation_keywords = ["required", "mandatory", "invalid", "format", "min", "max", "length", "email", "phone"]
    validation_found = sum(1 for k in validation_keywords if k in text)

    if validation_found >= 3:
        score += 15
    else:
        issues.append("Validation rules missing/weak (email format, phone format, required constraints)")

    # ----------------------------
    # RULE 5: Error Handling Presence
    # ----------------------------
    error_keywords = ["error", "warning", "message", "fail", "invalid", "not allowed"]
    error_found = sum(1 for k in error_keywords if k in text)

    if error_found >= 2:
        score += 10
    else:
        issues.append("Error handling scenarios not defined")

    # ----------------------------
    # RULE 6: Role Access / Security
    # ----------------------------
    access_keywords = ["role", "access", "permission", "only", "authorized", "admin"]
    access_found = sum(1 for k in access_keywords if k in text)

    if access_found >= 2:
        score += 10
    else:
        issues.append("Role access/security requirements missing")

    # ----------------------------
    # RULE 7: Non-Functional Requirements
    # ----------------------------
    nfr_keywords = ["performance", "response time", "audit", "logging", "security", "encryption", "sla", "availability"]
    nfr_found = sum(1 for k in nfr_keywords if k in text)

    if nfr_found >= 1:
        score += 10
    else:
        issues.append("Non-functional requirements missing")

    # ----------------------------
    # Summary
    # ----------------------------
    summary = {
        "has_as_a": has_as_a,
        "has_i_want": has_i_want,
        "has_so_that": has_so_that,
        "has_acceptance": has_acceptance,
        "behavior_keywords_found": behavior_found,
        "validation_keywords_found": validation_found,
        "error_keywords_found": error_found,
        "access_keywords_found": access_found,
        "nfr_keywords_found": nfr_found,
    }

    return score, issues, summary
