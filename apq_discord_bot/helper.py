from apq_discord_bot import db, client


# ------------------------ HELPER METHODS ----------------------------------
def db_print(collection):
	docs = db.collection(collection).stream()

	for doc in docs:
	    print(f'{doc.id} => {doc.to_dict()}')
	# doc.to_dict()['Iaora']['user_id'].get().get('jamie')
	# Gets a user_id reference from Characters


# Removes the prefex from a command. Returns the important command fields
# Ex: '$add char xuri se br'  -->  ['xuri', 'se', 'br']
def str_remove_command(message, command):
	return message.content[len(command)+1:]


def find_single_doc_id(collection_ref, tar_field, tar_key):
	return collection_ref.where(tar_field, '==', tar_key).get()[0].id
