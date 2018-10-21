"""
Main module
"""

from .app import APP, DB, BCRYPT, MANAGER, JWT_MANAGER
from app.api import API

import app.commands
