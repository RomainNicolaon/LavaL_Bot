import discord
import time
from discord.ext import commands
from discord import app_commands

class Random(commands.Cog, name="random"):
	"""
	Description des commandes pour le fun

	Require intents:
		- presences
	
	Require bot permission:
		- use_external_emojis
	"""

	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

	def help_custom(self) -> tuple[str, str, str]:
		emoji = '💊'
		label = "Random"
		description = "Commandes random pour déconner"
		return emoji, label, description

	@app_commands.command(name="jail", description="Direction la prison.")
	@app_commands.checks.bot_has_permissions(embed_links=True)
	async def hug(self, interaction: discord.Interaction, user: discord.Member = None):
		"""Direction la prison."""
		if not user:
			user = interaction.user

		pfp = user.display_avatar.url
		img = f"https://some-random-api.ml/canvas/jail?avatar={pfp}"
		embed = discord.Embed(title=f"{user.name} a été emmené à la prison.", color=0x00FF00)

		embed.set_image(url=img)

		embed.set_footer(text=f"Demandé par : {str(interaction.user.name)} à {time.strftime('%H:%M:%S')}", icon_url=interaction.user.display_avatar.url)

		await interaction.response.send_message(embed=embed)
   
async def setup(bot):
	await bot.add_cog(Random(bot))