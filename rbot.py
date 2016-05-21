#!/usr/bin/env python
from flask import flask
app = Flask(__name__)

@app.route("/")
def send_intro_text():
	return """"
		Thanks for using rBot!
		To get started, type /help for a list of commands
	"""