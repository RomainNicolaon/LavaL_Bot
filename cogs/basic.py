import time
from classes.discordbot import DiscordBot
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
import discord

class Basic(commands.Cog, name="basic"):
	"""
		Des commandes de base, comme ping.

		Require intents: 
			- None
		
		Require bot permission:
			- send_messages
	"""
	def __init__(self, bot: DiscordBot) -> None:
		self.bot = bot

	def help_custom(self) -> tuple[str, str, str]:
		emoji = '📙'
		label = "Basic"
		description = "Des commandes de base, comme ping."
		return emoji, label, description

	@commands.hybrid_command(name="ping", description="Ping le bot.")
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.bot_has_permissions(send_messages=True)
	@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
	async def ping(self, ctx: commands.Context):
		"""Afficher la latence en secondes et millisecondess"""
		before = time.monotonic()
		message = await ctx.send(":ping_pong: Pong !")
		ping = (time.monotonic() - before) * 1000
		await message.edit(content=f":ping_pong: Pong ! en `{float(round(ping/1000.0,3))}s` ||{int(ping)}ms||")

	@app_commands.command(name="deletemessage", description="Supprime n message(s).")
	@app_commands.choices(number=[Choice(name=str(i), value=i) for i in range(1, 21)])
	@app_commands.checks.has_permissions(manage_messages=True)
	async def delete_message(self, interaction: discord.Interaction, number: int):
		await interaction.response.defer()
		await interaction.channel.purge(limit=number+1)

	@app_commands.command(name="clear", description="Supprime 10 messages.")
	@app_commands.checks.has_permissions(manage_messages=True)
	async def clear(self, interaction: discord.Interaction):
		"""Supprime 10 message"""
		await interaction.response.defer()
		await interaction.channel.purge(limit=11)


async def setup(bot: DiscordBot):
	await bot.add_cog(Basic(bot))