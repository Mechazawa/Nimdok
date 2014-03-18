Nimdok 
======
[![Build Status](https://secure.travis-ci.org/Mechazawa/Nimdok.png)] (http://travis-ci.org/Mechazawa/Nimdok)[![Dependency Status](https://gemnasium.com/Mechazawa/Nimdok.png)](https://gemnasium.com/Mechazawa/Nimdok)

A bot based on BotKit. Currently running on a couple of channels on rizon.
Commands and triggers can be found in the README.md in the Modules folder.

Setting up Nimdok
======
First clone the repo
```bash
git clone "https://github.com/Mechazawa/Nimdok.git"
cd Nimdok
git submodule init
git submodule update
#optional; get the latest version of botkit
cd Botkit
git pull
cd ..
```

Then copy and edit the contents of apikeys.py
```bash
cp apikeys.py.example apikeys.py
nano apikeys.py
```

Then modify nimdok.py so that He'll connect to the correct server.
```bash
nano nimdok.py
```
