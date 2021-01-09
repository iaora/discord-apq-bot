from apq_discord_bot import db, client

from apq_discord_bot.helper import *
from apq_discord_bot.users_and_chars import *
from apq_discord_bot.dailies import *
from apq_discord_bot.image_ocr import *

from keys import discord_token

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('$hello'):
		await message.channel.send('Hello!')
	
	if message.attachments[0]:
		print ('Attachment woooooooooooooo')
		accept_image(message.attachments[0])
	#messages.attachments[0].url

	"""
		EXPECTED COMMAND:
			$add char <IGN> <CLASS> <BR/GR>
	"""
	if message.content.startswith('$add char'):
		command_list = str_remove_command(message, '$add char').split()
		# Check if the number of variables is correct 
		if len(command_list) != 3:
			await message.channel.send('```Incorrect number of arguments. Command is: $add char <IGN> <CLASS> <BR/GR>```')
		else:
			await message.channel.send('```'+add_char(command_list, message.author)+'```')



	"""
		EXPECTED COMMAND:
			$add name <NAME>
	"""
	if message.content.startswith('$add name'):
		command_list = str_remove_command(message, '$add name').split()
		# Check if the number of variables is correct 
		if len(command_list) != 1:
			await message.channel.send('```Incorrect number of arguments. Command is: $add user <NAME>```')
		else:
			await message.channel.send('```'+add_name(message.author.name.lower(), command_list[0].lower())+'```')



	"""
		EXPECTED COMMAND:
			$remove char <IGN>
	"""
	if message.content.startswith('$remove char'):
		command_list = str_remove_command(message, '$remove char').split()
		# Check if the number of variables is correct 
		if len(command_list) != 1:
			await message.channel.send('```Incorrect number of arguments. Command is: $remove char <IGN>```')
		else:
			await message.channel.send('```'+remove_char(command_list[0])+'```')
	


	"""
		EXPECTED COMMAND:
			$log <PQ TYPE> <IGN> (<IGN> <IGN> ...)

		Can handle adding a single IGN or multiple IGNs WITHOUT a comma
	"""
	if message.content.startswith('$log'):
		command_list = str_remove_command(message, '$log').split()
		# Check if the number of variables is correct 
		await message.channel.send('```'+log_daily(command_list[0].lower(), command_list[1:])+'```')
			

	"""
		EXPECTED COMMAND:
			$daily <IGN>, or
			$daily <DAILY>, or
			$daily <DAILY> <USER>

		Returns the timestamps of all bosses for a specific character
	"""
	if message.content.startswith('$daily'):
		command_list = str_remove_command(message, '$daily').split()
		# Check if the number of variables is correct 
		if len(command_list) > 2:
			await message.channel.send('```Incorrect number of arguments. Command is: $daily <IGN> or $daily <BOSS> or $daily <BOSS> <USER>```')
		else:
			await message.channel.send('```'+query_dailies(command_list, message.author.name.lower())+'```')
	

	if message.content.startswith('$help'):
		await message.channel.send('```\n Add a new char: $add char <IGN> <CLASS> <BR/BR>\n Add your name: $add name <NAME>\n Remove a character: $remove <IGN>\n \n Log a new daily: $log <PQ/BOSS> <IGN> (optional: <IGN> <IGN>)```')

	

client.run(discord_token)
