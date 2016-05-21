#!/usr/bin/env python
from flask import Flask
from flask import request
import sys
app = Flask(__name__)

import data_handler

@app.route("/")
def send_intro_text():
	return """
		Thanks for using rBot!
		To get started, type /help for a list of commands
	"""

@app.route("/test_route")
def get_from_test_route():
	return "test works!"

@app.route("/create_list")
def route_create_list():
	return "ok"

@app.route("/highfive", methods=['POST'])
def route_highfive():
	print( str(request.args))
	result = "args: " + str(request.form['user_name']) + " " + str(request.form['text'])
	return result
	# result = {}
	# result.text = "@" + str(request.args.get('user_name')) + \
	# 	' sent a high five to ' + str(request.args.get('text'))
	# return result

@app.route("/add_article", methods=['POST'])
def route_add_article():
	args = request.form['text'].split(' ')
	if len(args) < 3:
		return "please use the format /radd <title> <url> <description>"
	title = args[0]
	url = args[1]
	description = ' '.join(args[2:])

	data_handler.add_content(title, description, 'stuff', url, 1, 1)

	return "added!"
	# result = {}
	# result.text = "@" + str(request.args.get('user_name')) + \
	# 	' sent a high five to ' + str(request.args.get('text'))
	# return result

@app.route("/get_article", methods=['GET'])
def route_get_article():
	arg = request.form['text']
	return search_content_by_id(request.form['text'])
	# result = {}
	# result.text = "@" + str(request.args.get('user_name')) + \
	# 	' sent a high five to ' + str(request.args.get('text'))
	# return result

if __name__ == "__main__":
    app.run()