import sqlite3


#runs initial commands to wipe the DB and set up all tables
def set_up_DB(conn):

	#drop the tables if they already exists
	#fail gracefully if the tables don't exist yet
	try:
		conn.execute('DROP TABLE Users')
	except Exception:
		print("Users doesn't exist yet")
		pass

	try:
		conn.execute('DROP TABLE Lists')
	except Exception:
		print("Lists doesn't exist yet")
		pass

	try:
		conn.execute('DROP TABLE Content')
	except Exception:
		print("Content doesn't exist yet")
		pass
	
	# conn.execute("""
	# 	CREATE TABLE Users (
			
	# 	)
	# 	""")



if __name__ == '__main__':
	#run dev tests
	conn = sqlite3.connect('db/research_test.db')
	set_up_DB(conn)