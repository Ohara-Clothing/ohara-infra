import jwt


def usernameFromIdToken(idToken):
    decoded_token = jwt.decode(idToken, options={"verify_signature": False})
    username = decoded_token.get("cognito:username")
    return username
