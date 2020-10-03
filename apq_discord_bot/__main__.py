from apq_discord_bot import db, client

from apq_discord_bot.helper import *
from apq_discord_bot.users_and_chars import *

from keys import discord_token

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('$hello'):
		db_print('users')


		await message.channel.send('Hello!')
	

	if message.content.startswith('$add char'):
		command_list = str_remove_command(message, '$add char').split()
		# Check if the number of variables is correct 
		if len(command_list) != 3:
			await message.channel.send('```Incorrect number of arguments. Command is: $add char <IGN> <CLASS> <BR/GR>```')
		else:
			await message.channel.send('```'+add_char(command_list, message.author)+'```')

	
	if message.content.startswith('$remove char'):
		command_list = str_remove_command(message, '$remove char').split()
		# Check if the number of variables is correct 
		if len(command_list) != 1:
			await message.channel.send('```Incorrect number of arguments. Command is: $remove char <IGN>```')
		else:
			await message.channel.send('```'+remove_char(command_list[0])+'```')
			

client.run(discord_token)
