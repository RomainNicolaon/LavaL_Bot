import discord

from discord.ext import commands


class Welcome(commands.Cog, name="welcome"):
	"""Basic description"""
	def __init__(self, bot):
		self.bot = bot

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

def setup(bot):
	bot.add_cog(Welcome(bot))
