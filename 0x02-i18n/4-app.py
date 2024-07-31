#!/usr/bin/env python3
"""Parametrize templates."""
from flask import Flask, render_template, request
from flask_babel import Babel


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


@app.route('/', strict_slashes=False)
def index():
    """GET /
    Return: 4-index.html
    """
    return render_template('3-index.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
