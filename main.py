from flask import Flask, render_template, request, redirect

from databases.exceptions import PollNotFound, PollAlreadyExists
from databases.handlers.polls_handler import PollsHandler
from databases.handlers.questions_handler import QuestionsHandler
from databases.handlers.votes_handler import VotesHandler
from databases.creators.questions_tables_creator import Creator as QuestionsTablesCreator
from databases.creators.votes_tables_creator import Creator as VotesTablesCreator

app = Flask(__name__)
app.static_folder = "static"


@app.get("/")
@app.get("/index.html")
def index():
    polls = PollsHandler().get_all_polls()

    found_polls = []
    for poll in polls:
        poll_id = poll[0]
        poll_name = poll[1]
        try:
            if QuestionsHandler().is_questions_table_exists(poll_id) and \
                    VotesHandler().is_votes_table_exists(poll_id) and \
                    poll_name.strip():
                found_polls.append(poll)
        except PollNotFound:
            print(f"Poll {poll_id} not found!")

    return render_template("index.html", polls=found_polls)


@app.route("/add_poll", methods=["POST", "GET"])
def add_poll():
    ok = request.args.get("ok", None)

    if request.method == "POST":
        multiple_votes_enabled = request.form.get("multiple_votes_enabled", "")

        try:
            PollsHandler().add_poll(request.form["name"],
                                    request.form["description"],
                                    True if multiple_votes_enabled == "on" else False)
        except PollAlreadyExists:
            return redirect("/add_poll?ok=&error=Poll_already_exists!")

        new_poll_id = PollsHandler().get_last_poll_id()

        VotesTablesCreator().create_table(new_poll_id)
        QuestionsTablesCreator().create_table(new_poll_id)

        questions = request.form.getlist("question")

        for question in questions:
            QuestionsHandler().add_question(new_poll_id, question)

        return redirect("/add_poll?ok=oh_yee")

    form_added_successfully = 0
    if ok is None:
        form_added_successfully = -1
    elif ok:
        form_added_successfully = 1

    return render_template("add_poll.html",
                           form_added_successfully=form_added_successfully,
                           error=request.args.get("error", "Unknown error"))


@app.get("/view_poll")
def view_poll():
    poll_id = request.args.get("id", None)
    if poll_id and isinstance(poll_id, str) and poll_id.isnumeric():
        poll_id_int = int(poll_id)

        poll_questions = QuestionsHandler().get_questions(poll_id_int)
        poll_data = PollsHandler().get_poll_data(poll_id_int)

        return render_template("view_poll.html", poll={
            "title": poll_data[0],
            "description": poll_data[1],
            "multiple_votes_enabled": poll_data[2],
            "questions": poll_questions,
            "id": poll_id_int
        })

    return redirect("/", 404)


@app.post("/vote")
def vote():
    print(request.form)

    return redirect("/view_poll")


if __name__ == '__main__':
    app.run(debug=True)
