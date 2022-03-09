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

from discord.ext.commands import bot

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

	@commands.command(name="reloadlatest", aliases=["rl"])
	@commands.is_owner()
	async def reload_latest(self, ctx):
		"""Reload the latest edited cog."""
		base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		cogs_directory = os.path.join(base_directory, "cogs")
		latest_cog = (None, 0)
		for file in os.listdir(cogs_directory):
			actual = os.path.splitext(file)
			if actual[1] == ".py":
				file_path = os.path.join(cogs_directory, file)
				latest_edit = os.path.getmtime(file_path)
				if latest_edit > latest_cog[1]: latest_cog = (actual[0], latest_edit)

		try:
			victims = await self.reload_cogs([f"cogs.{latest_cog[0]}"])
		except commands.ExtensionError as e:
			await ctx.send(f"{e.__class__.__name__}: {e}")
		else:
			await ctx.send(f"🤘 {latest_cog[0]} reloaded ! | ☠️ __`{len(victims)} task killed`__ | 🔄 __`view(s) reloaded`__")

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

	@commands.command(name="ads")
	@commands.is_owner()
	async def ads(self, guild, ctx):
		my_channel = self.get_channel(840003378062557202)
		annonce_channel = 'moderator-only'
		if annonce_channel is not None:
			await annonce_channel.send(ctx)
			await my_channel.send("L'annonce a bien été envoyé")
		else:
			if guild.system_channel is not None:
				await annonce_channel.send(ctx)
				await my_channel.id.send("L'annonce a bien été envoyée")

	@commands.command(name="changeprefix", aliases=["cp"])
	@commands.has_guild_permissions()
	async def change_guild_prefix(self, ctx, new_prefix):
		"""Change the guild prefix."""
		try:
			exist = await self.bot.database.exist(self.bot.database_data["prefix"]["table"], "*", f"guild_id={ctx.guild.id}")
			if exist:
				await self.bot.database.update(self.bot.database_data["prefix"]["table"], "guild_prefix", new_prefix, f"guild_id={ctx.guild.id}")
			else:
				await self.bot.database.insert(self.bot.database_data["prefix"]["table"], {"guild_id": ctx.guild.id, "guild_prefix": new_prefix})

			self.bot.prefixes[ctx.guild.id] = new_prefix
			await ctx.send(f":warning: Le préfix a bien été changé pour `{new_prefix}`")
		except Exception as e:
			await ctx.send(f"Erreur : {e}")

def setup(bot):
	bot.add_cog(Admin(bot))
