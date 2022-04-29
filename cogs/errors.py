import discord

from discord.ext import commands
from discord import app_commands

class Errors(commands.Cog, name="errors"):
	"""Gestionnaire d'erreurs."""
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot
		bot.tree.error(coro = self.dispatch_to_app_command_handler)

		self.default_error_message = "🕳️ There is an error."

	"""def help_custom(self):
		emoji = "<a:no_animated:844992804480352257>"
		label = "Error"
		description = "Un gestionnaire d'erreurs personnalisé. Rien à voir ici."
		return emoji, label, description"""

	async def dispatch_to_app_command_handler(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
		self.bot.dispatch("app_command_error", interaction, error)

	async def __respond_to_interaction(self, interaction: discord.Interaction) -> bool:
		try:
			await interaction.response.send_message(self.default_error_message, ephemeral=True)
			return True
		except discord.errors.InteractionResponded:
			return False

	@commands.Cog.listener("on_error")
	async def get_error(self, event, *args, **kwargs):
		"""Error handler"""
		print(f"! Unexpected Internal Error: (event) {event}, (args) {args}, (kwargs) {kwargs}.")

	@commands.Cog.listener("on_command_error")
	async def get_command_error(self, ctx: commands.Context, error: commands.CommandError):
		"""Command Error handler
		doc: https://discordpy.readthedocs.io/en/master/ext/commands/api.html#exception-hierarchy
		"""
		try:
			if ctx.interaction: # HybridCommand Support
				await self.__respond_to_interaction(ctx.interaction)
				edit = ctx.interaction.edit_original_message
				if isinstance(error, commands.HybridCommandError):
					error = error.original # Access to the original error
			else:
				discord_message = await ctx.send(self.default_error_message, ephemeral=True)
				edit = discord_message.edit

			raise error

		# ConversionError
		except commands.ConversionError as d_error:
			await edit(content=f"🕳️ {d_error}")
		# UserInputError
		except commands.MissingRequiredArgument as d_error:
			await edit(content=f"🕳️ Il manque quelque chose.. `{ctx.clean_prefix}{ctx.command.name} <{'> <'.join(ctx.command.clean_params)}>`")
		# UserInputError -> BadArgument
		except commands.MemberNotFound or commands.UserNotFound as d_error:
			await edit(content=f"🕳️ Membre `{str(d_error).split(' ')[1]}` non trouvé ! N'hésitez pas à envoyer un ping au membre demandé.")
		# UserInputError -> BadUnionArgument | BadLiteralArgument | ArgumentParsingError
		except commands.BadArgument or commands.BadUnionArgument or commands.BadLiteralArgument or commands.ArgumentParsingError as d_error:
			await edit(content=f"🕳️ {d_error}")
		# CommandNotFound
		except commands.CommandNotFound as d_error:
			await edit(content=f"🕳️ Commande `{str(d_error).split(' ')[1]}` non trouvée !")
		# CheckFailure
		except commands.PrivateMessageOnly:
			await edit(content="🕳️ Cette commande ne peut pas être utilisée dans un serveur, essayez en message privé.")
		except commands.NoPrivateMessage:
			await edit(content="🕳️ Cela ne fonctionne pas comme prévu.")
		except commands.NotOwner:
			await edit(content="🕳️ Vous devez posséder ce robot pour exécuter cette commande.")
		except commands.MissingPermissions as d_error:
			await edit(content=f"🕳️ Votre compte requiert les permissions suivantes : {'` `'.join(d_error.missing_permissions)}.")
		except commands.BotMissingPermissions as d_error:
			if not "send_messages" in d_error.missing_permissions:
				await edit(content=f"🕳️ Le bot nécessite les permissions suivantes : {'` `'.join(d_error.missing_permissions)}.")
		except commands.CheckAnyFailure or commands.MissingRole or commands.BotMissingRole or commands.MissingAnyRole or commands.BotMissingAnyRole as d_error:
			await edit(content=f"🕳️ {d_error}")
		except commands.NSFWChannelRequired:
			await edit(content="🕳️ Cette commande nécessite un canal NSFW.")
		# DisabledCommand
		except commands.DisabledCommand:
			await edit(content="🕳️ Désolé, cette commande est désactivée.")
		# CommandInvokeError
		except commands.CommandInvokeError as d_error:
			await edit(content=f"🕳️ {d_error.original}")
		# CommandOnCooldown
		except commands.CommandOnCooldown as d_error:
			await edit(content=f"🕳️ La commande est en cooldown, attendez `{str(d_error).split(' ')[7]}` !")
		# MaxConcurrencyReached
		except commands.MaxConcurrencyReached as d_error:
			await edit(content=f"🕳️ Concurrence maximale atteinte. Nombre maximum d'utilisateurs concurrents autorisés : `{d_error.number}`, par `{d_error.per}`.")
		# HybridCommandError
		except commands.HybridCommandError as d_error:
			await self.get_app_command_error(ctx.interaction, error)
		except Exception as e:
			print(f"! Cogs.errors get_command_error : {type(error).__name__} : {error}\n! Internal Error : {e}\n")

	@commands.Cog.listener("on_app_command_error")
	async def get_app_command_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
		"""App command Error Handler
		doc: https://discordpy.readthedocs.io/en/master/interactions/api.html#exception-hierarchy
		"""
		try:
			await self.__respond_to_interaction(interaction)
			edit = interaction.edit_original_message

			raise error
		except app_commands.CommandInvokeError as d_error:
			if isinstance(d_error.original, discord.errors.InteractionResponded):
				await edit(content=f"🕳️ {d_error.original}")
			elif isinstance(d_error.original, discord.errors.Forbidden):
				await edit(content=f"🕳️ `{type(d_error.original).__name__}` : {d_error.original.text}")
			else:
				await edit(content=f"🕳️ `{type(d_error.original).__name__}` : {d_error.original}")
		except app_commands.CheckFailure as d_error:
			if isinstance(d_error, app_commands.errors.CommandOnCooldown):
				await edit(content=f"🕳️ La commande est en cooldown, attendez `{str(d_error).split(' ')[7]}` !")
			else:
				await edit(content=f"🕳️ `{type(d_error).__name__}` : {d_error}")
		except app_commands.CommandNotFound:
			await edit(content=f"🕳️ La commande n'a pas été trouvée. Il semble qu'il s'agisse d'un bug de discord, probablement dû à une désynchronisation. Il se peut que plusieurs commandes portent le même nom, vous devriez en essayer une autre.")
		except Exception as e: 
			"""
			Caught here:
			app_commands.TransformerError
			app_commands.CommandLimitReached
			app_commands.CommandAlreadyRegistered
			app_commands.CommandSignatureMismatch
			"""

			print(f"! Cogs.errors get_app_command_error : {type(error).__name__} : {error}\n! Internal Error : {e}\n")

	@commands.Cog.listener("on_view_error")
	async def get_view_error(self, interaction: discord.Interaction, error: Exception, item: any):
		"""View Error Handler"""
		try:
			raise error
		except discord.errors.Forbidden:
			pass
		except Exception as e:
			print(f"! Cogs.errors get_view_error : {type(error).__name__} : {error}\n! Internal Error : {e}\n")


async def setup(bot):
	await bot.add_cog(Errors(bot))