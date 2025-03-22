import discord
from discord import app_commands
from discord.ext import commands
from models.services.cat_service import CatService
from models.services.player_service import PlayerService
import random

class CatCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cat_service = CatService()
        self.player_service = PlayerService()
    
    @app_commands.command(name="cats", description="View your cat collection")
    async def cats(self, interaction: discord.Interaction):
        """Display all cats owned by the player"""
        try:
            # Defer the response immediately to prevent timeout
            await interaction.response.defer()
            
            profile_data = self.player_service.get_profile(interaction.user.id)
            if not profile_data:
                await interaction.followup.send(
                    "You haven't started your adventure yet! Use `/start` to begin.",
                    ephemeral=True
                )
                return
            
            cats = profile_data['cats']
            if not cats:
                await interaction.followup.send(
                    "You don't have any cats yet! Use `/start` to get your first cat.",
                    ephemeral=True
                )
                return
            
            # Create paginated embeds for cats (5 cats per page)
            embeds = []
            for i in range(0, len(cats), 5):
                embed = discord.Embed(
                    title=f"{profile_data['player']['username']}'s Cats",
                    description=f"Page {i//5 + 1}/{(len(cats)-1)//5 + 1}",
                    color=discord.Color.blue()
                )
                
                for cat in cats[i:i+5]:
                    # Get rarity from breed
                    rarity = next(
                        rarity for rarity, breeds in self.cat_service.RARITY_WEIGHTS.items()
                        if cat['breed'] in breeds
                    )
                    
                    # Emoji based on rarity
                    rarity_emoji = {
                        'common': '⚪',
                        'uncommon': '🟢',
                        'rare': '🔵',
                        'epic': '🟣',
                        'legendary': '🟡'
                    }[rarity]
                    
                    active_status = "✨ Active" if cat['is_active'] else ""
                    
                    embed.add_field(
                        name=f"{rarity_emoji} {cat['name']} {active_status}",
                        value=f"ID: {cat['id']}\n"
                              f"Breed: {cat['breed']}\n"
                              f"Level: {cat['level']}\n"
                              f"Stats: ❤️ {cat['health']} | ⚔️ {cat['attack']} | "
                              f"🛡️ {cat['defense']} | 💨 {cat['speed']}",
                        inline=False
                    )
                
                embeds.append(embed)
            
            # Create pagination buttons
            class CatCollectionView(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=180)  # 3 minute timeout
                    self.current_page = 0
                    self.embeds = embeds
                
                @discord.ui.button(label="Previous", style=discord.ButtonStyle.secondary, disabled=True)
                async def previous_button(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                    try:
                        self.current_page = max(0, self.current_page - 1)
                        
                        # Update button states
                        self.children[0].disabled = self.current_page == 0  # Previous button
                        self.children[1].disabled = self.current_page == len(self.embeds) - 1  # Next button
                        
                        # Handle both legacy and slash command interactions
                        if hasattr(button_interaction, 'response'):
                            await button_interaction.response.edit_message(
                                embed=self.embeds[self.current_page],
                                view=self
                            )
                        else:
                            # For legacy interactions, edit the original message
                            await button_interaction.message.edit(
                                embed=self.embeds[self.current_page],
                                view=self
                            )
                    except Exception as e:
                        error_msg = f"An error occurred while navigating: {str(e)}"
                        if hasattr(button_interaction, 'response'):
                            await button_interaction.response.send_message(error_msg, ephemeral=True)
                        else:
                            await button_interaction.channel.send(error_msg)
                
                @discord.ui.button(label="Next", style=discord.ButtonStyle.secondary, disabled=len(embeds) <= 1)
                async def next_button(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                    try:
                        self.current_page = min(len(self.embeds) - 1, self.current_page + 1)
                        
                        # Update button states
                        self.children[0].disabled = self.current_page == 0  # Previous button
                        self.children[1].disabled = self.current_page == len(self.embeds) - 1  # Next button
                        
                        # Handle both legacy and slash command interactions
                        if hasattr(button_interaction, 'response'):
                            await button_interaction.response.edit_message(
                                embed=self.embeds[self.current_page],
                                view=self
                            )
                        else:
                            # For legacy interactions, edit the original message
                            await button_interaction.message.edit(
                                embed=self.embeds[self.current_page],
                                view=self
                            )
                    except Exception as e:
                        error_msg = f"An error occurred while navigating: {str(e)}"
                        if hasattr(button_interaction, 'response'):
                            await button_interaction.response.send_message(error_msg, ephemeral=True)
                        else:
                            await button_interaction.channel.send(error_msg)
                
                async def on_timeout(self):
                    try:
                        # Disable all buttons when the view times out
                        for child in self.children:
                            child.disabled = True
                        # Try to edit the message to disable buttons
                        message = await interaction.original_response()
                        await message.edit(view=self)
                    except discord.errors.NotFound:
                        # If the original message was deleted
                        pass
                    except Exception as e:
                        # Log any other errors
                        print(f"Error in on_timeout: {str(e)}")
                        pass
            
            # Send first page with navigation buttons
            await interaction.followup.send(
                embed=embeds[0],
                view=CatCollectionView()
            )
            
        except Exception as e:
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        f"An error occurred while fetching your cats: {str(e)}",
                        ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        f"An error occurred while fetching your cats: {str(e)}",
                        ephemeral=True
                    )
            except Exception:
                # If we can't send any response, just log the error
                print(f"Failed to send error message: {str(e)}")
    
    @app_commands.command(name="switch_cat", description="Switch your active cat")
    @app_commands.describe(cat_id="The ID of the cat you want to make active")
    async def switch_cat(self, interaction: discord.Interaction, cat_id: int):
        """Switch your active cat"""
        try:
            # Defer the response immediately to prevent timeout
            await interaction.response.defer()
            
            success, message = self.cat_service.switch_active_cat(
                cat_id=cat_id,
                player_id=interaction.user.id
            )
            
            if not success:
                await interaction.followup.send(message, ephemeral=True)
                return
            
            await interaction.followup.send(
                f"{message} 🐱",
                ephemeral=True
            )
            
        except Exception as e:
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        f"An error occurred while switching cats: {str(e)}",
                        ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        f"An error occurred while switching cats: {str(e)}",
                        ephemeral=True
                    )
            except Exception:
                # If we can't send any response, just log the error
                print(f"Failed to send error message: {str(e)}")
    
    @app_commands.command(name="rename_cat", description="Rename one of your cats")
    @app_commands.describe(
        cat_id="The ID of the cat you want to rename",
        new_name="The new name for your cat"
    )
    async def rename_cat(self, interaction: discord.Interaction, cat_id: int, new_name: str):
        """Rename a cat"""
        try:
            # Defer the response immediately to prevent timeout
            await interaction.response.defer()
            
            success, message = self.cat_service.rename_cat(
                cat_id=cat_id,
                player_id=interaction.user.id,
                new_name=new_name
            )
            
            await interaction.followup.send(
                f"{message} 🐱" if success else message,
                ephemeral=True
            )
            
        except Exception as e:
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        f"An error occurred while renaming your cat: {str(e)}",
                        ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        f"An error occurred while renaming your cat: {str(e)}",
                        ephemeral=True
                    )
            except Exception:
                # If we can't send any response, just log the error
                print(f"Failed to send error message: {str(e)}")
    
    @app_commands.command(name="encounter", description="Look for a cat to catch")
    async def encounter(self, interaction: discord.Interaction):
        """Find a random cat to catch"""
        try:
            # Defer the response immediately to prevent timeout
            await interaction.response.defer()
            
            profile_data = self.player_service.get_profile(interaction.user.id)
            if not profile_data:
                await interaction.followup.send(
                    "You haven't started your adventure yet! Use `/start` to begin.",
                    ephemeral=True
                )
                return
            
            # Get active cat
            active_cat = profile_data['active_cat']
            if not active_cat:
                await interaction.followup.send(
                    "You need an active cat to go on encounters! Use `/cats` to view your cats and `/switch_cat` to set one active.",
                    ephemeral=True
                )
                return
            
            # Generate a random cat based on location
            # TODO: Implement location-based rarity weights
            encountered_cat = self.cat_service.generate_random(
                player_id=None,  # No owner yet
                name="Wild Cat"
            )
            
            embed = discord.Embed(
                title="A Wild Cat Appears! 🐱",
                description="You've encountered a wild cat! What would you like to do?",
                color=discord.Color.gold()
            )
            
            embed.add_field(
                name="Wild Cat",
                value=f"Breed: {encountered_cat['breed']}\n"
                      f"Level: {encountered_cat['level']}\n"
                      f"Stats: ❤️ {encountered_cat['health']} | ⚔️ {encountered_cat['attack']} | "
                      f"🛡️ {encountered_cat['defense']} | 💨 {encountered_cat['speed']}",
                inline=False
            )
            
            # Create buttons for actions
            class EncounterView(discord.ui.View):
                def __init__(self, cat_service, player_data):
                    super().__init__(timeout=30)
                    self.cat_service = cat_service
                    self.player_data = player_data
                    self.encountered_cat = encountered_cat
                
                @discord.ui.button(label="Battle", style=discord.ButtonStyle.danger)
                async def battle(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                    # TODO: Implement battle system
                    await button_interaction.response.send_message(
                        "Battle system coming soon!",
                        ephemeral=True
                    )
                
                @discord.ui.button(label="Try to Catch", style=discord.ButtonStyle.primary)
                async def catch(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                    try:
                        # Calculate catch chance based on health percentage
                        catch_chance = 0.5  # Base 50% chance
                        
                        if random.random() < catch_chance:
                            # Success!
                            self.encountered_cat['player_id'] = self.player_data['player']['id']
                            self.encountered_cat['name'] = f"{self.player_data['player']['username']}'s {self.encountered_cat['breed']}"
                            self.cat_service.save_cat(self.encountered_cat)
                            
                            await button_interaction.response.send_message(
                                f"Success! You caught the {self.encountered_cat['breed']}! 🎉",
                                ephemeral=True
                            )
                        else:
                            await button_interaction.response.send_message(
                                "Oh no! The cat ran away! 😿",
                                ephemeral=True
                            )
                        
                        # Disable all buttons after an action
                        for child in self.children:
                            child.disabled = True
                        await interaction.edit_original_response(view=self)
                    except discord.errors.NotFound:
                        # If the original message was deleted or interaction expired
                        pass
                    except Exception as e:
                        await button_interaction.response.send_message(
                            f"An error occurred while catching the cat: {str(e)}",
                            ephemeral=True
                        )
                
                @discord.ui.button(label="Run", style=discord.ButtonStyle.secondary)
                async def run(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                    try:
                        await button_interaction.response.send_message(
                            "You ran away safely!",
                            ephemeral=True
                        )
                        
                        # Disable all buttons
                        for child in self.children:
                            child.disabled = True
                        await interaction.edit_original_response(view=self)
                    except discord.errors.NotFound:
                        # If the original message was deleted or interaction expired
                        pass
                    except Exception as e:
                        await button_interaction.response.send_message(
                            f"An error occurred: {str(e)}",
                            ephemeral=True
                        )
                
                async def on_timeout(self):
                    try:
                        # Disable all buttons when the view times out
                        for child in self.children:
                            child.disabled = True
                        await interaction.edit_original_response(view=self)
                    except discord.errors.NotFound:
                        # If the original message was deleted
                        pass
            
            await interaction.followup.send(
                embed=embed,
                view=EncounterView(self.cat_service, profile_data)
            )
            
        except Exception as e:
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        f"An error occurred during the encounter: {str(e)}",
                        ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        f"An error occurred during the encounter: {str(e)}",
                        ephemeral=True
                    )
            except Exception:
                # If we can't send any response, just log the error
                print(f"Failed to send error message: {str(e)}")

async def setup(bot):
    await bot.add_cog(CatCommands(bot)) 