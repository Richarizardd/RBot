#!/usr/local/bin python

class User(object):
    
    def __init__(self, user_id):
        '''
        Args:
            user_id: user ID
        '''
        self.uid = user_id
        self.domains = list() # list of research categories
        self.lists = list() # list of content lists user possessed
    
    
class List(object):
    
    def __init__(self, list_id, list_name):
        '''
        Args:
            list_id: list ID
            list_name: list name
        '''
        self.lid = list_id
        self.lname = self.list_name
        self.permission_level = 0 # private = 0, public = 1 
        self.cids = list()
        
    
class Content(object):
    
    def __init__(self, content_id, secret_id, title, user_id, list_id, desc, category):
        '''
        Args:
            content_id: content ID
            secret_id: secret ID
            title: content title
            user_id: ID of user the content belongs to
            list_id: ID of list the content belongs to
            desc: short description of the content
            category: research category content falls in
        '''
        self.cid = content_id
        self.secret_id = secret_id
        self.title = title
        self.uid = uid
        self.lid = lid
        self.desc = description
        self.category = category
           