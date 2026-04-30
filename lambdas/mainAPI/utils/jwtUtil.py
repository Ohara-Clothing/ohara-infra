import jwt


def _decode_token(token):
    return jwt.decode(token, options={"verify_signature": False})


def usernameFromIdToken(idToken):
    decoded_token = _decode_token(idToken)
    username = decoded_token.get("cognito:username")
    return username


def userIdFromIdToken(idToken):
    decoded_token = _decode_token(idToken)
    user_id = decoded_token.get("sub")
    return user_id


def emailFromIdToken(idToken):
    decoded_token = _decode_token(idToken)
    email = decoded_token.get("email")
    return email


def usernameFromAccessToken(accessToken):
    decoded_token = _decode_token(accessToken)
    username = decoded_token.get("username") or decoded_token.get("cognito:username")
    return username


def userIdFromAccessToken(accessToken):
    decoded_token = _decode_token(accessToken)
    user_id = decoded_token.get("sub")
    return user_id
