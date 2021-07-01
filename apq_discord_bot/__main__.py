from apq_discord_bot import db, client

from apq_discord_bot.db_helper import *
from apq_discord_bot.users_and_chars import *
from apq_discord_bot.dailies import *
from apq_discord_bot.image_ocr import *
import apq_discord_bot.owl as owl

from keys import discord_token

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	url = 'https://media.discordapp.net/attachments/848937705114304572/857474691266248744/unknown.png'
	#owl.add_owl_screenshot(url)

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('$hello'):
		await message.channel.send('Hello!')
	
	if message.attachments:
		print ('Attachment woooooooooooooo')
		# check if correct channel
		item_name = owl.add_owl_screenshot(message.attachments[0].url)
		await message.channel.send('{} added!'.format(item_name))	
	#messages.attachments[0].url

	"""------------------ OWL BOT -------------------"""
	if message.content.startswith('$get price'):
		import datetime
		command_list = str_remove_command(message, '$get price')
		item_info = owl.get_item_info(command_list)
		if not item_info:
			result = 'Error: Could not find item'
		else:
			result = '**{}**\n>>> Avg Price: {}\nMin Price: {}\nMax Price: {}\nMedian Price: {}\nLast updated: {}'.format(
			item_info['item_name'], 
			format(item_info['avg'],','),
			format(item_info['min'],','),
			format(item_info['max'],','),
			format(item_info['median'],','),
			item_info['update_date'].strftime('%m-%d-%y'))

		await message.channel.send(result)	


	"""------------------ APQ BOT -------------------"""
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
		await message.channel.send('```\n Add a new char: $add char <IGN> <CLASS> <BR/GR>\n Add your name: $add name <NAME>\n Remove a character: $remove <IGN>\n \n Log a new daily: $log <PQ/BOSS> <IGN> (optional: <IGN> <IGN>)```')

	
client.run(discord_token)
