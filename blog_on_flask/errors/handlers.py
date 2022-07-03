from http import HTTPStatus

from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(HTTPStatus.NOT_FOUND)
def error_404(error):
    return render_template('errors/404.html'), HTTPStatus.NOT_FOUND


@errors.app_errorhandler(HTTPStatus.FORBIDDEN)
def error_403(error):
    return render_template('errors/403.html'), HTTPStatus.FORBIDDEN


@errors.app_errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def error_500(error):
    return render_template('errors/500.html'), HTTPStatus.INTERNAL_SERVER_ERROR
