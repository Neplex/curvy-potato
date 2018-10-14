"""
Authentication service
"""

from .. import DB


def generate_api_key():
    """Generate a new api key"""
    import uuid
    return str(uuid.uuid4())


def add_app(app):
    """Add app to the data base"""
    # TODO: Save the app in the database.
    pass
