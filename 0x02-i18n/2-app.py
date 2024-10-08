#!/usr/bin/env python3
"""Get location from URL parameters."""
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
    """Get locale from request."""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index():
    """GET /
    Return: 2-index.html
    """
    return render_template('2-index.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
