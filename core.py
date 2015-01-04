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

def searchPlayer(playerid, min_price=0, max_price=15000000, min_buy=0, max_buy=15000000, page=0):
	items = fifa.searchAuctions('player', assetId=int(playerid), min_price=min_price, max_price=max_price, min_buy=min_buy, max_buy=max_buy, start=page)
	return items

def findLowestBin(playerid):
	pass

"""
PROGRAM INITIALIZATION
"""
logIntoFut()

if loggedin:
	print 'You have:', fifa.credits, 'FIFA credits.'
	inp = ''
	while not inp == 'quit':
		inp = raw_input('Search for player: ')
		if not inp == 'quit':
			myCard = fifa.cardInfo(int(inp))['Item']
			print 'Looking for', myCard['FirstName'], myCard['LastName'], '. . .'
			with open('market.log', 'w') as log:
				trades = {}
				for item in searchPlayer(inp):
					trades[item['buyNowPrice']] = {'ID':item['tradeId'], 'Owner':item['sellerName']}
					log.write(str(item))
					log.write('\n'*5)
			print 'Lowest price is', str(min(trades)), 'sold by', trades[min(trades)]['Owner'] + '(' + str(trades[min(trades)]['ID']) + ')'
		else:
			break
