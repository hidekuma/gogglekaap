from flask import Flask

db = 'database'

def create_app():
    print('run: create_app()')
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'hello world'

    return app