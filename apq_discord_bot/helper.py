from apq_discord_bot import db, client


# ------------------------ HELPER METHODS ----------------------------------
def db_print(collection):
	docs = db.collection(collection).stream()

	for doc in docs:
	    print(f'{doc.id} => {doc.to_dict()}')
	# doc.to_dict()['Iaora']['user_id'].get().get('jamie')
	# Gets a user_id reference from Characters

def str_remove_command(message, command):
	return message.content[len(command)+1:]

