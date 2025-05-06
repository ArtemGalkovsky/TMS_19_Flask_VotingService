from flask import Flask, render_template, request
from databases.handlers.polls_handler import PollsHandler
app = Flask(__name__)
app.static_folder = "static"

@app.get("/")
@app.get("/index.html")
def index():
    polls = PollsHandler().get_all_polls()
    return render_template("index.html", polls=polls)

@app.get("/add_poll")
def add_poll():
    return render_template("add_poll.html")

if __name__ == '__main__':
    app.run(debug=True)