import discord

from discord.ext import commands
from discord.ext.commands import errors

class Errors(commands.Cog, name="errors", command_attrs=dict(hidden=True)):
	"""Errors handler"""
	def __init__(self, bot):
		self.bot = bot

	"""def help_custom(self):
		emoji = '<a:crossmark:842800737221607474>'
		label = "Error"
		description = "A custom errors handler."
		return emoji, label, description"""

	@commands.Cog.listener('on_command_error')
	async def get_command_error(self, ctx, error):
		try:
			message = await ctx.send("💥 Une erreur s'est produite.")
			if isinstance(error, commands.errors.CommandNotFound):
				await message.edit("💥 La commande `"+str(error).split(' ')[1]+"` n'a pas été trouvée !")
			elif isinstance(error, commands.errors.NotOwner):
				await message.edit("💥 Vous devez posséder ce robot pour exécuter cette commande.")
			elif isinstance(error, commands.errors.CommandOnCooldown):
				await message.edit("💥 La commande est en rechargement, attendez `"+str(error).split(' ')[7]+"` !")
			elif isinstance(error, commands.errors.MissingRequiredArgument):
				command, params = ctx.command, ""
				for param in command.clean_params: params += " {"+str(param)+"}"
				await message.edit("💥 Il manque quelque chose. `?"+str(command)+str(params)+'`')
			elif isinstance(error, commands.errors.MemberNotFound):
				await message.edit("💥 Le membre `"+str(error).split(' ')[1]+"` n'a pas été trouvé ! N'hésite pas à envoyer un ping au membre demandé.")
			elif isinstance(error, commands.errors.MissingPermissions):
				await message.edit("💥 Cette commande nécessitent plus de permissions.")
			elif isinstance(error, commands.errors.DisabledCommand):
				await message.edit("💥 Cette commande est désactivé.")
			else:
				await message.edit("💥 `"+str(type(error).__name__)+"` : "+str(error))
			await ctx.message.add_reaction(emoji='<a:crossmark:842800737221607474>') #❌
		except:
			print("! Cog errors get_command_error : "+str(type(error).__name__)+" : "+str(error))

def setup(bot):
	bot.add_cog(Errors(bot))