from rest_framework import serializers


class UsernameValidationMixin:
    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Username should be not equal "me"'
            )
        return value
