import functools
from contextvars import ContextVar, copy_context
from credentials_generator import generate_credentials

dynamodb_session_keys = ContextVar("dynamodb_session_keys", default=None)


def dynamodb_tenant_isolation(func):
    @functools.wraps(func)
    def inner(event, context):
        ctx = copy_context()
        session_keys = generate_credentials(event)
        ctx.run(_set_dynamodb_session_keys, session_keys)
        return ctx.run(func, event, context)
    return inner


def _set_dynamodb_session_keys(session_keys):
    dynamodb_session_keys.set(session_keys)


def get_dynamodb_session_keys():
    """accessor to get the relevant credentials"""
    return dynamodb_session_keys.get()

