import futcore
import time
import random
from time import strftime
from threading import Timer	
fifa = futcore.logIntoFut()
while str(type(fifa)) == "<type 'str'>" or not fifa:
	fifa = futcore.logIntoFut(fifa)

watchlist = []
"""
LOAD THE WATCHLIST
STRUCTURE:
Player Name##AssetID
ex:
Gareth Bale##173731
"""

def logAction(text):
	with open(strftime("%Y-%m-%d") + '-fifa.log', 'a') as ourLog:
		ourLog.write(text + '\n')

def updateWatchlist():
	global watchlist
	watchlist = []
	with open('watchlist.ini', 'r') as playas:
		for line in playas.read().splitlines():
			line = line.split('##')
			watchlist.append({'Player':line[0], 'ID':line[1]})
updateWatchlist()

def keepAlive():
	global fifa
	if fifa:
		fifa.keepalive()
		print 'Keeping alive..'
		Timer(120, keepAlive, ()).start()
keepAlive()

x = 0
while True:
	player = watchlist[x%len(watchlist)]
	print 'Monitoring', player['Player'], '. . .'
	lowestCards = futcore.findLowestBins(fifa, player['ID'])
	averageCost = futcore.findAverageBin(fifa, player['ID'])
	percent = 100-((lowestCards[0]['buyNowPrice'] / float(lowestCards[1]['buyNowPrice']))*100)
	averagePercent = 100-((lowestCards[0]['buyNowPrice'] / float(averageCost))*100)
	print 'Possible profit is', str(percent)[:4] + '%', 'since the cheapest is', lowestCards[0]['buyNowPrice'], 'and the second is', lowestCards[1]['buyNowPrice']
	print 'Average is ' + str(averageCost) + ' and its ' + str(averagePercent)[:4] + '% more costly.'
	entry =  "=====LOG ENTRY" + strftime("%H:%M:%S") + "=====\n"
	entry += "Inspected Player: " + player['Player'] + '\n'
	entry += "Prices: " + str(lowestCards[0]['buyNowPrice']) + "(lowest), " + str(lowestCards[1]['buyNowPrice']) + ', ' + str(lowestCards[2]['buyNowPrice']) + '\n'
	entry += "Threshold: " + futcore.settings['THRESHOLD'] +'\n'
	entry += "Enough?: " + str(percent >= int(futcore.settings['THRESHOLD'])) + '\n'
	entry += "Average price is " + str(averageCost) + ", it's " + str(averagePercent)[:4] + "% more costly"
	logAction(entry)
	if percent >= int(futcore.settings['THRESHOLD']) and averagePercent >= int(futcore.settings['THRESHOLD']) and lowestCards[0]['buyNowPrice'] > fifa.credits: #PROFIT!
		if futcore.checkLowerPrice(fifa, player['ID'], lowestCards[0]['buyNowPrice']):
			print 'Enough for me. BUYING!'
			entry =  ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
			entry += "BUYING PLAYER '" + player['Player'] + "'\n"
			entry += ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
			print entry
			logAction(entry)
			time.sleep(1 + random.randint(1, 4))
			futcore.buyPlayer(fifa, lowestCards[0]['trade_id'], lowestCards[0]['buyNowPrice'])
	else:
		print 'It\'s not enough. Sleeping...'
	x += 1
	updateWatchlist()
	time.sleep(int(futcore.settings['TIMER']) + random.randint(1, int(futcore.settings['RANDOMTIMER'])))