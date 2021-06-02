from typing import Tuple, Optional

from django.conf import settings
from django.contrib.auth import get_user_model
import jwt
from rest_framework.authentication import get_authorization_header

User = get_user_model()


def _sync_groups(user, claims):
    if "groups" not in claims:
        return
    current_groups = set(group.name for group in user.groups.all())
    new_groups = set(claims["groups"])
    user_should_be_staff = "staff" in new_groups
    if user.is_staff != user_should_be_staff:
        user.is_staff = user_should_be_staff
        user.save()
    if user.is_superuser != user_should_be_staff:
        user.is_superuser = True
        user.save()
    if current_groups != new_groups:
        user.groups.clear()
        for group_name in new_groups:
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
        user.save()


def _get_or_create_user(claims: dict) -> User:
    try:
        return User.objects.get_by_natural_key(claims["sub"])
    except User.DoesNotExist:
        user = User(username=claims["sub"])
        user.save()
        return user


def _decode_jwt(token):
    """Try to decode the given token with all JWT_PUBLIC_KEYS from the settings."""
    for public_key in settings.JWT_PUBLIC_KEYS[:-1]:
        try:
            return jwt.decode(token, public_key, algorithms=["ES256"])
        except jwt.InvalidTokenError:
            pass  # Just try the next public key.
    return jwt.decode(token, settings.JWT_PUBLIC_KEYS[-1], algorithms=["ES256"])


def _authenticate(request) -> Optional[Tuple[User, dict]]:
    """Can raise jwt.InvalidTokenError."""
    prefix_and_token = get_authorization_header(request).split()
    try:
        auth_type, token = prefix_and_token
    except (TypeError, ValueError):
        return None
    if auth_type != b"Bearer":
        return None
    claims = _decode_jwt(token)
    user = _get_or_create_user(claims)
    _sync_groups(user, claims)
    return user, {**claims, "token": token}


class DRFAuthentication:
    def authenticate(self, request):
        try:
            return _authenticate(request)
        except jwt.InvalidTokenError as err:
            raise exceptions.AuthenticationFailed(str(err))
