import discord
from discord import file
from discord import message
from discord import channel

from discord.ext import commands

from PIL import Image, ImageDraw, ImageFont, ImageChops
from io import BytesIO


class Joinserv(commands.Cog, name="joinserv", command_attrs=dict(hidden=False)):
	"""Description des commandes bienvenue"""
	def __init__(self, bot):
		self.bot = bot

	def help_custom(self):
		emoji = ':🥳:'
		label = "Bienvenue"
		description = "Informations sur l'accueil global"
		return emoji, label, description

	@commands.Cog.listener()
	async def on_member_join(self, member):
		for channel in member.guild.channels:
			if str(channel) == "arrive":
				embed = discord.Embed(color=0x4a3d9a)
				embed.add_field(name="Bienvenue", value=f"**{member.name}** vient de rejoindre **{member.guild.name}**", inline=False)
				embed.set_thumbnail(url="https://media.tenor.com/images/d139e96072bae377be522258f7128881/tenor.gif")
				await channel.send(embed=embed)

	
	@commands.Cog.listener()
	async def on_member_remove(self, member):
		for channel in member.guild.channels:
			if str(channel) == "arrive":
				embed = discord.Embed(color=0x4a3d9a)
				embed.add_field(name="Au revoir", value=f"**{member.name}** vient de quitter **{member.guild.name}**", inline=False)
				embed.set_thumbnail(url="https://i.pinimg.com/originals/2d/02/44/2d024443d7e18982443275923492ec5e.gif")
				await channel.send(embed=embed)
	
	@commands.command(name='pic')
	async def picture(self, ctx, user: discord.Member = None):
		if user == None:
			user = ctx.message
  
		# text = f"Bienvenue {user.author.name} vient de rejoindre {user.guild.name}"
  
		def add_corners( pfp, rad):
			circle = Image.new('L', (rad * 2, rad * 2), 0)
			draw2 = ImageDraw.Draw(circle)
			draw2.ellipse((0, 0, rad * 2, rad * 2), fill=255)
			alpha = Image.new('L', pfp.size, 255)
			w, h = pfp.size
			alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
			alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
			alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
			alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
			pfp.putalpha(alpha)
			return pfp

  
		text = f"Eh toi tu t'appelle bien {user.author.name} ?"

		card = Image.open("img/background2.png")
		asset = user.author.avatar_url
		data = BytesIO(await asset.read())
		pfp = Image.open(data)
		pfp = pfp.resize((220,220))

		pfp = add_corners(pfp, 100)
		pfp.save("img/pfp.png")
		card.paste(pfp, (110,65))
		# pfp.show()
  
		############################
  
		draw = ImageDraw.Draw(card)
		font = ImageFont.truetype("arial.ttf", 30)
  
		draw.text((25,370), text, font=font, fill=(255,255,255,128))
  
		card.save("img/profile.png")

		picture = discord.File("img/pfp.png")
		profile = discord.File("img/profile.png")
  
		await ctx.send(file = profile)
		# await channel.send(file = picture)

def setup(bot):
	bot.add_cog(Joinserv(bot))
