Nimdok
======

A bot based on BotKit. Currently running on a couple of channels on rizon.

Commands and triggers
======
| Module  | Type    | What             | Description                           | admin | Example         |
| --------|---------|------------------|---------------------------------------|-------|-------------------|
| admin   | Command | addadmin         | Adds a user to the admin group        | Yes   | :addadmin shodan  |
| admin   | Command | admins           | Lists all the admins                  | No    | :admins           |
| admin   | Command | remadmin         | Removes a user from the admin group   | Yes   | :remadmin shodan  |
| bots    | Trigger | .bots            | Shows basic bot info                  | No    | .bots             |
| btc     | Command | btc              | Shows the current value of bitcoin    | No    | :btc              |
| chan    | Trigger | thread url       | Shows 4chan thread statistics         | No    | \*4chan thread\*  |
| chatlog | Trigger | message          | Writes all messages to chat.log       | No    | Any message       |
| control | Command | part             | Makes the bot part from a channel     | Yes   | :part #/g/sicp    |
| doge    | Command | doge             | Shows the current value of dogecoin   | No    | :doge             |
| execgo  | Command | go               | Executes GoLang code, shows the result| No    | :go fmt &#124; fmt.Println ("Hello, 世界") |
| execpython | Command | py            | Executes Python code, shows the result| No    | :py print "hi"    |
| fortune | Command | fortune          | Shows your fortune                    | No    | :fortune          |
| fun     | Command | 8ball            | Gives you a random answer             | No    | :8ball question   |
| fun     | Trigger | y/n              | Searches for 'y/n' in the message and prints a yes or a no' | No   | ask her out? y/n |
| fun     | Trigger | this or that     | Splits after ' or ' and returns one of your choices | No   | blondes or brunettes? |
| insult  | Trigger | message          | Insults people when they insult Nimdok| No    | Nimdok sucks      |
| insult  | Command | insult           | Adds an insult                        | Yes   | :insult okay then |
| isup    | Command | isup             | Displays if a website is down or not  | No    | :isup google.com  |
| lastfm  | Command | np               | Shows what the user is listenting to  | No    | :np               |
| lastfm  | Command | np register      | Registers the users lastfm username   | No    | :np register usr  |
| leet    | Command | leet             | Converts text to "leetspeak"          | No    | :leet hello world |
| lmgtfy  | Command | lmgtfy           | Creates a lmgtfy link                 | No    | :lmgtfy something |
| lmgtfy  | Command | lmddgtfy         | Creates a lmgddgtfy link              | No    | :lmddgtfy stuff   |
| ltc     | Command | ltc              | Shows the current litecoin price      | No    | :ltc              |
| misc    | Command | Dongle           | Forks someone's dongle                | No    | :dongle shodan    |
| misc    | Trigger | donger           | Tells people to raise their dongers   | No    | raise that donger |
| more    | Command | more             | Shows what is stored in the "more"    | No    | :more             |
| ping    | Command | ping             | replies with pong                     | No    | :ping             |
| redirect| Trigger | message          | Redirects to a 4chan board on >>>/ASD/| No    | >>>/g/            |
| say     | Command | say              | Put words in the bot's mouth          | No    | :say hello world  |
| shout   | Tigger  | message          | Shouts something random               | No    | HELLO WORLD       |
| smile   | Trigger | message          | Prints a random smiley                | No    | smile             |
| translate| Command| tr               | Translates text                       | No    | :tr {from auto} {to english} hello world |
| undress | Command | undress          | Prints a link to the current source   | No    | :undress          |
| urlinfo | Trigger | message          | Prints info about posted urls         | No    | http://example.com/ |
| urlminify| Command| minify           | Minifies the last posted url          | No    | :minify           |
| weather | Command | weather          | Displays weather info                 | No    | :weather new york |
| wolfram | Command | wa               | Executes a Wolfram Alpha query        | No    | :wa wine in france|
| youtube | Trigger | message          | Displays youtube video info           | No    | \*youtube link\*  |


TODO
======
* fix db's not being created properly
* make a db manager
