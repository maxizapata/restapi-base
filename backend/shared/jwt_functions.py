from rest_framework_simplejwt.tokens import (
    AccessToken,
    RefreshToken)

def get_jwt_token(user):
    access = AccessToken.for_user(user)
    refresh = RefreshToken.for_user(user)
    return {'access': access, 'refresh': refresh}