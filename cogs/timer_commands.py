import discord
from discord import app_commands
from discord.ext import commands
from models.services.timer_service import TimerService
import json
import os

class TimerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timer_service = TimerService()
        # Load timer config from configs folder
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs', 'timers_config.json'), 'r') as f:
            config = json.load(f)
            self.timer_config = config["timers"]
            self.admin_id = config["players"]["admin_id"]
    
    def is_admin(self, user_id: int) -> bool:
        """Check if the user is an admin"""
        return user_id == self.admin_id
    
    @app_commands.command(name="timer_reset_all", description="[ADMIN] Reset all timer cooldowns for everyone")
    async def timer_reset_all(self, interaction: discord.Interaction):
        """Reset all timer cooldowns for all players"""
        try:
            # Check if user is admin
            if not self.is_admin(interaction.user.id):
                await interaction.response.send_message(
                    "❌ You don't have permission to use this command.",
                    ephemeral=True
                )
                return
            
            # Defer the response immediately to prevent timeout
            await interaction.response.defer()
            
            # Clear all timers from the database
            success = self.timer_service.reset_all_timers()
            
            if success:
                embed = discord.Embed(
                    title="✅ Timer Reset Complete",
                    description="All timer cooldowns have been reset for all players.",
                    color=discord.Color.green()
                )
                embed.add_field(
                    name="Actions Reset",
                    value="• Encounter timers\n• Train timers\n• All other action timers",
                    inline=False
                )
                embed.set_footer(text=f"Reset by {interaction.user.name}")
                
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(
                    "❌ Failed to reset timers. Please check the logs for errors.",
                    ephemeral=True
                )
            
        except Exception as e:
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        f"❌ An error occurred while resetting timers: {str(e)}",
                        ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        f"❌ An error occurred while resetting timers: {str(e)}",
                        ephemeral=True
                    )
            except Exception:
                # If we can't send any response, just log the error
                print(f"Failed to send error message: {str(e)}")

async def setup(bot):
    await bot.add_cog(TimerCommands(bot))
