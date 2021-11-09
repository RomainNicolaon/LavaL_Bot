import time
import asyncio
import discord
from discord.embeds import Embed
from views import link
from discord.ext import commands
from datetime import datetime, timedelta
from pytz import timezone
from views import help as vhelp

from PIL import Image, ImageDraw, ImageFont, ImageChops
from io import BytesIO
import requests

def Timer():
	fmt = "%H:%M:%S"
	# Current time in UTC
	now_utc = datetime.now(timezone('UTC'))
	now_berlin = now_utc.astimezone(timezone('Europe/berlin'))
	actual_time = now_berlin.strftime(fmt)
	return actual_time

class Basic(commands.Cog, name="basic", command_attrs=dict(hidden=False)):
	"""Description des commandes de base"""
	def __init__(self, bot):
		self.bot = bot

	def help_custom(self):
		emoji = '📙'
		label = "Basic"
		description = "Commandes de base, comme help, ping, etc.."
		return emoji, label, description

	@commands.command(name='help', aliases=['?', 'h', 'commands'])
	async def help(self, ctx, *input):
		"""Affiche le menu d'aide"""
		if not input:
			allowed = 3
			close_in = round(datetime.timestamp(datetime.now() + timedelta(minutes=allowed)))
			embed = discord.Embed(color=discord.Color.dark_grey(), title = "👋 Aide · Acceuil", description = "`Bienvenue sur le menu d'aide.`\n\nUtilise `help command` pour avoir plus d'informations sur une commande.\nUtilise `help category` pour avoir plus d'informations sur une categorie.\nUtilise le menu déroulant ci-dessous pour sélectionner une catégorie.\n\u200b", url='https://github.com/LavaL18/LavaL_Bot')
			embed.add_field(name="Temps restant avant la fin de la commande :", value="Cette session d'aide se terminera <t:"+str(close_in)+":R>.\nUtilise la commande `help` pour ouvrir une nouvelle cession d'aide.\n\u200b", inline=False)
			embed.add_field(name="Qui suis-je ?", value="Je suis un bot créé par <@!405414058775412746>; en collaboration avec <@!265148938091233293>. Créé pour le fun en 2021, je suis désormais un Bot avec le but d'être utilisé partout donc n'hésite pas à m'ajouter sur ton serveur xD.\nJ'ai beaucoup de fonctionnalités comme un lecteur de musique, un gestionnaire d'événements, des utilitaires, et plus encore.\n\nJe suis open source, vous pouvez voir mon code sur [Github](https://github.com/LavaL18/LavaL_Bot) !")

			view = vhelp.View(bot=self.bot, ctx=ctx, homeembed=embed, ui=2)
			message = await ctx.send(embed=embed, view=view)
			try:
				await asyncio.sleep(60*allowed)
				view.stop()
				await message.delete()
				await ctx.message.add_reaction("<a:yes_animated:844992841938894849>")
			except: pass

		elif len(input) == 1:
			search, search_command, search_cog, embed = input[0].lower(), None, None, None
			try:
				search_command = self.bot.get_command(search)
				search_cog = self.bot.cogs[search]
			except: pass

			if search_cog:
				if "help_custom" in dir(search_cog):
					emoji, label, description = search_cog.help_custom()
					embed = discord.Embed(title = str(emoji)+" Aide · "+str(label),description='`'+str(search_cog.__doc__)+'`', url='https://github.com/LavaL18/LavaL_Bot')
					for command in search_cog.get_commands():
						params = ""
						for param in command.clean_params: params += " <"+str(param)+">"
						embed.add_field(name=str(command.name)+str(params), value=str(command.help)+"\n\u200b", inline=False)
			elif search_command:
				cog = search_command.cog
				if "help_custom" in dir(cog):
					emoji, label, description = cog.help_custom()
					embed = discord.Embed(title = str(emoji)+" Aide · "+str(label)+" : "+str(search_command.name), description="**Commande** : "+str(search_command.name)+"\n"+str(search_command.help), url='https://github.com/LavaL18/LavaL_Bot')
				params = ""
				for param in search_command.clean_params: params += " <"+str(param)+">"
				embed.add_field(name="Utilisation", value=str(search_command.name)+str(params), inline=False)
				embed.add_field(name="Alias", value='`'+str(search_command.aliases)+'`')
			else:
				raise commands.CommandError("Rien n'a été trouvé.")
			
			embed.set_footer(text="Rappel : Les crochets tels que <> ne doivent pas être utilisés lors de l'exécution de commandes.", icon_url=ctx.message.author.display_avatar.url)
			await ctx.send(embed=embed)

		elif len(input) > 1:
			raise commands.CommandError("Trop d'arguments.")

	@commands.command(name='ping', pass_context=True)
	async def ping(self, ctx):
		before = time.monotonic()
		message = await ctx.message.reply(":ping_pong: Pong !")
		ping = (time.monotonic() - before) * 1000
		await message.edit(content=f":ping_pong: Pong ! in `{float(round(ping/1000.0,3))}s` ||{int(ping)}ms||")

	@commands.command(name='server', aliases=['serv', 's'])
	async def server(self, ctx):
		"""Donne des informations sur le serveur"""
		
		server_icon = ctx.guild.icon
		embed = discord.Embed(title="Donne des informations sur le serveur", color=0x12F932, description="Ce serveur s'appelle "+str(ctx.message.guild.name) +
							  " et totalise "+str(ctx.message.guild.member_count)+" membres et son créateur est <@!" + str(ctx.message.guild.owner_id)+">.", colour=discord.Colour(0x12F932))

		embed.set_thumbnail(
			url=server_icon)

		embed.set_footer(text="Demandé par : "+str(ctx.message.author.name)+" à " +
						 Timer(), icon_url=ctx.message.author.display_avatar.url)

		await ctx.send(embed=embed)

	@commands.command(name='invitation', aliases=['inv', 'invit'])
	async def invitation(self, ctx):
		"""Comment inviter LavaL Bot"""

		view = link.View(label=f"Cliquez ici pour ajouter {self.bot.user.name}", url="https://discord.com/api/oauth2/authorize?client_id=829279577267896382&permissions=8&scope=bot")

		embed = discord.Embed(title = "Invitation", color = 0x12F932, description=f"Comment inviter {self.bot.user.name}", colour=discord.Colour(0x12F932))

		embed.add_field(name="Ajoutes moi sur ton serveur en cliquant ici :", value="__[Invitation](https://discord.com/api/oauth2/authorize?client_id=829279577267896382&permissions=8&scope=bot)__")
  
		embed.set_thumbnail(
			url="https://steemitimages.com/DQmbQ9tUdvP98ruzMX6gCjXWz6N5yMBHbn7oJ1WeiiQoj68/16361360.png")

		await ctx.send(embed=embed, view=view)

	@commands.command(name='alliasinfos', aliases=['all', 'allias'])
	async def alliasinfos(self, ctx, *input):
		"""Affiche la commande d'aide en utilisant : help {COMMANDE/CATEGORIE}"""
		embed = discord.Embed()
		remind = "\n**Rappel** : Les crochets tels que {} ne doivent pas être utilisés lors de l'exécution de commandes."
		title, description, color = "Aide · ", "", discord.Color.blue()
		if not input:
			category_list = ''
			for cog in self.bot.cogs:
				cog_settings = self.bot.get_cog(cog).__cog_settings__
				if len(cog_settings) == 0 or not cog_settings['hidden']:
					category_list += "{**"+str(cog).upper()+"**}\n *" + \
						str(self.bot.cogs[cog].__doc__)+"*\n"
			embed.add_field(name="Categorie :",
							value=category_list, inline=False)

		elif len(input) == 1:
			search, search_command, search_cog = input[0].lower(), False, False
			try:
				search_command = self.bot.get_command(search)
				search_cog = self.bot.cogs[search]
			except:
				pass

			title = "Aide · " + str(search)
			if search_cog:
				description, command_list = str(search_cog.__doc__), ''
				for command in search_cog.get_commands():
					command_list += "__" + \
						str(command.name)+"__\n"+str(command.help)+'\n'
				embed.add_field(name="Commandes :",
								value=command_list, inline=False)
			elif search_command:
				description, color = '', discord.Color.green()
				embed.add_field(name=str(search_command.name), value="__Alias__ : `"+"`, `".join(
					search_command.aliases)+"`\n__Aide__ : "+str(search_command.help), inline=False)
			else:
				title, description, color = "Aide · Erreur", "Rien n'a été trouvé", discord.Color.orange()

		elif len(input) > 1:
			title, description, color = "Aide · Erreur", "Trop d'arguments", discord.Color.orange()

		embed.title, embed.description, embed.color = title, remind + description, color
		embed.set_footer(text="Demandé par : "+str(ctx.message.author.name)+" à " +
						 Timer(), icon_url=ctx.message.author.display_avatar.url)
		await ctx.send(embed=embed)

	@commands.command(name='collaborators', aliases=['clb'])
	async def collaborators(self, ctx, *input):
		"""Affiche la liste des collaborateurs"""

		collabs = ['78691006', '71769515']

		url0 = 'https://avatars.githubusercontent.com/u/' + collabs[0] + '?v=4/img'
		url1 = 'https://avatars.githubusercontent.com/u/' + collabs[1] + '?v=4/img'

		card0 = Image.open(requests.get(url0, stream=True).raw)
		card1 = Image.open(requests.get(url1, stream=True).raw)
		
		card0 = card0.resize((280,280))
		card1 = card1.resize((280,280))
  
		card0.save('img/Romain.png')
		card1.save('img/Paul.png')
  
		card = Image.open('img/github.png')
  
		card.paste(card0, (80,165))
		card.paste(card1, (580,165))
  
  
		####################################################################
  
		text = "Collaborators"
  
		draw = ImageDraw.Draw(card)
		font = ImageFont.truetype("arial.ttf", 60)
  
		draw.text((280,60), text, font=font, fill=(255,255,255,128))
  
		card.save('img/final_card.png')
 
		final_card = discord.File('img/final_card.png')
		
		await ctx.send(file = final_card)


def setup(bot):
	bot.add_cog(Basic(bot))
