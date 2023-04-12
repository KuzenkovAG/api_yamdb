from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def get_confirmation_code(user) -> str:
    """Get confirmation code for User"""
    return default_token_generator.make_token(user)


def check_confirmation_code(user, token) -> bool:
    """Check valid of confirmation code."""
    return default_token_generator.check_token(user, token)


def send_email_with_confirmation_code(user):
    """Send message on User email with confirmation code."""
    token = get_confirmation_code(user)
    email_test = (
        f'Dear Mr.{user.username.title()},\n\n'
        f'Your API token: {token}.\n\n'
        'Best regards, Administration.'
    )
    send_mail(
        'Api token yamdb',
        email_test,
        'webmaster@localhost',
        [user.email],
        fail_silently=False,
    )
