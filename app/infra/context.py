from typing import Optional

from flask import current_app, has_request_context, request

from werkzeug.local import LocalProxy
from werkzeug.wrappers import BaseRequest

from app.infra.orm import Session, create_session


def current_context() -> Optional[BaseRequest]:
    if has_request_context():
        return request._get_current_object()


def current_config() -> Optional[dict]:
    if has_request_context():
        app = current_app
        return app.config['APP_CONFIG']


@LocalProxy
def session() -> Session:
    ctx = current_context()
    if hasattr(ctx, '_current_session'):
        session_ = ctx._current_session
    else:
        session_ = create_session(current_config())
        ctx._current_session = session_
    return session_
