"""
Authentication service
"""

from app.app import DB
from app.model.revoked_token import RevokedToken
from app.model.user import User


def save_user(user):
    """Save user to the data base"""
    DB.session.add(user)
    DB.session.commit()


def remove_user(user):
    """Delete an user"""
    DB.session.delete(user)
    DB.session.commit()


def get_user(username, password):
    """Get user from credentials"""
    user = User.query.filter_by(username=username).first()

    if user is not None and user.check_password(password):
        return user

    return None


def revoke_jti(jti):
    """Revoke the given jti"""
    revoked_token = RevokedToken(jti=jti)
    DB.session.add(revoked_token)
    DB.session.commit()


def jti_is_revoked(jti):
    """Check if jti is revoked or not"""
    return RevokedToken.query.filter_by(jti=jti).first() is not None
