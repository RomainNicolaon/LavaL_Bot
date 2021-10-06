import os
from re import S, purge
import ssl
import discord
from discord import channel
import types
import sys
import os

from discord.ext import commands
from importlib import reload

class Admin(commands.Cog, name="admin", command_attrs=dict(hidden=True)):
	"""Admin description"""
	def __init__(self, bot):
		self.bot = bot

	def help_custom(self):
		emoji = '⚙️'
		label = "Admin"
		description = "Affiche la liste des commandes admin."
		return emoji, label, description

	async def reload_views(self):
		modules, infants = [], []
		for module in sys.modules.items():
			if isinstance(module[1], types.ModuleType):
				modules.append(module[1])

		for module in modules:
			try:
				if os.path.basename(os.path.dirname(module.__file__)) == "views":
					reload(module)
					infants.append(module.__name__)
			except: pass

		return infants

	async def reload_cogs(self, cogs):
		victims = []
		for cog in cogs:
			norm_cog = self.bot.get_cog(cog[5:len(cog)])
			if "return_loop_task" in dir(norm_cog): 
				norm_cog.return_loop_task().cancel()
				victims.append(cog)
			self.bot.reload_extension(cog)
		return victims

	@commands.command(name='reloadall', aliases=['rell', 'relall'])
	@commands.is_owner()
	async def reload_all_cogs(self, ctx):
		victim, victim_list, botCogs, safeCogs = 0, [], self.bot.extensions, []
		try:
			for cog in botCogs:
				safeCogs.append(cog)
			for cog in safeCogs:
				g_cog = self.bot.get_cog(cog[5:len(cog)])
				if "return_loop_task" in dir(g_cog): 
					g_cog.return_loop_task().cancel()
					victim += 1
					victim_list.append(cog)
				self.bot.reload_extension(cog)
		except commands.ExtensionError as e:
			await ctx.send(f'{e.__class__.__name__}: {e}')
		else:
			succes_text = ':muscle:  All cogs reloaded ! | __`' + str(victim) + ' task killed`__ : '
			for victims in victim_list:
				succes_text += "`"+str(victims).replace('cogs.', '')+"` "
			await ctx.send(succes_text)

	@commands.command(name='reload', aliases=['rel'], require_var_positional=True)
	@commands.is_owner()
	async def reload_cogs(self, ctx, cog):
		victim, cog, g_cog = 0, 'cogs.'+cog, self.bot.get_cog(cog)
		try:
			if "return_loop_task" in dir(g_cog):
				g_cog.return_loop_task().cancel()
				victim += 1
			self.bot.reload_extension(cog)
		except commands.ExtensionError as e:
			await ctx.send(f'{e.__class__.__name__}: {e}')
		else:
			await ctx.send(':metal: '+cog+' reloaded ! : __`' + str(victim) + ' task killed`__')

	@commands.command(name='reloadviews', aliases=['rmod', 'rview', 'rviews'])
	@commands.is_owner()
	async def reload_view(self, ctx):
		"""Reload each registered views."""
		try:
			infants = await self.reload_views()
		except commands.ExtensionError as e:
			await ctx.send(f'{e.__class__.__name__}: {e}')
		else:
			succes_text = '👌 All views reloaded ! | 🔄 __`'+str(len(infants))+' view(s) reloaded`__ : '
			for infant in infants: succes_text += "`"+str(infant).replace('views.', '')+"` "
			await ctx.send(succes_text)

	@commands.command(name='killloop', aliases=['kill'], require_var_positional=True)
	@commands.is_owner()
	async def kill_loop(self, ctx, cog):
		cogs = self.bot.get_cog(cog)
		if "return_loop_task" in dir(cogs):
			cogs.return_loop_task().cancel()
			await ctx.send("Task successfully killed")
		else : await ctx.send("Task not found..")

	@commands.command(name='deletechannel', aliases=['dc'], require_var_positional=True)
	@commands.has_permissions(manage_messages=True)
	async def delete_channel(self, ctx, channel_name):
		channel = discord.utils.get(ctx.guild.channels, name=channel_name)
		while channel:
			await channel.delete()
			channel = discord.utils.get(ctx.guild.channels, name=channel_name)
		await ctx.send("Tout les channels appelés `"+str(channel_name)+"` ont bien été supprimés")
  
	@commands.command(name="deletemessage", aliases=['dm'])
	@commands.is_owner()
	async def delete_message(self, ctx, number: int):
		messages = await ctx.channel.history(limit=number + 1).flatten()
		for each_message in messages:
			await each_message.delete()

	@commands.command(name="clear")
	@commands.is_owner()
	async def clear(self, ctx, amount=10):
		"""Supprime 10 message"""
		await ctx.channel.purge(limit=amount)

def setup(bot):
	bot.add_cog(Admin(bot))
