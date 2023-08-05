from sanic import Sanic
from sanic.response import text
from skywalking.plugins import sw_requests

from skywalking_sanic import SkywalkingSanic

sw_requests.install()

app = Sanic(__name__)


@app.route('/')
def hello_world(request):
    return text("Hello World")


SkywalkingSanic(app, service='My Service', collector='127.0.0.1:11800')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
