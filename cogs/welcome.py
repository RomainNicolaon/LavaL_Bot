from ast import Not
import discord
from discord.ext import commands
from views import link

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

class Welcome(commands.Cog, name="welcome", command_attrs=dict(hidden=False)):
	"""Description des commandes bienvenue"""
	def __init__(self, bot):
		self.bot = bot
		self.welcome_data = self.bot.database_data["welcome"]

	@commands.Cog.listener()
	async def on_member_join(self, member):
		guild = member.guild
		response = await self.bot.database.lookup(self.welcome_data["table"], "is_active", "guild_id", str(member.guild.id))
		if guild.id == 441962473583804416:
			if guild.system_channel:
				embed = discord.Embed(color=0x4a3d9a)
				embed.add_field(name="Bienvenue", value=f"**<@!{member.id}>** vient de rejoindre **{member.guild.name}**", inline=False)
				embed.set_thumbnail(url="https://c.tenor.com/PhhN-3LjE3AAAAAd/gatto-cibo.gif")
				await guild.system_channel.send(embed=embed)
		if response and response[0][0]:
			if guild.system_channel:
				embed = discord.Embed(color=0x4a3d9a)
				embed.add_field(name="Bienvenue", value=f"**<@!{member.id}>** vient de rejoindre **{member.guild.name}**", inline=False)
				embed.set_thumbnail(url="https://media.tenor.com/images/d139e96072bae377be522258f7128881/tenor.gif")
				await guild.system_channel.send(embed=embed)
		if not response:
			if guild.system_channel:
				embed = discord.Embed(color=0x4a3d9a)
				embed.add_field(name="Bienvenue", value=f"**<@!{member.id}>** vient de rejoindre **{member.guild.name}**", inline=False)
				embed.set_thumbnail(url="https://media.tenor.com/images/d139e96072bae377be522258f7128881/tenor.gif")
				await guild.system_channel.send(embed=embed)

	
	@commands.Cog.listener()
	async def on_member_remove(self, member):
		guild = member.guild
		response = await self.bot.database.lookup(self.welcome_data["table"], "is_active", "guild_id", str(member.guild.id))
		if response and response[0][0]:
			if guild.system_channel:
				embed = discord.Embed(color=0x4a3d9a)
				embed.add_field(name="Au revoir", value=f"**<@!{member.id}>** vient de quitter **{member.guild.name}**", inline=False)
				embed.set_thumbnail(url="https://i.pinimg.com/originals/2d/02/44/2d024443d7e18982443275923492ec5e.gif")
				await guild.system_channel.send(embed=embed)
	
	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		if guild.system_channel:
			view = link.View(label="Github", url="https://github.com/RomainNicolaon/LavaL_Bot")
			embed = discord.Embed(title="LavaL Bot - Un bot fun et utile créé par LavaL#9240", description="Merci de m'avoir ajouté à ton serveur !\n\nPour commencer, utilises la commande `?help` pour accerder aux commandes disponibles.\nTu peux aussi modifier le préfix du bot en utilisant la commande `?changeprefix`.\n\nRetrouves le code source du bot en cliquant sur le lien ci-dessous.", color=0x12F932)
			await guild.system_channel.send(embed=embed, view=view)
	
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
  
		text = f"Bienvenue, {user.author.name} vient de rejoindre {user.guild.name}"

		card = Image.open("img/background2.png")

		asset = user.author.display_avatar
		data = BytesIO(await asset.read())
		pfp = Image.open(data).convert('RGB')
		pfp = pfp.resize((220,220))

		pfp = add_corners(pfp, 100)
		pfp.save("img/pfp.png")
		card.paste(pfp, (110,65))

  
		draw = ImageDraw.Draw(card)
		font = ImageFont.truetype("arial.ttf", 30)
		draw.text((25,370), text, font=font, fill=(255,255,255,128))
		card.save("img/profile.png")

		picture = discord.File("img/pfp.png")
		profile = discord.File("img/profile.png")
  
		await ctx.send(file = profile)

	@commands.command(name='test')
	async def test(self, member):
		response = await self.bot.database.lookup(self.welcome_data["table"], "is_active", "guild_id", str(member.guild.id))
		print(response)
		print(response[0][0])

def setup(bot):
	bot.add_cog(Welcome(bot))
