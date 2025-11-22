from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    """
    Return a dict with 'refresh' and 'access' tokens for a given user.
    Useful to return tokens after registration via API.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
