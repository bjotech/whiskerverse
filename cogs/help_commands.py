import discord
from discord import app_commands
from discord.ext import commands

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Remove default help command
        bot.remove_command('help')
    
    @app_commands.command(name="help", description="View information about Whiskerverse commands")
    @app_commands.describe(category="Optional category to view specific commands")
    async def help(self, interaction: discord.Interaction, category: str = None):
        """Shows help about Whiskerverse commands and categories"""
        try:
            # Defer the response immediately to prevent timeout
            await interaction.response.defer()
            await self._show_help(interaction, category)
        except Exception as e:
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        f"An error occurred while showing help: {str(e)}",
                        ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        f"An error occurred while showing help: {str(e)}",
                        ephemeral=True
                    )
            except Exception:
                # If we can't send any response, just log the error
                print(f"Failed to send error message: {str(e)}")

    @commands.command(name="help", description="View information about Whiskerverse commands")
    async def legacy_help(self, ctx, category: str = None):
        """Legacy help command for non-slash command support"""
        class LegacyInteraction:
            def __init__(self, ctx):
                self.ctx = ctx
                self.response = self.Response(ctx)
                self._followup = self.Response(ctx)  # Create a separate response object for followup
            
            @property
            def followup(self):
                return self._followup

            class Response:
                def __init__(self, ctx):
                    self.ctx = ctx
                    self._deferred = False
                    self._done = False

                async def send_message(self, embed=None, content=None, ephemeral=False, **kwargs):
                    self._done = True
                    if content and embed:
                        return await self.ctx.send(content=content, embed=embed, **kwargs)
                    elif content:
                        return await self.ctx.send(content=content, **kwargs)
                    else:
                        return await self.ctx.send(embed=embed, **kwargs)
                
                async def defer(self, ephemeral=False):
                    self._deferred = True
                    # For legacy commands, we don't need to actually defer
                    pass
                
                def is_done(self):
                    return self._done or self._deferred
                
                async def edit_message(self, **kwargs):
                    # For legacy commands, edit_message is the same as send_message
                    return await self.send_message(**kwargs)

        interaction = LegacyInteraction(ctx)
        try:
            await self._show_help(interaction, category)
        except Exception as e:
            await ctx.send(f"An error occurred while showing help: {str(e)}", ephemeral=True)

    async def _show_help(self, interaction, category: str = None):
        """Internal method to show help that works with both slash and legacy commands"""
        try:
            categories = {
                "getting_started": {
                    "name": "🌟 Getting Started",
                    "description": "Begin your adventure in Whiskerverse!",
                    "commands": [
                        ("/start", "Create your profile and get your first cat"),
                        ("/help", "View information about commands and gameplay"),
                        ("/profile", "View your player profile and stats")
                    ]
                },
                "cats": {
                    "name": "🐱 Cat Management",
                    "description": "Commands for managing your cat collection",
                    "commands": [
                        ("/cats", "View all cats in your collection"),
                        ("/switch_cat", "Change your active cat for battles"),
                        ("/rename_cat", "Give your cat a new name"),
                        ("/encounter", "Look for wild cats to catch")
                    ]
                },
                "locations": {
                    "name": "🗺️ Exploration",
                    "description": "Explore the magical world of Whiskerverse",
                    "commands": [
                        ("/explore", "Explore your current location (Coming Soon)"),
                        ("/travel", "Travel to a different location (Coming Soon)"),
                        ("/map", "View the world map (Coming Soon)")
                    ]
                },
                "battles": {
                    "name": "⚔️ Battles",
                    "description": "Train and battle with your cats",
                    "commands": [
                        ("/battle", "Challenge another player to a battle (Coming Soon)"),
                        ("/train", "Train your active cat (Coming Soon)"),
                        ("/moves", "View your cat's available moves (Coming Soon)")
                    ]
                },
                "inventory": {
                    "name": "🎒 Inventory & Crafting",
                    "description": "Manage your items and craft equipment",
                    "commands": [
                        ("/inventory", "View your inventory (Coming Soon)"),
                        ("/craft", "Craft items from materials (Coming Soon)"),
                        ("/shop", "Visit the Whiskerton Market (Coming Soon)")
                    ]
                }
            }
            
            if category and category.lower() in categories:
                # Show specific category
                cat_info = categories[category.lower()]
                embed = discord.Embed(
                    title=cat_info["name"],
                    description=cat_info["description"],
                    color=discord.Color.blue()
                )
                
                for cmd, desc in cat_info["commands"]:
                    embed.add_field(name=cmd, value=desc, inline=False)
                
            else:
                # Show main help menu
                embed = discord.Embed(
                    title="Welcome to Whiskerverse! 🐱",
                    description="An immersive cat-collecting adventure where you explore, battle, and become legendary!",
                    color=discord.Color.blue()
                )
                
                # Add each category
                for cat_id, cat_info in categories.items():
                    embed.add_field(
                        name=cat_info["name"],
                        value=f"{cat_info['description']}\nUse `/help {cat_id}` for details",
                        inline=False
                    )
                
                # Add tips section
                embed.add_field(
                    name="📝 Quick Tips",
                    value="• Use `/start` to begin your adventure\n"
                          "• Each command has detailed help - use `/help category_name`\n"
                          "• Your active cat is used for battles and encounters\n"
                          "• Different locations have different types of cats to find",
                    inline=False
                )
            
            embed.set_footer(text="🌟 New features coming soon! Stay tuned for updates!")
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        f"An error occurred while showing help: {str(e)}",
                        ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        f"An error occurred while showing help: {str(e)}",
                        ephemeral=True
                    )
            except Exception:
                # If we can't send any response, just log the error
                print(f"Failed to send error message: {str(e)}")

async def setup(bot):
    await bot.add_cog(HelpCommands(bot)) 