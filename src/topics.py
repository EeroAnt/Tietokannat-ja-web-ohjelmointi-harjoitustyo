from flask import redirect, request, session
from src.db import db
from src.error import error
from sqlalchemy import text

def _create():
    if session["admin"]:
        topic = request.form["topic"]
        check_topic = db.session.execute(text("SELECT Topic FROM topics WHERE Topic=:topic"), {"topic":topic}).fetchone()
        if check_topic:
            return error("topic_error")
        sql_topics = "INSERT INTO topics (Topic) VALUES (:topic)"
        db.session.execute(text(sql_topics), {"topic":topic})
        db.session.commit()
    return redirect("/")

def _remove():
    if session["admin"]:
        topic = request.form["topic"]
        check_topic = db.session.execute(text("SELECT Topic FROM topics WHERE Topic=:topic"), {"topic":topic}).fetchone()
        if not check_topic:
            return error("topic_not_found_error")
        sql_topics = "DELETE FROM topics WHERE Topic=:topic"
        db.session.execute(text(sql_topics), {"topic":topic})
        sql_headers = "DELETE FROM headers WHERE topic=:topic"
        db.session.execute(text(sql_headers), {"topic":topic})
        sql_messages = "DELETE FROM messages WHERE topic=:topic"
        db.session.execute(text(sql_messages), {"topic":topic})
        db.session.commit()
    return redirect("/")
