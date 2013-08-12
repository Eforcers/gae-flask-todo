from main import app

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'

@app.route('/_ah/warmup')
def warmup():
    #TODO: Warmup
    return 'Warming Up...'