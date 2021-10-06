import time
import discord
import random

from discord.ext import commands
from discord import Member

class Funcmd(commands.Cog, name="funcmd", command_attrs=dict(hidden=False)):
	"""Description des commandes pour le fun"""
	def __init__(self, bot):
		self.bot = bot

	def help_custom(self):
		emoji = '<a:CatGunner:876156284557221929>'
		label = "Commandes Fun"
		description = "Commandes pour le fun, comme avatar, etc.."
		return emoji, label, description
  
	@commands.command(name='avatar', aliases=['a'])
	async def getpfp(self, ctx, member: Member = None):
		"""Affiche la photo de profil (soi même ou un utilisateur"""
		if not member:
			member = ctx.author
		pfp = member.display_avatar.url
		embed = discord.Embed(title=f"Affiche la photo de profile de {member.name}#{member.discriminator}", color=0x00000, description=f"[Avatar URL]({pfp})")

		embed.set_image(url=pfp)

		embed.set_footer(text="Demandé par : "+str(ctx.message.author.name)+" à " +
						 str(time.strftime('%H:%M:%S')), icon_url=ctx.message.author.display_avatar.url)

		await ctx.send(embed=embed)


	@commands.command(name='hug')
	async def hug(self, ctx, member: Member = None):
		gif_hug = random.choice([
			"https://cdn.zerotwo.dev/HUG/9300c260-931c-4572-9a11-9a0f1f54735d.gif", "https://media.giphy.com/media/fvN5KrNcKKUyX7hNIA/giphy.gif",
			"https://media.giphy.com/media/kooPUWvhaGe7C/giphy.gif",
			"https://media.giphy.com/media/3EJsCqoEiq6n6/giphy.gif",
			"https://cdn.zerotwo.dev/HUG/e2d1bb44-d211-423e-9130-ad86dc29c882.gif"
			])

		embed = discord.Embed(title =f"{ctx.author.name} fait un gros câlin à {member.name}#{member.discriminator}", description="", color = 0x83B5E3)

		embed.set_image(url=gif_hug)

		embed.set_footer(text="Demandé par : "+str(ctx.message.author.name)+" à " +
						 str(time.strftime('%H:%M:%S')), icon_url=ctx.message.author.display_avatar.url)

		await ctx.send(embed=embed)


	@commands.command(name='kiss')
	async def kiss(self, ctx, member: Member = None):
		gif_kiss = random.choice([
			"https://cdn.zerotwo.dev/KISS/1afe24ba-5014-4ddd-9222-5969076e9de3.gif",
			"https://cdn.zerotwo.dev/KISS/1a43ff80-a5ca-4e78-929b-09714a51b557.gif",
			"https://cdn.zerotwo.dev/KISS/c769d606-869d-48c7-8fc7-a531010bcb27.gif",
			"https://cdn.zerotwo.dev/KISS/8b7dbe1a-ad13-48bf-9142-a9db21748f12.gif"
			])

		embed = discord.Embed(title =f"{ctx.author.name} embrasse passionnément {member.name}#{member.discriminator}", description="", color = 0x83B5E3)

		embed.set_image(url=gif_kiss)

		embed.set_footer(text="Demandé par : "+str(ctx.message.author.name)+" à " +
						 str(time.strftime('%H:%M:%S')), icon_url=ctx.message.author.display_avatar.url)

		await ctx.send(embed=embed)


	@commands.command(name='punch')
	async def punch(self, ctx, member: Member = None):
		gif_punch = random.choice([
			"https://media.giphy.com/media/Z5zuypybI5dYc/giphy.gif",
			"https://media.discordyui.net/reactions/slap/6784568.gif",
			"https://media.discordyui.net/reactions/slap/aVDQEfA.gif"
			])

		embed = discord.Embed(title =f"{ctx.author.name} frappe violemment {member.name}#{member.discriminator}", description="", color = 0x83B5E3)

		embed.set_image(url=gif_punch)

		embed.set_footer(text="Demandé par : "+str(ctx.message.author.name)+" à " +
						 str(time.strftime('%H:%M:%S')), icon_url=ctx.message.author.display_avatar.url)

		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Funcmd(bot))