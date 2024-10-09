from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World"


if __name__ == '__main__':
    app.run(host="172.20.10.3", port="50000")

