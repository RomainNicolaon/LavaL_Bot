import io
import time
import discord
import matplotlib.pyplot as plt
from datetime import datetime
from pytz import timezone

from discord.ext import commands

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

class Info(commands.Cog, name="info"):
	"""Info description"""
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='stat', aliases=['status','graph','gs','sg'])
	async def help(self, ctx):
		plt.clf()
		ax, data, colors = plt.subplot(), statServer(ctx.guild.members), ["#747f8d","#f04747","#faa81a","#43b582"]
		ax.pie([data['offline'], data['dnd'], data['idle'], data['online']], colors=colors, startangle=-40, wedgeprops=dict(width=0.5))
		leg = ax.legend(['Offline','dnd','idle','Online'],frameon=False, loc='lower center', ncol=5)
		for color,text in zip(colors,leg.get_texts()):
			text.set_color(color)
		image_binary = io.BytesIO()
		plt.savefig(image_binary, transparent=True)
		image_binary.seek(0)
		
		embed = discord.Embed(title="Current server stats ({})".format(data['members']),description="<:white_circle:845307338252222474> : **`{}`** (Offline)\n<:sleeping:698246924058361898> : **`{}`** (AFK)\n<:red_circle:845307338252222474>: **`{}`** (Do not disturb)\n<:green_circle:845307287307943957> : **`{}`** (Online)\n<:purple_circle:845308223196102727> : **`{}`** (Streaming)\n<:mobile_phone:698257015578951750> : **`{}`** (On mobile)\n<:robot:698250069165473852> : **`{}`** (Bot)".format(data['offline'], data['idle'], data['dnd'], data['online'], data['streaming'], data['mobile'], data['bot']))
		embed.set_image(url='attachment://stat.png')
		embed.set_footer(text="Requested by : "+str(ctx.message.author)+" à "+str(time.strftime('%H:%M:%S')), icon_url=ctx.message.author.avatar_url)
		await ctx.send(file=discord.File(fp=image_binary, filename='stat.png'), embed=embed)
  
	@commands.command(name="infos", aliases=["i"])
	async def infos(self, ctx):
		embed = discord.Embed(title="Donne des informations sur moi", color=0x4F2B10, description="Yo, je suis le bot de <@!405414058775412746>, pour m'utiliser, tapez la commande : \n```?help``` ```??```  ```?h```", colour=discord.Colour(0x4F2B10))
  
		embed.add_field(name="Ajoutes moi sur ton serveur :", value="https://discord.com/api/oauth2/authorize?client_id=808008104628322334&permissions=8&scope=bot")

		embed.set_thumbnail(url="https://steemitimages.com/DQmbQ9tUdvP98ruzMX6gCjXWz6N5yMBHbn7oJ1WeiiQoj68/16361360.png")

		embed.set_footer(text="Requested by : "+str(ctx.message.author.name) +" "+ str(time.strftime('%H:%M:%S')), icon_url=ctx.message.author.avatar_url)

		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Info(bot))
