#!/usr/bin/env python
from myapp import app
from user import add_user

my_list = {'1': {'name': 'jj', 'pass': 'pass', 'api_key': '661'},
           '2': {'name': 'admin', 'pass': 'admin', 'api_key': '88121'},
           '3': {'name': 'ivan', 'pass': 'ivan', 'api_key': '771'}}
for k, v in my_list.iteritems():
    add_user(uid=k, name=v['name'], password=v['pass'], api_key=v['api_key'])

app.run(debug=True)
