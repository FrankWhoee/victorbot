![](logo.svg)
# victorbot
Multi-function bot that can manage voice channel movement and also acts as a soundboard. Also keeps track of server social credit. More features incoming, check out our [Projects tab](https://github.com/users/FrankWhoee/projects/7).

## Prerequisites
VictorBot runs on python3.8 so that we can use discord.py latest. The installation will not work with lower versions.
* Install [python3.8](https://wiki.python.org/moin/BeginnersGuide/Download)
* Install [pip](https://pip.pypa.io/en/stable/installation/)
* Install [virtualenv](https://pypi.org/project/virtualenv/)
* Install [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Installation
1. `git clone git@github.com:FrankWhoee/victorbot.git`
2. `cd victorbot`
3. `python3.8 -m venv venv`
4. `source venv/bin/activate`
5. `pip install -r requirements.txt`
6. `git submodule init`
7. `git submodule update`
8. `cd discord.py`
9. `pip install -U .`
10. `cd ..`
11. `echo "discord=YOURTOKEN" > .env`
    * Replace YOURTOKEN with your discord bot token from [the Discord Developer Portal](https://discord.com/developers/applications)
12. To run: `python main.py`
