from flask import Flask
from skywalking_flask import SkywalkingFlask


app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello World"


SkywalkingFlask(app, service='My Service', collector='127.0.0.1:11800')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
