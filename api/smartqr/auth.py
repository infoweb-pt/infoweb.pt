from .utils import check_manage_token


def authorize_manage(request, code):
    user = getattr(request, 'user', None)
    if user and user.is_authenticated and code.owner_user_id == user.id:
        return True

    token = request.headers.get('X-Manage-Token', '') or request.META.get('HTTP_X_MANAGE_TOKEN', '')
    if token and check_manage_token(token, code.manage_token_hash):
        return True

    return False
