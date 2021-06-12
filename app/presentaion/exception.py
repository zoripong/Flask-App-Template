import json
import typing as t

from werkzeug._internal import _get_environ
from werkzeug.exceptions import (
    BadRequest as BadRequest_,
    Forbidden as Forbidden_,
    HTTPException,
    InternalServerError as InternalServerError_,
    NotFound as NotFound_,
    ServiceUnavailable as ServiceUnavailable_,
    Unauthorized as Unauthorized_,
)
from werkzeug.wrappers import Response


class JSONHTTPException(HTTPException):
    """Base JSON HTTP exception."""

    def get_body(
        self,
        environ: t.Optional[t.Any] = None,
        scope: t.Optional[dict] = None,
    ) -> str:
        return json.dumps({
            'status_code': self.code,
            'description': self.description,
            'message': self.description,
            'name': self.name,
            'ok': False,
        })

    def get_response(
        self,
        environ: t.Optional[t.Any] = None,
        scope: t.Optional[dict] = None,
    ) -> Response:
        if self.response is not None:
            return self.response
        if environ is not None:
            environ = _get_environ(environ)
        headers = self.get_headers(environ)
        headers.append(('Content-Type', 'application/json'))
        return Response(self.get_body(environ), self.code, headers)


class NotFound(JSONHTTPException, NotFound_):
    """Requested resource is not found."""


class Forbidden(JSONHTTPException, Forbidden_):
    """Requested resource is forbidden."""


class BadRequest(JSONHTTPException, BadRequest_):
    """Request has syntax error."""


class ServiceUnavailable(JSONHTTPException, ServiceUnavailable_):
    """Service unavailabl error."""


class Unauthorized(JSONHTTPException, Unauthorized_):
    """Unauthorize."""


class InternalServerError(JSONHTTPException, InternalServerError_):
    """Internal server error."""
