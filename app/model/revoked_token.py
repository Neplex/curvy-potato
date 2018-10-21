"""
Revoked tokens
"""

from datetime import datetime

from .. import DB


class RevokedToken(DB.Model):
    """Store revoked tokens."""

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    jti = DB.Column(DB.String(120), unique=True, nullable=False)
    revoked_on = DB.Column(DB.DateTime, nullable=False, default=datetime.now)
