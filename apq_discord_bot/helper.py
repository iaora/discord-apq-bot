from apq_discord_bot import db, client

def db_print(collection):
	docs = db.collection(collection).stream()

	for doc in docs:
	    print(f'{doc.id} => {doc.to_dict()}')
	# doc.to_dict()['Iaora']['user_id'].get().get('jamie')
	# Gets a user_id reference from Characters

def str_remove_command(message, command):
	return message.content[len(command)+1:]


def add_char(command_list, message):
	command_list[0] = command_list[0].lower()
	print('Adding character...')
	# Check if user exists. If not, add a new user
	users_c = db.collection('users')
	if check_doc_exists(users_c, str(message.author.id)) is False:
		print ('Adding new user')
		# add_user(users_c, str(message.author.id), str(message.author.name))
	# Check if character exists 
	characters_c = db.collection('characters')
	if check_doc_exists(characters_c, command_list[0]) is True:
		return (f'{command_list[0]} already exists!')

	data = {
		'class' : command_list[1],
		'user' : db.collection('users').document(str(message.author.name))
	}

	db.collection('characters').document(command_list[0].lower()).set(data)
	#import pdb; pdb.set_trace()
	return (f'Added a new character: {command_list[0]}')



def check_doc_exists(collection, name):
	print (f'Checking if {name} exists in {collection}')
	return collection.document(name).get().exists
	

def add_user(users_coll, discord_author_id, discord_author_name):
	data = {
		'discord_user' : discord_author_name,
	}
	users_coll.document(discord_author_id).set(data)
	print ('f {data} added into document {discord_author_id}')


def query_example():
	# Create a reference to the cities collection
	cities_ref = db.collection(u'cities')

	# Create a query against the collection
	query_ref = cities_ref.where(u'state', u'==', u'CA')
