from datetime import UTC, datetime, timedelta, timezone

from langchain_core.tools import tool

@tool
def get_current_time() -> str:
    """
    Return the current UTC+8 date and time.
    Use this for simple time/date questions.
    """
    utc_plus_8 = timezone(timedelta(hours=8), name="UTC+08")
    now = datetime.now(UTC).astimezone(utc_plus_8)
    return now.strftime("Current UTC+8 time is %Y-%m-%d %H:%M:%S %Z%z")
