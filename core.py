import fut
"""
	TODO:
		>KeepAlive ping

"""

"""
VARIABLES
"""
fifa = None
loggedin = False

"""
SETTINGS FILE STRUCTURE
KEY==value
OBLIGATORY KEYS:
EMAIL - Your account email
PASSWORD - Your account password
SECRET - Your account secret word.
OPTIONAL:
PLATFORM - defaults to pc
"""
settings = {'PLATFORM': 'pc', 'EMAIL':'none', 'PASSWORD':'none', 'SECRET':'none'}
with open('account.ini', 'r') as options:
	for line in options.read().splitlines():
		line = line.split('==')
		settings[line[0]] = line[1]

def logIntoFut(code=''):
	global fifa, loggedin
	try:
		print 'Logging in . . .'
		fifa = fut.Core(settings['EMAIL'], settings['PASSWORD'], settings['SECRET'], platform=settings['PLATFORM'], cookies='cookies.txt', code=code)
		print 'FUT Client logged in.'
		loggedin = True
	except Exception as ex:
		if 'probably invalid email' in str(ex):
			print 'FUT Login Error: Invalid email or password.'
			quit()
		elif 'code is required' in str(ex):
			ourCode = raw_input('FUT Login Error: Code is required, please type it in:\n')	
			logIntoFut(ourCode)
		elif 'provided code is incorrect' in str(ex):
			ourCode = raw_input('FUT Login Error: Provided code is incorrect, please retype it:\n')
		else:
			print ex

def searchPlayer(playerid, min_price=0, max_price=15000000, min_buy=0, max_buy=15000000, page=0, pagesize=13):
	items = fifa.searchAuctions('player', assetId=int(playerid), min_price=min_price, max_price=max_price, min_buy=min_buy, max_buy=max_buy, start=page, page_size=pagesize)
	return items

def findLowestBin(playerid):
	items = searchPlayer(int(playerid), pagesize=26)
	cards = []
	for item in items:
		cards.append(item)
	orderedCards = sorted(cards, key=lambda k: k['buyNowPrice'])
	return orderedCards[0]

def findAverageBin(playerid):
	items = searchPlayer(int(playerid), pagesize=26)
	cards = []
	for item in items:
		cards.append(item['buyNowPrice'])
	return reduce(lambda x, y: x + y, cards) / len(cards)

def testMe():
	print 'It worked!'
	raw_input()

