import discord
from discord import app_commands
from discord.ext import commands
from models.services.player_service import PlayerService

class PlayerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.player_service = PlayerService()
    
    @app_commands.command(name="start", description="Start your Whiskerverse adventure!")
    async def start(self, interaction: discord.Interaction):
        """Create a new player profile and get your first cat"""
        try:
            success, message, cat = self.player_service.start_adventure(
                discord_id=interaction.user.id,
                username=interaction.user.name,
                cat_name=f"{interaction.user.name}'s First Cat"
            )
            
            if not success:
                await interaction.response.send_message(
                    f"{message}! Use `/profile` to see your status.",
                    ephemeral=True
                )
                return
            
            # Create embed for response
            embed = discord.Embed(
                title="Welcome to Whiskerverse! 🐱",
                description="Your journey begins in the magical world of cats!",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="Your Profile",
                value=f"Level: 1\nCoins: 100\nLocation: Whiskerton",
                inline=False
            )
            
            embed.add_field(
                name="Your First Cat",
                value=f"Name: {cat['name']}\n"
                      f"Breed: {cat['breed']}\n"
                      f"Stats: ❤️ {cat['health']} | ⚔️ {cat['attack']} | "
                      f"🛡️ {cat['defense']} | 💨 {cat['speed']}",
                inline=False
            )
            
            embed.set_footer(text="Use /help to see all available commands!")
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            await interaction.response.send_message(
                f"An error occurred while starting your adventure: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(name="profile", description="View your Whiskerverse profile")
    async def profile(self, interaction: discord.Interaction):
        """Display player profile information"""
        try:
            profile_data = self.player_service.get_profile(interaction.user.id)
            if not profile_data:
                await interaction.response.send_message(
                    "You haven't started your adventure yet! Use `/start` to begin.",
                    ephemeral=True
                )
                return
            
            player = profile_data['player']
            active_cat = profile_data['active_cat']
            cats = profile_data['cats']
            inventory = profile_data['inventory']
            
            embed = discord.Embed(
                title=f"{player['username']}'s Profile",
                color=discord.Color.blue()
            )
            
            # Player stats
            embed.add_field(
                name="Player Stats",
                value=f"Level: {player['level']}\n"
                      f"Experience: {player['experience']}/{player['level'] * 1000}\n"
                      f"Coins: {player['coins']}\n"
                      f"Location: {player['current_location']}",
                inline=False
            )
            
            # Active cat
            if active_cat:
                embed.add_field(
                    name="Active Cat",
                    value=f"Name: {active_cat['name']}\n"
                          f"Breed: {active_cat['breed']}\n"
                          f"Level: {active_cat['level']}\n"
                          f"Stats: ❤️ {active_cat['health']} | ⚔️ {active_cat['attack']} | "
                          f"🛡️ {active_cat['defense']} | 💨 {active_cat['speed']}",
                    inline=False
                )
            
            # Cat collection
            cat_count = len(cats)
            embed.add_field(
                name="Cat Collection",
                value=f"Total Cats: {cat_count}",
                inline=False
            )
            
            # Inventory summary
            item_count = sum(item['quantity'] for item in inventory)
            embed.add_field(
                name="Inventory",
                value=f"Total Items: {item_count}",
                inline=False
            )
            
            embed.set_footer(text="Use /cats to see your cat collection and /inventory to see your items!")
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            await interaction.response.send_message(
                f"An error occurred while fetching your profile: {str(e)}",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(PlayerCommands(bot)) 