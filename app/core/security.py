import re

# =========================================================
# VALIDATE QUERY
# =========================================================

def validate_query(query: str):

    blocked_patterns = [

        r"hack",

        r"fake otp",

        r"steal money",

        r"bypass bank",

        r"ignore previous instructions",

        r"reveal system prompt",

        r"show.*api key",

        r"password",

        r"credential"
    ]

    query = query.lower()

    for pattern in blocked_patterns:

        if re.search(pattern, query):

            return False

    return True

# =========================================================
# MASK SENSITIVE DATA
# =========================================================

def mask_sensitive_data(text: str):

    text = re.sub(

        r"\b[A-Z]{4}0[A-Z0-9]{6}\b",

        "[IFSC]",

        text,

        flags=re.IGNORECASE
    )

    text = re.sub(

        r"\b[A-Z]{5}\d{4}[A-Z]\b",

        "[PAN]",

        text,

        flags=re.IGNORECASE
    )

    text = re.sub(

        r"\b\d{6}\b",

        "[OTP]",

        text
    )

    text = re.sub(

        r"\b(?:\d[ -]*?){13,16}\b",

        "[CARD_NUMBER]",

        text
    )

    text = re.sub(

        r"\b\d{11,18}\b",

        "[ACCOUNT_NUMBER]",

        text
    )

    text = re.sub(

        r"\b[6-9]\d{9}\b",

        "[PHONE]",

        text
    )

    text = re.sub(

        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",

        "[EMAIL]",

        text,

        flags=re.IGNORECASE
    )

    return text


def contains_pii(text: str):

    masked_text = mask_sensitive_data(
        text
    )

    return masked_text != text
