import discord
import asyncio
import glob
import os
from discord.ext import commands
from datetime import datetime, timedelta
from views import help as vhelp

def CountLines():
	path = 'cogs/'
	variable = []
	for filename in glob.glob(os.path.join(path, '*.py')):
		with open(os.path.join(os.getcwd(), filename), 'r') as files:
			nonempty_lines = [line.strip("\n") for line in files if line != "\n"]
		line_count = len(nonempty_lines)
		variable.append(line_count)
	return variable

class HelpCommand(commands.HelpCommand):
	"""Commande d'aide"""

	async def on_help_command_error(self, ctx, error) -> None:
		handledErrors = [
			commands.CommandOnCooldown, 
			commands.CommandNotFound
		]

		if not type(error) in handledErrors:
			print("! Help command Error :", error, type(error), type(error).__name__)
			return await super().on_help_command_error(ctx, error)

	def command_not_found(self, string) -> None:
		raise commands.CommandNotFound(f"Command {string} is not found")

	async def send_bot_help(self, mapping) -> None:
		allowed = 5
		close_in = round(datetime.timestamp(datetime.now() + timedelta(minutes=allowed)))
		embed = discord.Embed(color=discord.Color.dark_grey(), title = "👋 Aide · Acceuil", description = "Bienvenue sur le menu d'aide.\n\nUtilise la commande `help` pour avoir plus d'informations sur une commande.\nUtilise la catégorie `help` pour avoir plus d'informations sur une catégorie.\nUtilise le menu déroulant ci-dessous pour sélectionner une catégorie.\n\u200b", url='https://github.com/RomainNicolaon/LavaL_Bot')
		embed.add_field(name="Temps restant avant la fin de la commande :", value="Cette session d'aide se terminera <t:"+str(close_in)+":R>.\nUtilise la commande `help` pour ouvrir une nouvelle cession d'aide.\n\u200b", inline=False)
		embed.add_field(name="Qui suis-je ?", value="Je suis un bot créé par <@!405414058775412746>; en collaboration avec <@!265148938091233293>. Créé pour le fun en 2021, je suis désormais un Bot avec le but d'être utilisé partout donc n'hésite pas à m'ajouter sur ton serveur xD.\nJ'ai beaucoup de fonctionnalités comme un lecteur de musique, un gestionnaire d'événements, des utilitaires, et plus encore.\n\nJe suis open source, vous pouvez voir mon code sur [Github](https://github.com/RomainNicolaon/LavaL_Bot) !\n\n `Total de lignes de code : "+ str(sum(CountLines()))+"`")

		view = vhelp.View(mapping = mapping, ctx = self.context, homeembed = embed, ui = 2)
		message = await self.context.send(embed = embed, view = view)
		try:
			await asyncio.sleep(60*allowed)
			view.stop()
			await message.delete()
		except: 
			pass

	async def send_command_help(self, command):
		cog = command.cog
		if "help_custom" in dir(cog):
			emoji, label, _ = cog.help_custom()
			embed = discord.Embed(title = f"{emoji} Help · {label} : {command.name}", description=f"**Command** : {command.name}\n{command.help}", url="https://github.com/RomainNicolaon/LavaL_Bot")
			params = ""
			for param in command.clean_params: 
				params += f" <{param}>"
			embed.add_field(name="Usage", value=f"{command.name}{params}", inline=False)
			embed.add_field(name="Aliases", value=f"{command.aliases}`")
			embed.set_footer(text="Rappel : Les crochets tels que <> ne doivent pas être utilisés lors de l'exécution de commandes.", icon_url=self.context.message.author.display_avatar.url)
			await self.context.send(embed=embed)

	async def send_cog_help(self, cog):
		if "help_custom" in dir(cog):
			emoji, label, _ = cog.help_custom()
			embed = discord.Embed(title = f"{emoji} Help · {label}",description=f"`{cog.__doc__}`", url="https://github.com/RomainNicolaon/LavaL_Bot")
			for command in cog.get_commands():
				params = ""
				for param in command.clean_params: 
					params += f" <{param}>"
				embed.add_field(name=f"{command.name}{params}", value=f"{command.help}\n\u200b", inline=False)
			embed.set_footer(text="Rappel : Les crochets tels que <> ne doivent pas être utilisés lors de l'exécution de commandes.", icon_url=self.context.message.author.display_avatar.url)
			await self.context.send(embed=embed)

	async def send_group_help(self, group):
		await self.context.send("Commandes de groupe non disponibles.")

class Help(commands.Cog, name="help"):
	"""
		Commandes d'aide.
		
		Require intents: 
			- message_content
		
		Require bot permission:
			- read_messages
			- send_messages
	"""
	def __init__(self, bot: commands.Bot) -> None:
		self._original_help_command = bot.help_command

		attributes = {
			'name': "help",
			'aliases': ['h', '?'],
			'cooldown': commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.user) # discordpy2.0
		} 

		bot.help_command = HelpCommand(command_attrs=attributes)
		bot.help_command.cog = self
		
	async def cog_unload(self) -> None:
		self.bot.help_command = self._original_help_command

	def help_custom(self) -> tuple[str, str, str]:
		emoji = '🆘'
		label = "Help"
		description = "Help utilities."
		return emoji, label, description

async def setup(bot):
	await bot.add_cog(Help(bot))