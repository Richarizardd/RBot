
from slacker import Slacker
slack = Slacker('xoxp-3078035362-22751824724-44794572839-a983a8880f')
slack.chat.post_message('#newhires', 'Hello from slacker')
response = slack.users.list()
users = response.body['members']

valid_users = []
for u in users:
    if (u['deleted'] == False):
        valid_users.append(u)
names, ids = [str(u['name']) for u in valid_users], [str(u['id']) for u in valid_users]


