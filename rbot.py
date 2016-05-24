#!/usr/bin/env python
from flask import Flask
from flask import request
from flask import g
import sqlite3
import sys
import shlex
import data_handler
app = Flask(__name__)

import data_handler
app.debug = True

# open a db connection and have it fail gracefully on exitdef get_db():
DATABASE = 'db/research_test.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('db/research_test.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



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
	result = "@" + str(request.form['user_name']) + \
		' sent a high five to ' + str(request.form['text'])
	return result

#adds a list to the user's lists
@app.route("/create_list", methods=['POST'])
def route_add_list():
	args = []

	lexer = shlex.shlex(request.form['text'])
	for token in lexer:
		args.append(token)

	if len(args < 2):
		return "please use the format:\n/r+list <list_name> \"<description>\""


	lname = args[1]
	descr = args[2]




@app.route("/add_article", methods=['POST'])
def route_add_article():

	args = []

	lexer = shlex.shlex(request.form['text'])
	for token in lexer:
		args.append(token)

	if len(args) < 5:
		return "please use the format:\n/radd <list> <title> <description> \"<url>\" \"<string separated category tags>\""


	list_name = args[0]
	title = args[1]
	description = args[2][1:len(args[2])-1]
	url = args[3]
	#array deliminated by spaces
	tags = args[4][1:len(args[4])-1].split(' ')

	user_name = request.form['user_name']

	data_handler.add_content(get_db(), title, description, tags, url, 1, 1)

	return "added! title: " + str(title) + ", description: " + str(description) + ", tags: " + str(tags) + ", url: " + str(url)


@app.route("/get_article", methods=['POST'])
def route_get_article():
	arg = request.form['text']

	#get the article with that ID value
	result = data_handler.search_content_by_id(get_db(), request.form['text'])

	return result
	# result = {}
	# result.text = "@" + str(request.args.get('user_name')) + \
	# 	' sent a high five to ' + str(request.args.get('text'))
	# return result






if __name__ == "__main__":
    app.run()