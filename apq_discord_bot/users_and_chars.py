from apq_discord_bot import db, client
from apq_discord_bot.db_helper import *


def remove_char(ign):
	print('Removing Character...')
	chars_c = db.collection('characters')
	target_doc_id = chars_c.where('ign', '==', ign).get()[0].id

	chars_c.document(target_doc_id).delete()

	return (f'Deleted {ign} successfully')

"""
@params:
	command_list - 
		list of character attributes to add, excluding the initial '$add char' substring
		ex: ['iaora', 'i/l']

	author_info - 
		an object containing the ID and Name of the sender of the discord message
		ex: ID - 156976596987674624
				Name - 'Iaora'

This function checks if the user exists. If not, it creates a new user in the 'users' collection. Simiarly, it first checks if the character being added is already added in the 'characters' collection. If not, then it add a new document to the collection. 

@returns:
	A message to send to Discord to announce success of creation or 

"""
def add_char(command_list, author_info):
	print('Adding character...')
	# Check if user exists. If not, add a new user
	users_c = db.collection('users')
	if check_doc_exists(users_c, str(author_info.id)) is False:
		print ('Adding new user')
		add_user(users_c, str(author_info.id), str(author_info.name.lower()))

	# Check if character exists 
	characters_c = db.collection('characters')
	if check_doc_exists(characters_c, command_list[0]) is True:
		return (f'{command_list[0]} already exists!')

	# If the user exists and the character does NOT exist, then create a new character document in the users collection
	data = {
		'ign' : command_list[0].lower(),
		'class' : command_list[1].lower(),
		'apq_type' : command_list[2].lower(),
		'user' : db.collection('users').document(str(author_info.id))
	}

	db.collection('characters').document(command_list[0].lower()).set(data)
	#import pdb; pdb.set_trace()
	return (f'Added a new character: {command_list[0]}')



def add_user(users_coll, discord_author_id, discord_author_name):
	data = {
		'discord_user' : discord_author_name,
		'discord_id' : discord_author_id,
	}
	users_coll.document(discord_author_id).set(data)
	print (f' {data} added into document {discord_author_id}')


def add_name(discord_author_name, name):
	tar_doc_id = find_single_doc_id(db.collection('users'), 'discord_user', discord_author_name)
	db.collection('users').document(tar_doc_id).update(
		{'name' : name}
	)

	return(f'Added {name}')
