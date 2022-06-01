import asyncio
import discord

from discord.ext import commands

class Status(commands.Cog, name="status"):
	"""Une boucle pour définir l'état actuel du bot."""
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

	def help_custom(self) -> tuple[str, str, str]:
		emoji = '🏷️'
		label = "Status"
		description = "Configurer le statut du bot."
		return emoji, label, description

	async def cog_load(self):
		self.task_change_status = self.bot.loop.create_task(self.loop_change_status())

	async def cog_unload(self):
		self.task_change_status.cancel()

	async def loop_change_status(self) -> None:
		await self.bot.wait_until_ready()
		status_message = self.bot.config["bot"]["bot_status"]
		while not self.bot.is_closed():
			for status in status_message:
				await self.bot.change_presence(
					activity=discord.Streaming(
						name=status, 
						url="https://www.twitch.tv/laval_tv"), 
					status=discord.Status.do_not_disturb
				)
				await asyncio.sleep(10)



async def setup(bot):
	await bot.add_cog(Status(bot))