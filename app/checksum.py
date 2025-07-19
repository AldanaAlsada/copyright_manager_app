"""
this file is for checksum
"""

import hashlib

def create_checksum(data):
    """creates the checksum using sha256."""
    return hashlib.sha256(data).hexdigest()
