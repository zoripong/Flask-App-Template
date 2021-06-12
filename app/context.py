from typing import Optional

from flask import current_app, has_request_context, request

from werkzeug.local import LocalProxy
from werkzeug.wrappers import BaseRequest

from app.orm import Session, create_engine, create_session

_test_app = None
_test_ctx = None


def current_context() -> Optional[BaseRequest]:
    if _test_app is not None:
        ctx = _test_ctx
        app_config = _test_app
    if has_request_context():
        ctx = request._get_current_object()
        app_config = current_app.config['APP_CONFIG']
    return ctx, app_config


@LocalProxy
def session() -> Session:
    ctx, app_config = current_context()
    if hasattr(ctx, '_current_session'):
        session_ = ctx._current_session
    else:
        session_ = create_session(create_engine(app_config))
        ctx._current_session = session_
    return session_
