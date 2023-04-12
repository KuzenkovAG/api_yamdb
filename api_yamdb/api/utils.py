from django.contrib.auth.tokens import default_token_generator


def get_confirmation_code(user) -> str:
    """Get confirmation code for User"""
    return default_token_generator.make_token(user)


def check_confirmation_code(user, token) -> bool:
    """Check valid of confirmation code."""
    return default_token_generator.check_token(user, token)


def send_email_with_confirmation_code(user):
    """Send message on User email with confirmation code."""
    token = get_confirmation_code(user)
    print('Email was sent.')
    print(token)
