from os import name
import time
import discord

from discord.ext import commands


class Test(commands.Cog, name="test"):
	"""Basic description"""
	def __init__(self, bot):
		self.bot = bot
	
def setup(bot):
		bot.add_cog(Test(bot))
