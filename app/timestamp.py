"""
This file only reates the timestamp for artefacts
"""

from datetime import datetime

def timestamp_current_today():
    """current time stamp according to the ISO format"""
    return datetime.now().isoformat()
