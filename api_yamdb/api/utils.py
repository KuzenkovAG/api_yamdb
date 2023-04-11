from django.contrib.auth.tokens import PasswordResetTokenGenerator

account_activation_token = PasswordResetTokenGenerator()


def get_confirmation_code(user) -> str:
    """Get confirmation code for User"""
    return account_activation_token.make_token(user)


def check_confirmation_code(user, token) -> bool:
    """Check valid of confirmation code."""
    return account_activation_token.check_token(user, token)


def send_email_with_confirmation_code(user):
    """Send message on User email with confirmation code."""
    token = get_confirmation_code(user)
    print('Email was sent.')
    print(token)
