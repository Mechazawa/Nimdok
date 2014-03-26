#! /bin/env bash

sudo pip install -r requirements.txt
git pull origin master
git submodule init
git submodule update

echo "Now copy and modify the apikeys.py.example and edit nimdok.py"
