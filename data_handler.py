# -*- coding: utf-8 -*-
import sqlite3


#runs initial commands to wipe the DB and set up all tables
def set_up_DB(conn):

	#drop the tables if they already exists
	#fail gracefully if the tables don't exist yet

	try:
		conn.execute('DROP TABLE Users')
	except Exception:
		print("Users doesn't exist yet")

	try:
		conn.execute('DROP TABLE Lists')
	except Exception:
		print("Lists doesn't exist yet")

	try:
		conn.execute('DROP TABLE Content')
	except Exception:
		print("Content doesn't exist yet")

	try:
		conn.execute('DROP TABLE List_to_Content')
	except Exception:
		print("List_to_Content doesn't exist yet")

	try:
		conn.execute('DROP TABLE Tags')
	except Exception:
		print("Tags doesn't exist yet")

	try:
		conn.execute('DROP TABLE Items_Tags')
	except Exception:
		print("Items_Tags doesn't exist yet")

	conn.commit()

	try:
		conn.execute("""
			CREATE TABLE Users (
				UserID INTEGER PRIMARY KEY AUTOINCREMENT,
				UserName VARCHAR(33)
			)
			""")
	except Exception:
		print("Cannot create user table")
	
	try:   
		conn.execute("""
			CREATE TABLE Lists (
				ListID INTEGER PRIMARY KEY AUTOINCREMENT,
				ListName VARCHAR(32),
				UserID INTEGER,
				PermissionLevel INTEGER
			)
		""")
	except Exception:
		print("Cannot create lists table")
		
	try:            
		conn.execute("""
			CREATE TABLE Content (
				ContentID INTEGER PRIMARY KEY AUTOINCREMENT,
				Title VARCHAR(32),
				Description TEXT,
				Category VARCHAR(32),
				UserID INTEGER,
				URL INTEGER
			)
		""")
	except Exception:
		print("Cannot create content table")
		
	try:
		conn.execute("""
			CREATE TABLE List_to_Content (
				ListID INTEGER NOT NULL,
				ContentID INTEGER NOT NULL
			)
		""")
	except Exception:
		print("Cannot create list_to_content table")
		
	try:
		conn.execute("""
			CREATE TABLE Tags(
				TagID INTEGER PRIMARY KEY NOT NULL,
				TagTitle INTEGER NOT NULL
			)
		""")
	except Exception:
		print("Cannot create Tags table")
		
	try:
		conn.execute("""
			CREATE TABLE Items_Tags(
				ContentID INTEGER NOT NULL,
				TagID INTEGER NOT NULL,
				PRIMARY KEY(ContentID, TagID)
			)
		""")
	except Exception:
		print("Cannot create Items_Tags table")
   


	conn.commit()
 
#adds new user        
def add_user(conn, user_name):
	
	#create a new entry in the User table 
	try:
		conn.execute("""
			INSERT INTO Users (UserName)
			VALUES (%s)
			""", user_name)
	except Exception:
		print("Cannot add new user")
		pass
		
		
#adds new list        
def add_list(conn, list_name, user_id, permission=0):
	
	#create a new entry in the Lists table 
	#default permission level = 0 (private)
	try:
		conn.execute("""
			INSERT INTO Lists (ListName, UserID, PermissionLevel)
			VALUES (%s, %s, %s)
			""", list_name, user_id, permission)
	except Exception:
		print("Cannot add new list")
 
	
#adds new content
def add_content(conn, title, desc, category, url, user_name, list_id):
	
	#check if the user owns the list being added to
	try:
		cursor = conn.execute("""
			SELECT ListID FROM Lists WHERE ListID = %s AND UserID = (
				SELECT UserID FROM Users WHERE User
			)

		""")


	#create a new entry in the Content table
	try:
		conn.execute("""
		INSERT INTO Content (Title, Description, Category, UserID)
		VALUES (%s, %s, %s, %s)
		""", title, desc, category, user_id)
	except Exception:
		print("Cannot add new content")

	#create a new list-to-content relationship
	try:
		content_id = conn.insert_id()
		conn.execute("""
			INSERT INTO List_to_Content (ListID, ContentID)
			VALUES (%s, %s)
			""", list_id, content_id)
	except Exception:
		print("Cannot create associate content with list")
	

#returns information of interest given content ID
def search_content_by_id(conn, content_id):
   
	#fetch content title, description, category and user name 
	try:
		cursor = conn.execute("SELECT * FROM Contents WHERE ContentID = '%s'" % content_id)
	except Exception as err:
		print("Query to table Contents fails")
		return "something went wrong selecting the content!  " + str(err)
		
	for row in cursor:
		(title, desc, category, user_id) = row

	return title, desc, category, user_id
	

#returns information of interest given list name
def search_contents_by_list_name(conn, list_name):
	
	#fetch lists given the list name if the permission level is public
	try:
		cursor = conn.execute("SELECT ListID FROM Lists WHERE ListName = '%s'" % list_name)
	except Exception:
		print("List name does not exist")
		pass
		
	list_ids = [row[0] for row in cursor]
	content_ids = []
	
	for list_id in list_ids:
		cursor = conn.execute("SELECT ContentID FROM List_to_Content WHERE ListID = '%s'" % list_id)
		content_ids += [row[0] for row in cursor]
		
	info = []
	for content_id in content_ids:
		try:
			cursor = conn.execute("SELECT * FROM Content WHERE ContentID = '%s'" % content_id)
			(title, desc, category, user_id) = cursor.fetchone()
		except Exception:
			pass

		try:
			cursor = conn.execute("SELECT UserName FROM Users WHERE UserID = '%s'" % user_id)
			user_name = cursor.fetchone()[0]
			info.append([title, desc, category, user_name])
		except Exception:
			pass
		
	return info
	

#returns information of interest given user ID
def search_contents_by_user(conn, user_id):
	
	#fetch contents given user ID
	info = []
	try:
		cursor = conn.execute("SELECT * FROM Content WHERE UserID = '%s'" % user_id)
		for row in cursor:
			(title, desc, category, user_id) = row
			# try:
			#     cursor = conn.execute("SELECT UserName FROM Users WHERE UserID = '%d'" % user_id)
			#     user_name = cursor.fetchone()[0]
			#     info.append([title, desc, category, user_name])
			# except Exception:
			#     pass
	except Exception:
		pass
	
	return info
		
	
if __name__ == '__main__':
	#run dev tests
	conn = sqlite3.connect('db/research_test.db')
	set_up_DB(conn)
	conn.close()