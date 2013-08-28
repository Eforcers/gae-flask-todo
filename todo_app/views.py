from main import app
from flask import render_template

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'

@app.route('/_ah/warmup')
def warmup():
    #TODO: Warmup
    return 'Warming Up...'