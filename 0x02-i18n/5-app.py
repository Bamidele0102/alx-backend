#!/usr/bin/env python3
"""Parametrize templates."""
from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Dict, Union


app = Flask(__name__)
babel = Babel(app)


class Config(object):
    """Babel configuration."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """Choose the best language to serve among the supported ones
    or the one specified in 'locale' URL parameter if given and supported
    """
    # If we have 'locale' in the request arguments
    # and this language is supported, return it
    lang = request.args.get('locale')
    if lang and lang in app.config['LANGUAGES']:
        return lang

    # Return the default preference from the browser
    return request.accept_languages.best_match(app.config['LANGUAGES'])

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """Return a user dictionary, or None if the ID
    cannot be found or if login_as was not passed
    """
    try:
        user_id = int(request.args.get('login_as'))
    except BaseException:
        return None

    return users.get(user_id)


@app.before_request
def before_request() -> None:
    """Should use get_user to find a user if any,
    and set it as a global on flask.g.user
    """
    g.user = get_user()


@app.route('/', strict_slashes=False)
def index():
    """GET /
    Return: 5-index.html
    """
    return render_template('5-index.html', user=g.user)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
