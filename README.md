FutSniper
=========
##What does it do?
It scans the market for the players you choose for any profitable cards. If it finds one, it buys it for you.
##Set up
You need to create a file named `account.ini` where you have to set your settings:
```
EMAIL==youremail@mail.com
PASSWORD==yourpassword123
SECRET==the fut secret question
THRESHOLD==profit percent (the more the less likely you are to find something)
PLATFORM==pc
```
You will have to create another file named `watchlist.ini` where you store your players.
```
Gareth Bale##173731
Luis Suarez##176580
```
The structure is the next:
```
Player Name##assetID
```
Then execute futsniper.py and you're set.
