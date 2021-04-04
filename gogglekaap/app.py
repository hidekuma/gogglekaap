from flask import Flask

app = Flask(__name__)

print('__name__', __name__)
print('DEBUG', app.config['DEBUG'])

@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    print('run')
    app.run(debug=True, port=5051, host='localhost')
