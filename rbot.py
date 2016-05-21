#!/usr/bin/env python
from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/")
def send_intro_text():
	return """"
		Thanks for using rBot!
		To get started, type /help for a list of commands
	"""

@app.route("/create_list")
def route_create_list():
	return "ok"

@app.route("/highfive", methods=['POST'])
def route_highfive():
	result = {}
	result.text = "@" + request.args.get('user_name') + \
		' sent a high five to ' + request.args.get('text')
	return result