from apq_discord_bot import db, client
from apq_discord_bot.helper import *
from firebase_admin.firestore import SERVER_TIMESTAMP

dailies = ['apq', 'shao', 'krex', 'zak', 'auf', 'dojo']

"""
	Takes in <IGN> and <PQ TYPE> as params

	Adds a field into the character's document with:
		<PQ TYPE> : SERVER_TIMESTAMP

		Ex: in document 'xuri', this field is added
			'apq' : 'Oct 3, 10:34:23 AM UTC'
"""
def log_daily(pq_type, ign_list):
	# Verify it's a correct daily
	if pq_type not in dailies:
		return (f'Incorrect boss type. Please enter one of the following: {dailies}')
		
	chars_c = db.collection('characters')
	for ign in ign_list:
		log_single_daily(chars_c, pq_type, ign)

	return (f'Logged {pq_type} for {ign_list}')


def log_single_daily(chars_c, pq_type, ign):
	tar_doc_id = find_single_doc_id(chars_c, 'ign', ign)

	chars_c.document(tar_doc_id).update(
		{pq_type : SERVER_TIMESTAMP}
	)


def query_dailies():
	print('test')
