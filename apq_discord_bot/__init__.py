from keys import project_id#, discord_token

import discord
from google.cloud import firestore

# Project ID is determined by the GCLOUD_PROJECT environment variable
db = firestore.Client()

# initiaiate Discord
client = discord.Client()
