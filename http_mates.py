import os
import time
from flask import Flask, render_template, request, redirect, url_for, session
from mates import generate_question
from config import TARGET_SCORE, TIME_NO_PENALTY, PENALTY_PER_SECOND, REPEAT_FAILED_AFTER

app = Flask(__name__, template_folder="templates")
app.secret_key = os.environ.get("HTTP_MATES_SECRET", "please-change-this-default-useless-secret")

SESSION_KEY = "quiz_state"


def new_quiz_state():
    return {
        "started": False,
        "done": False,
        "my_score": 0,
        "failed_stack": [],
        "q_counter": 0,
        "current_text": None,
        "current_answer": None,
        "current_score": None,
        "question_start": None,
        "global_time_start": None,
        "global_time_seconds": 0.0,
        "last_message": None,
    }


def get_state():
    state = session.get(SESSION_KEY)
    if state is None:
        state = new_quiz_state()
        session[SESSION_KEY] = state
    return state


def save_state(state):
    session[SESSION_KEY] = state
    session.modified = True


def choose_next_question(state):
    state["q_counter"] += 1
    if state["failed_stack"] and state["failed_stack"][0]["q_id"] < state["q_counter"] - REPEAT_FAILED_AFTER:
        failed = state["failed_stack"].pop(0)
        state["current_text"] = failed["text"]
        state["current_answer"] = failed["answer"]
        state["current_score"] = failed["score"]
    else:
        text, answer, score = generate_question()
        state["current_text"] = text
        state["current_answer"] = answer
        state["current_score"] = score
    state["question_start"] = time.time()
    return state


def start_quiz(state):
    state = new_quiz_state()
    state["started"] = True
    state["global_time_start"] = time.time()
    choose_next_question(state)
    save_state(state)
    return state


@app.route("/", methods=["GET"])
def index():
    state = get_state()
    if state["started"] and not state["done"] and state["current_text"] is None:
        choose_next_question(state)
        save_state(state)

    return render_template(
        "http_mates.html",
        state=state,
        target_score=TARGET_SCORE,
        time_no_penalty=TIME_NO_PENALTY,
        penalty_per_second=PENALTY_PER_SECOND,
    )


@app.route("/start", methods=["POST"])
def start():
    start_quiz(get_state())
    return redirect(url_for("index"))


@app.route("/answer", methods=["POST"])
def answer():
    state = get_state()
    if not state["started"] or state["done"] or state["current_text"] is None:
        return redirect(url_for("index"))

    answer_value = request.form.get("answer", "").strip()
    if not answer_value or not answer_value.lstrip("-+").isdigit():
        state["last_message"] = "Please enter a valid integer answer."
        save_state(state)
        return redirect(url_for("index"))

    user_input = int(answer_value)
    time_taken = time.time() - float(state["question_start"])

    if user_input == state["current_answer"]:
        penalty_time = max(0, time_taken - TIME_NO_PENALTY)
        this_score = max((state["current_score"] - int(penalty_time * PENALTY_PER_SECOND)), 0)
        state["my_score"] += this_score
        state["last_message"] = (
            f"✅ Correcte! Temps: {time_taken:.2f}s, puntuació: {this_score}"
        )
    else:
        state["last_message"] = (
            f"❌ Resposta incorrecta. Resposta correcta: {state['current_answer']}"
        )
        state["failed_stack"].append(
            {
                "q_id": state["q_counter"],
                "text": state["current_text"],
                "answer": state["current_answer"],
                "score": state["current_score"],
            }
        )

    if state["my_score"] >= TARGET_SCORE:
        state["done"] = True
        state["global_time_seconds"] = time.time() - state["global_time_start"]
        state["current_text"] = None
        state["current_answer"] = None
        state["current_score"] = None
        state["question_start"] = None
    else:
        choose_next_question(state)

    save_state(state)
    return redirect(url_for("index"))


@app.route("/restart", methods=["POST"])
def restart():
    start_quiz(get_state())
    return redirect(url_for("index"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
