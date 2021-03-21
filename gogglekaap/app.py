from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World and Python!"


print('__name__:', __name__)

if __name__ == '__main__':
    #FLASK_ENV=development
    app.run(port=5000, host='0.0.0.0')
