import traceback, os, uuid as _uuid
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from database.sheets_db import get_student, get_passage, save_attempt, build_attempt_record

app = Flask(__name__)
app.secret_key = "ssc-steno-portal-change-in-production"

# ── In-process result store — avoids 4KB cookie limit entirely ───────────────
# Stores {token: {"result": ..., "highlighted": ...}} in server memory.
# Works on any host with no extra packages. Cleared on server restart (fine for tests).
_RESULT_STORE = {}

from admin import admin_bp
app.register_blueprint(admin_bp)


# HOME
@app.route("/")
def start_page():
    return render_template("start.html")


# AJAX — lookup student name
@app.route("/lookup-student")
def lookup_student():
    sid     = request.args.get("id", "").strip()
    student = get_student(sid)
    if student:
        name = student.get("StudentName") or student.get("Name") or ""
        return jsonify({"name": name})
    return jsonify({"name": ""})


# POST — validate & start test
@app.route("/start-test", methods=["POST"])
def start_test():
    data         = request.get_json()
    student_id   = (data.get("student_id")   or "").strip()
    passage_code = (data.get("passage_code") or "").strip()

    if not student_id or not passage_code:
        return jsonify({"status": "error", "message": "Student ID and Passage Code are required."})

    student = get_student(student_id)
    if not student:
        return jsonify({"status": "error", "message": "Student ID not found. Please check and try again."})

    passage = get_passage(passage_code)
    if not passage:
        return jsonify({"status": "error", "message": "Invalid or inactive Passage Code."})

    session["student_id"]   = student_id
    session["passage_code"] = passage_code

    return jsonify({"status": "ok"})


# GET — typing page
@app.route("/typing/<code>")
def typing_page(code):
    passage = get_passage(code)
    if not passage:
        return render_template("error.html", message="Passage code is invalid or inactive."), 404

    student_id = request.args.get("student", "").strip()
    if student_id:
        session["student_id"] = student_id

    student_name = student_id
    if student_id:
        student = get_student(student_id)
        if student:
            student_name = student.get("StudentName") or student.get("Name") or student_id

    return render_template(
        "typing_test.html",
        code=code,
        passage=passage["text"],
        total_words=passage["word_count"],
        student_name=student_name
    )


# POST — evaluate & save
@app.route("/submit-test", methods=["POST"])
def submit_test():
    try:
        from engine.evaluation_engine import evaluate, highlight_passage

        data         = request.get_json()
        typed_text   = (data.get("typed_text")   or "").strip()
        passage_code = (data.get("passage_code") or "").strip()
        time_taken   = int(data.get("time_taken") or 0)
        student_id   = (data.get("student_id")   or session.get("student_id", "")).strip()

        if not typed_text or not passage_code:
            return jsonify({"status": "error", "message": "Missing typed text or passage code."})

        passage = get_passage(passage_code)
        if not passage:
            return jsonify({"status": "error", "message": "Invalid passage code."})

        result = evaluate(
            master_text=passage["text"],
            typed_text=typed_text,
            total_words=passage["word_count"]
        )

        typed_words   = len(typed_text.split())
        minutes       = time_taken / 60 if time_taken > 0 else 1
        result["wpm"] = round(typed_words / minutes)

        highlighted = highlight_passage(passage["text"], typed_text)

        attempt_id = None
        if student_id:
            try:
                record = build_attempt_record(
                    student_id=student_id,
                    passage_code=passage_code,
                    result=result,
                    time_taken=time_taken,
                    typed_words=typed_words,
                    highlighted=highlighted
                )
                save_attempt(record)
                attempt_id = record["AttemptID"]
            except Exception as e:
                print(f"[WARN] Could not save attempt: {e}")

        # Store large data server-side; only a tiny token goes in the cookie
        token = str(_uuid.uuid4())
        _RESULT_STORE[token] = {"result": result, "highlighted": highlighted}
        session["result_token"] = token
        session["attempt_id"]   = attempt_id

        return jsonify({"status": "ok"})

    except Exception as e:
        err = traceback.format_exc()
        print(f"[ERROR] submit_test crashed:\n{err}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


# GET — results page
@app.route("/results")
def results_page():
    token = session.get("result_token", "")
    data  = _RESULT_STORE.get(token)
    if not data:
        return redirect(url_for("start_page"))
    return render_template("result.html",
                           result=data["result"],
                           highlighted=data["highlighted"])


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
