"""Make apps quickly in python."""
import os

import flask
from werkzeug.local import LocalProxy

from . import files
from . import html
from .app import App
from .files import File
from .html import HTMLElement, Link, Page, Paragraph
from .utils import needs_params, needs_signin, sign_in_snippet, signin
from ..database import db

auth = LocalProxy(lambda: flask.request.auth)
signed_in = LocalProxy(lambda: flask.request.signed_in)

# TODO: signinwall(exclude=['/a', '/b'])
# TODO: @need_signin
# TODO: Param checking with @needs_params
