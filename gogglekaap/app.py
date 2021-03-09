from flask import Flask

app = Flask(__name__)

# NOTE: python app.py -> __name__ -> __main__
# NOTE: flask run -> __name__ -> {__name__}.py
print('__name__: ', __name__)
print('DEBUG:', app.config['DEBUG'])

@app.route('/')
def index():
    return 'Hello World'

if __name__ == '__main__':
    print('run')
    app.run(
        debug=True,
        port=5051,
        host='localhost'
    )
