from datetime import datetime


def get_nice_timestamp_format(ts=None) -> str:
    """
    Returns a YYYY-MM-DD_hours:minutes:secondes Timestamp
    """
    if not ts:
        ts = datetime.now()
    return ts.strftime("%Y-%m-%d_%H:%M:%S")
