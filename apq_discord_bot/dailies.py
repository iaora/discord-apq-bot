from apq_discord_bot import db, client
from apq_discord_bot.helper import *
#from firebase_admin.firestore import SERVER_TIMESTAMP
import time

dailies = ['apq', 'shao', 'krex', 'zak', 'auf', 'dojo']

"""
	Takes in <PQ TYPE> and a list of IGNS as params

	Parses through all IGNS in the list and adds a field into the character's document with:
		<PQ TYPE> : SERVER_TIMESTAMP

		Ex: in document 'xuri', this field is added
			'apq' : 'Oct 3, 10:34:23 AM UTC'
"""
def log_daily(pq_type, ign_list):
	# Verify it's a correct daily
	if pq_type.lower() not in dailies:
		return (f'Incorrect boss type. Please enter one of the following: {dailies}')
		
	chars_c = db.collection('characters')
	for ign in ign_list:
		log_single_daily(chars_c, pq_type, ign.lower())

	return (f'Logged {pq_type} for {ign_list}')


def log_single_daily(chars_c, pq_type, ign):
	tar_doc_id = find_single_doc_id(chars_c, 'ign', ign)

	chars_c.document(tar_doc_id).update(
		{pq_type : time.gmtime()}
	)

"""
	

"""
def query_dailies(command_list, author_name):
	# If parsing through $daily <IGN>
	if (len(command_list) == 1 and 
			get_user_or_char(command_list[0].lower()) == 'characters'):
		return query_character(command_list[0].lower())

	# If parsing through $daily <DAILY> or $daily <DAILY> <USER>
	print('User daily query')
	# Verify it's a correct daily
	if command_list[0] not in dailies:
		return (f'Incorrect boss type. Please enter one of the following: {dailies}')

	daily_type = command_list[0].lower()
	user_name = author_name
	name_type = 'discord_user'
	if len(command_list) == 2:
		user_name = command_list[1].lower()
		name_type = 'name'
	print(f'{daily_type}')
	print(f'{user_name}')
	query_user_daily(daily_type, user_name, name_type)



# NOT DONE YETTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
def query_user_daily(daily_type, user_name, name_type):
	#ref = ('/users/156976596987674624')
	ref = db.collection('users').where(name_type, '==', user_name).get()
	#import pdb; pdb.set_trace()
	chars_list = db.collection('characters').where('user', '==', ref[0])



"""
	Takes in a character's ign (in lower case) and finds all relevant bosses that were run in today's reset by comparing GMT times to current GMT time and logged time. 
"""
def query_character(target):
		print('Character query')
		target_char = db.collection('characters').where('ign', '==', target).get()[0]

		target_dailies = []
		time_log = None
		for daily in dailies:
			try:
				time_log = target_char.get(daily)
			except KeyError:
				continue
			gmt_now = time.gmtime()
			if (gmt_now[0] == time_log[0] and 
					gmt_now[1] == time_log[1] and 
					gmt_now[2] == time_log[2]):
				target_dailies.append(daily)

		return (f'{target} has ran {target_dailies} today')
	

#return the correct collection to parse
def get_user_or_char(target): 
	user_or_chars = 'characters'
	ref = db.collection(user_or_chars)
	try:
		find_single_doc_id(ref, 'ign', target)
	except IndexError:
		user_or_chars = 'users'

	return user_or_chars
