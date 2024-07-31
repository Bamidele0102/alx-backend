#!/usr/bin/env python3
"""Parametrize templates."""
from flask import Flask, render_template, request
from flask_babel import Babel
from jinja2 import select_autoescape

app = Flask(__name__)
babel = Babel(app)

class Config(object):
    """Babel configuration."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(Config)

# Configure Jinja2's autoescaping for HTML and XML files
app.jinja_env.autoescape = select_autoescape(['html', 'xml'])

@babel.localeselector
def get_locale():
    """Get locale from request."""
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/', strict_slashes=False)
def index():
    """GET /
    Return: 3-index.html
    """
    return render_template('3-index.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
