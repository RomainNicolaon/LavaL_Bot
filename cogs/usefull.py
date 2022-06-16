import discord
import asyncio

from datetime import datetime, timedelta

from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from classes.discordbot import DiscordBot

class Usefull(commands.Cog, name="usefull"):
	"""
		Commandes utiles pour les développeurs et autres.

		Require intents:
			- message_content
		
		Require bot permission:
			- send_messages
	"""
	def __init__(self, bot: DiscordBot) -> None:
		self.bot = bot

	def help_custom(self) -> tuple[str, str, str]:
		emoji = '🚩'
		label = "Usefull"
		description = "Usefull commands."
		return emoji, label, description

	@app_commands.command(name="reminder", description="Vous rappeller quelque chose.")
	@app_commands.describe(hours="Hours.", minutes="Minutes.", seconds="Seconds.", message="Votre message à vous rappeler.")
	@app_commands.choices(hours=[Choice(name=i, value=i) for i in range(0, 25)], minutes=[Choice(name=i, value=i) for i in range(0, 56, 5)], seconds=[Choice(name=i, value=i) for i in range(5, 56, 5)])
	@app_commands.checks.bot_has_permissions(send_messages=True)
	async def reminder(self, interaction: discord.Interaction, hours: int, minutes: int, seconds: int, message: str) -> None:
		"""Reminds you of something."""
		remind_in = round(datetime.timestamp(datetime.now() + timedelta(hours=hours, minutes=minutes, seconds=seconds)))
		await interaction.response.send_message(f"Your message will be sent <t:{remind_in}:R>.")
		
		await asyncio.sleep(seconds+minutes*60+hours*(60**2))
		await interaction.channel.send(f":bell: <@{interaction.user.id}> Reminder (<t:{remind_in}:R>): {message}")

	@app_commands.command(name="strawpoll", description="Créez un sondage.")
	@app_commands.describe(question="La question du sondage.")
	async def avatar(self, interaction: discord.Interaction, question: str):
		await interaction.response.send_message(content=f"__*{interaction.user.mention}*__ : {question}", allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False))
		message = await interaction.original_message()
		await message.add_reaction("<a:yes_animated:844992841938894849>")
		await message.add_reaction("<a:no_animated:844992804480352257>")

	@app_commands.command(name="emojilist", description="Retourner une liste de chaque emojis cutom.")
	@commands.guild_only()
	async def avatar(self, interaction: discord.Interaction):
		"""Renvoie une liste de tous les emojis cutom du serveur actuel."""
		embed_list, embed = [], discord.Embed(title=f"Liste d'emojis personnalisés ({len(interaction.guild.emojis)}) :")
		for i, emoji in enumerate(interaction.guild.emojis, start=1):
			if i == 0 : 
				i += 1
			value = f"`<:{emoji.name}:{emoji.id}>`" if not emoji.animated else f"`<a:{emoji.name}:{emoji.id}>`"
			embed.add_field(name=f"{self.bot.get_emoji(emoji.id)} - **:{emoji.name}:** - (*{i}*)",value=value)
			if len(embed.fields) == 25:
				embed_list.append(embed)
				embed = discord.Embed()
		if len(embed.fields) > 0: 
			embed_list.append(embed)

		for message in embed_list:
			await interaction.response.send_message(embed=message)

async def setup(bot: DiscordBot):
	await bot.add_cog(Usefull(bot))
