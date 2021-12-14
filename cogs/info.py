import io
import time
from typing import List
import discord
from discord import embeds
import matplotlib.pyplot as plt
from datetime import datetime
from pytz import timezone

from discord.ext import commands

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

def statServer(guild):
	status = {}
	must = ['members', 'bot', 'streaming', 'idle', 'dnd', 'online', 'offline', 'mobile']
	for a in must:
		status[a] = 0
	for member in guild:
		status['members'] += 1
		status[str(member.status)] += 1
		if member.is_on_mobile(): status['mobile'] += 1
		if member.bot: status['bot'] += 1
		if member.activity or member.activities: 
			for activity in member.activities:
				if activity.type == discord.ActivityType.streaming:
					status['streaming'] += 1

	return status

class Info(commands.Cog, name="info", command_attrs=dict(hidden=False)):
	"""Description des commandes sur l'information"""
	def __init__(self, bot):
		self.bot = bot

	def help_custom(self):
		emoji = '💬'
		label = "Informations"
		description = "Informations globales, comme les statistiques du serveur, les informations sur le Bot, etc"
		return emoji, label, description

	@commands.command(name='stat', aliases=['status','graph','gs','sg'])
	async def help(self, ctx):
		"""Stats du serveur"""
		plt.clf()
		ax, data, colors = plt.subplot(), statServer(ctx.guild.members), ["#747f8d","#f04747","#faa81a","#43b582"]
		ax.pie([data['offline'], data['dnd'], data['idle'], data['online']], colors=colors, startangle=-40, wedgeprops=dict(width=0.5))
		leg = ax.legend(['Offline','dnd','idle','Online'],frameon=False, loc='lower center', ncol=5)
		for color,text in zip(colors,leg.get_texts()):
			text.set_color(color)
		image_binary = io.BytesIO()
		plt.savefig(image_binary, transparent=True)
		image_binary.seek(0)
		
		embed = discord.Embed(title="Statistiques actuelles du serveur ({})".format(data['members']),description="<:white_circle:845307338252222474> : **`{}`** (Offline)\n<:sleeping:698246924058361898> : **`{}`** (AFK)\n<:red_circle:845307338252222474>: **`{}`** (Do not disturb)\n<:green_circle:845307287307943957> : **`{}`** (Online)\n<:purple_circle:845308223196102727> : **`{}`** (Streaming)\n<:mobile_phone:698257015578951750> : **`{}`** (On mobile)\n<:robot:698250069165473852> : **`{}`** (Bot)".format(data['offline'], data['idle'], data['dnd'], data['online'], data['streaming'], data['mobile'], data['bot']))

		embed.set_image(url='attachment://stat.png')

		embed.set_footer(text="Demandé par : "+str(ctx.message.author.name)+" à " + Timer(), icon_url=ctx.message.author.display_avatar.url)

		await ctx.send(file=discord.File(fp=image_binary, filename='stat.png'), embed=embed)
  
	@commands.command(name="informations", aliases=["i", 'infos'])
	async def infos(self, ctx):
		"""Affiche les informations sur le Bot"""
	 
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
  
		text = "Collaborateurs"
  
		draw = ImageDraw.Draw(card)
		font = ImageFont.truetype("arial.ttf", 60)
  
		draw.text((280,60), text, font=font, fill=(255,255,255,128))
  
		card.save('img/final_card.png')
 
		final_card = discord.File('img/final_card.png')
  

		file = discord.File("img/final_card.png", filename="final_card.png")
  
		embed = discord.Embed(title="Donne des informations sur moi", color=0x4F2B10, description="Yo, je suis le bot de <@!405414058775412746>", colour=discord.Colour(0x4F2B10))
  
		embed.add_field(name="Ajoutes moi sur ton serveur en cliquant ici :", value="__[Invitation](https://discord.com/api/oauth2/authorize?client_id=808008104628322334&permissions=8&scope=bot)__")

		embed.set_image(url="attachment://final_card.png")

		embed.set_footer(text="Demandé par : "+str(ctx.message.author.name)+" à " + Timer(), icon_url=ctx.message.author.display_avatar.url)

		await ctx.send(file=file, embed=embed)

	@commands.command(name='numbersofservers', aliases=['nbs'])
	async def servers(self, ctx):
		"""Affiche la liste ainsi que le nombre de serveurs où LavaL Bot est"""
		number_servers = str(len(self.bot.guilds))
		embed = discord.Embed(title=f"Nom de tout les servers où {self.bot.user.name} est", description=f"Actuellement {self.bot.user.name} est sur **" + number_servers + "** serveurs", colour=discord.Colour(0xFA8072))

		embed.add_field(name="Liste des serveurs :", value='\n'.join(guild.name for guild in self.bot.guilds))

		embed.set_footer(text="Demandé par : "+str(ctx.message.author.name)+" à " + Timer(), icon_url=ctx.message.author.display_avatar.url)
  
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Info(bot))
