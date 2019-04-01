from sanic import Sanic

from views import bp

app = Sanic()
app.blueprint(bp)

app.run(host='0.0.0.0', port=8000)
