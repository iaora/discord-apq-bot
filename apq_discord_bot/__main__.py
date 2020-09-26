from apq_discord_bot import db, client
from apq_discord_bot.helper import *
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
		#add_char(command_info.split(), message)
		if len(command_list) != 2:
			await message.channel.send('Incorrect number of arguments. Command is: $add char <IGN> <CLASS>')
		else:
			await message.channel.send(add_char(command_list, message))

client.run(discord_token)
