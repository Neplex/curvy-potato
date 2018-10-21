"""
Authentication service
"""

from .. import DB
from ..model.user_app import UserApp
from ..model.revoked_token import RevokedToken


def generate_api_key():
    """Generate a new api key"""
    import uuid
    return str(uuid.uuid4())


def save_app(app):
    """Save app to the data base"""
    DB.session.add(app)
    DB.session.commit()


def get_user_app(name, key):
    """Get application from credentials"""
    user_app = UserApp.query.filter_by(app_name=name).first()

    if user_app is not None and user_app.check_app_key(key):
        return user_app

    return None


def revoke_jti(jti):
    """Revoke the given jti"""
    revoked_token = RevokedToken(jti=jti)
    DB.session.add(revoked_token)
    DB.session.commit()


def jti_is_revoked(jti):
    """Check if jti is revoked or not"""
    return RevokedToken.query.filter_by(jti=jti).first() is not None
