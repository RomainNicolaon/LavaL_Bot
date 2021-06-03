import os
from re import S, purge
import ssl
import discord
from discord import channel

from discord.ext import commands

async def is_owner(ctx):
	return ctx.author.id == 405414058775412746

class Admin(commands.Cog, name="admin", command_attrs=dict(hidden=True)):
	"""Admin description"""
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='reloadall', aliases=['rell', 'relall'])
	@commands.check(is_owner)
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
	@commands.check(is_owner)
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

	@commands.command(name='killloop', aliases=['kill'], require_var_positional=True)
	@commands.check(is_owner)
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
		await ctx.send("All channels named `"+str(channel_name)+"` as been succesfuly deleted")
  
	@commands.command(name="deletemessage", aliases=['dm'])
	@commands.check(is_owner)
	async def delete_message(self, ctx, number: int):
		messages = await ctx.channel.history(limit=number + 1).flatten()
		for each_message in messages:
			await each_message.delete()

	@commands.command(name="clear")
	@commands.check(is_owner)
	async def clear(self, ctx, amount=10):
		await ctx.channel.purge(limit=amount)

	@reload_all_cogs.error
	async def reload_all_cogs_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('Error, you are not authorized to type that !')
		else:
			await ctx.send('Error')
		await ctx.message.add_reaction(emoji='❌')

	@reload_cogs.error
	async def reload_cogs_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('Please specify which cogs')
		elif isinstance(error, commands.CheckFailure):
			await ctx.send('Error, you are not authorized to type that !')
		else:
			await ctx.send('Error, check the argument(s) provided')
		await ctx.message.add_reaction(emoji='❌')
	
	

def setup(bot):
	bot.add_cog(Admin(bot))
