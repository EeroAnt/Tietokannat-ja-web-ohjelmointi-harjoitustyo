from flask import render_template, abort, redirect, request, session
from src.db import db
from sqlalchemy import text
from src.querys import listing_for_index, get_headers_for_topic, get_messages, get_message, get_header
from src.time_formatter import format_timestamp
from src.clearance import check_clearance_level


def to_index():
	return render_template("index.html", topics=listing_for_index())


def to_topic(topic_id):
	if check_clearance_level(topic_id):
		result = get_headers_for_topic(topic_id)
		return render_template("topic.html", conversations=result, topic_id=topic_id)
	else:
		abort(404)


def to_conversation(topic_id, header_id):
	if check_clearance_level(topic_id):
		messages, topic, header = get_messages(topic_id, header_id)
		return render_template("conversation.html", messages=messages, topic_id=topic_id, header_id=header_id, topic=topic, header=header)
	else:
		abort(404)


def to_edit_message():
	message_id = request.form["message_id"]
	topic_id = request.form["topic_id"]
	header_id = request.form["header_id"]
	session["edit"] = "message"
	message = get_message(message_id)
	return render_template("edit.html", message=message, message_id=message_id, topic_id=topic_id, header_id=header_id)


def to_edit_header():
	header_id = request.form["header_id"]
	topic_id = request.form["topic_id"]
	session["edit"] = "header"
	header = get_header(header_id)
	return render_template("edit.html", header=header, header_id=header_id, topic_id=topic_id)


def return_from_edit(topic_id="", header_id=""):
	if session["edit"] == "message":
		del session["edit"]
		return redirect(f"/topic{topic_id}/conversation{header_id}")
	elif session["edit"] == "header":
		del session["edit"]
		return redirect(f"/topic{topic_id}")