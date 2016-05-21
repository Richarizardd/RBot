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

    try:
        conn.execute("""
            CREATE TABLE Users (
                UserID int PRIMARY KEY AUTO_INCREMENT,
                UserName varchar(255)
            );
            """)
    except Exception:
        print("Cannot create user table")
        pass
      
    try:            
        conn.execute("""
            CREATE TABLE Lists (
                ListID int PRIMARY KEY AUTO_INCREMENT,
                ListName varchar(255),
                UserID int,
                PermissionLevel int
            );
            """)
    except Exception:
        print("Cannot create lists table")
        pass
        
    try:            
        conn.execute("""
            CREATE TABLE Content (
                ContentID int PRIMARY KEY AUTO_INCREMENT,
                Title varchar(255),
                Description text,
                Category varchar(255),
                UserID int,
                URL int,
            );
            """)
    except Exception:
        print("Cannot create content table")
        pass
        
    try:            
        conn.execute("""
            CREATE TABLE List_to_Content (
                ListID int NOT NULL,
                ContentID int NOT NULL
            );
            """)
    except Exception:
        print("Cannot create list_to_content table")
        pass
  
 
#adds new user        
def add_user(user_name):
    
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
def add_list(list_name, user_id, permission=0):
    
    #create a new entry in the Lists table 
    #default permission level = 0 (private)
	try:
		conn.execute("""
            INSERT INTO Lists (ListName, UserID, PermissionLevel)
            VALUES (%s, %d, %d)
            """, list_name, user_id, permission)
	except Exception:
		print("Cannot add new list")
		pass
 
    
#adds new content
def add_content(title, desc, category, url, user_id, list_id):
    
    #create a new entry in the Content table
    try:
        conn.execute("""
        INSERT INTO Content (Title, Description, Category, UserID)
        VALUES (%s, %s, %s, %d)
        """, title, desc, category, user_id)
    except Exception:
        print("Cannot add new content")
        pass

    #create a new list-to-content relationship
    try:
        content_id = conn.insert_id()
        conn.execute("""
            INSERT INTO List_to_Content (ListID, ContentID)
            VALUES (%d, %d)
            """, list_id, content_id)
    except Exception:
        print("Cannot create associate content with list")
        pass
    

#returns information of interest given content ID
def search_content_by_id(content_id):
   
    #fetch content title, description, category and user name 
    try:
        cursor = conn.execute("SELECT * FROM Contents WHERE ContentID = '%d'" % content_id)
    except Exception:
        print("Query to table Contents fails")
        pass
     
    (title, desc, category, user_id) = cursor.fetchone()
    
    try:
        cursor = conn.execute("SELECT UserName FROM Users WHERE UserID = '%d'" % user_id)
    except Exception:
        print("Query to table Users fails")
        pass
    
    user_name = cursor.fetchone()[0]

    return title, desc, category, user_name
    

#returns information of interest given list name
def search_contents_by_list_name(list_name):
    
    #fetch lists given the list name if the permission level is public
    try:
        cursor = conn.execute("SELECT ListID FROM Lists WHERE ListName = '%s'" % list_name)
    except Exception:
        print("List name does not exist")
        pass
        
    list_ids = [row[0] for row in cursor]
    content_ids = []
    
    for list_id in list_ids:
        cursor = conn.execute("SELECT ContentID FROM List_to_Content WHERE ListID = '%d'" % list_id)
        content_ids += [row[0] for row in cursor]
        
    info = []
    for content_id in content_ids:
        try:
            cursor = conn.execute("SELECT * FROM Content WHERE ContentID = '%d'" % content_id)
            (title, desc, category, user_id) = cursor.fetchone()
        except Exception:
            pass
        try:
            cursor = conn.execute("SELECT UserName FROM Users WHERE UserID = '%d'" % user_id)
            user_name = cursor.fetchone()[0]
            info.append([title, desc, category, user_name])
        except Exception:
            pass
        
    return info
    

#returns information of interest given user ID
def search_contents_by_user(user_id):
    
    #fetch contents given user ID
    info = []
    try:
        cursor = conn.execute("SELECT * FROM Content WHERE UserID = '%d'" % user_id)
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