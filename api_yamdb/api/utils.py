from django.contrib.auth.tokens import PasswordResetTokenGenerator

account_activation_token = PasswordResetTokenGenerator()


def get_confirmation_code(user) -> str:
    return account_activation_token.make_token(user)


def check_confirmation_code(user, token) -> bool:
    return account_activation_token.check_token(user, token)


def send_email_with_confirmation_code(user):
    token = get_confirmation_code(user)
    print('Email was sent.')
    print(token)
