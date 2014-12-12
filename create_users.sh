#!/usr/bin/env bash

mkdir -p myapp/data

echo '{"1": {"api_key": "661", "name": "jj", "pass": "bar"},
         "3": {"api_key": "771", "name": "ivan", "pass": "ivan"}, 
         "2": {"api_key": "88121", "name": "admin", "pass": "admin"}}' > myapp/data/users.json

