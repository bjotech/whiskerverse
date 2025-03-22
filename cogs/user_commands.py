# cogs/user_commands.py
import discord
from discord.ext import commands
from discord import app_commands

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="user_test", description="Test command for template")
    async def user_test(self, interaction: discord.Interaction):

        # Send response message
        await interaction.response.send_message("User test command recieved")

async def setup(bot):
    await bot.add_cog(UserCommands(bot))