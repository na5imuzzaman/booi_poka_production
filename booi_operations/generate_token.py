import secrets, string


def generate(self, *args, **kwargs):
    alphabet = string.digits + string.ascii_uppercase
    token = ''.join(secrets.choice(alphabet) for i in range(6))
    return str(token)
