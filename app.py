import os
from flask import Flask, render_template

app = Flask(__name__)
wsgi_app = app.wsgi_app


@app.route('/')
def homepage():
    return render_template('layout.html')


if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5858'))
    except ValueError:
        PORT = 5858
    app.run(HOST, PORT, debug=True)
