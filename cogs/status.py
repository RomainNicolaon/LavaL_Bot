import asyncio
import discord

from discord.ext import commands

class Status(commands.Cog, name="status"):
	"""Status description"""
	def __init__(self, bot):
		self.bot = bot
		self.task_change_status = self.bot.loop.create_task(self.loop_change_status())

	def return_loop_task(self):
		return self.task_change_status

	async def loop_change_status(self):
		await self.bot.wait_until_ready()
		status_message, reset = ["?help", "?infos", "?+ | ?- | ?_", "new ?spotify", "new ?join", "new ?play {URL}", "new ?tictactoe"], 0
		while not self.bot.is_closed():
			await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=status_message[reset], url='https://www.twitch.tv/laval_tv'), status=discord.Status.online, afk=False)
			await asyncio.sleep(10)
			if reset >= len(status_message)-1: reset = 0
			else: reset += 1

def setup(bot):
	bot.add_cog(Status(bot))
