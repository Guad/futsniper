import fut
fifa = 0
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
	try:
		fifa = fut.Core(settings['EMAIL'], settings['PASSWORD'], settings['SECRET'], platform=settings['PLATFORM'], cookies='cookies.txt')
		print 'FUT Client logged in.'
	except Exception as ex:
		if 'probably invalid email' in ex:
			print 'FUT Login Error: Invalid email or password'
		elif 'code is required' in ex:
			ourCode = raw_input('FUT Login Error: Code is required, please type it in:\n')	
			logIntoFut(ourCode)
		elif 'provided code is incorrect' in ex:
			ourCode = raw_input('FUT Login Error: Provided code is incorrect, please retype it:\n')
