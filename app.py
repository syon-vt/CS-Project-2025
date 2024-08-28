from flask import Flask, render_template
from time import strftime

app = Flask(__name__)

@app.route("/")
def home():
    return "hello"

if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()