import os

from simple_rest_client.exceptions import ClientError

from vgscli.auth_server import AuthServer
from vgscli.errors import AuthenticationError, AuthenticationRequiredError, TokenNotValidError, \
    AutoAuthenticationError
from vgscli.keyring_token_util import KeyringTokenUtil

token_util = KeyringTokenUtil()
TOKEN_FILE_NAME = 'vgs_token'


def handshake(ctx, environment):
    try:
        auth_server = AuthServer(environment)
        token_util.validate_refresh_token()
        if not token_util.validate_access_token():
            auth_server.refresh_authentication()
    except TokenNotValidError:
        raise AuthenticationRequiredError(ctx)
    except Exception as e:
        raise AuthenticationError(ctx, e.args[0])


def login(ctx, environment):
    try:
        auth_server = AuthServer(environment)
        return auth_server.login(environment)
    except Exception as e:
        raise AuthenticationError(ctx, e.args[0])


def logout(ctx, environment):
    try:
        auth_server = AuthServer(environment)
        auth_server.logout()
        token_util.clear_tokens()
        token_util.remove_encryption_secret()
    except Exception as e:
        raise AuthenticationError(ctx, e.args[0])


def auto_login(ctx, environment):
    client_id = os.environ.get('VGS_CLIENT_ID')
    secret = os.environ.get('VGS_CLIENT_SECRET')

    if not all([client_id, secret]):
        return False

    auth_server = AuthServer(environment)

    try:
        handshake(ctx, environment)
    except AuthenticationRequiredError:
        __auto_login(ctx, auth_server, client_id, secret)

    return True


def __auto_login(ctx, auth_server, client_id, secret):
    try:
        auth_server.auto_login(client_id, secret)
    except ClientError:
        raise AutoAuthenticationError(ctx)
