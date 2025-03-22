import os
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from models import initialize_database

def get_discord_token():
    token = os.getenv('DISCORD_TOKEN')
    if token:
        return token
    
    try:
        secret_name = "prod/whiskerverse/token"
        region_name = "us-east-1"

        # Create a Secrets Manager client
        client = boto3.client('secretsmanager', region_name=region_name)

        # Retrieve the secret value
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)["DISCORD_TOKEN"]
    except (NoCredentialsError, PartialCredentialsError, client.exceptions.ResourceNotFoundException) as e:
        print(f"Error retrieving token: {e}")
        return None
    
def get_version():
    token = os.getenv('VERSION')
    if token:
        return token
    else:
        return "Version not specified"

load_dotenv()
token = get_discord_token()
if not token:
    raise ValueError("Discord bot token not found in environment variables or AWS Secrets Manager")

class MyBot(commands.Bot):
    async def setup_hook(self):
        # Initialize database tables
        initialize_database()
        
        # Load cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and filename != '__init__.py':
                await self.load_extension(f'cogs.{filename[:-3]}')
        await self.tree.sync()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = MyBot(command_prefix="/", intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    version = get_version()
    print(f'Whiskerverse is ready and {bot.user} is logged in. Verison: {version}')

bot.run(token)