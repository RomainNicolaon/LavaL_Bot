import time
import discord
import datetime
from discord import message
from discord import colour

from discord.ext import commands, tasks

date_student = ["20/12", "23/10", "27/07", "14/11", "02/04", "11/05", "26/09", "13/11", "27/02", "21/04", "03/12", "18/12", "27/07"]

year_date_students = ["2002", "2002", "2002", "0666", "1999", "2003", "2002", "1985", "1999", "2002", "1997", "2001", "1999"]

ID_users = ["405414058775412746", "354321839234744320", "501471077709381643", "265148938091233293", "219156294974570497", "456516058984087583", "248910730122756108", "759045368591155221", "755449654912614441", "627775366601113601", "436469556257619978", "293476472767905792", "267377288989900810"]

# print(len(date_student), len(year_date_students), len(ID_users))

today = datetime.datetime.now()
hour = today.strftime("%H")
day = today.strftime("%d")
month = today.strftime("%m")
year = today.year

class Birthday(commands.Cog, name="birthday"):
	"""Birthday description"""
	def __init__(self, bot):
		self.bot = bot
		self.birthday.start()

	def cog_unload(self):
		self.birthday.cancel()

	@tasks.loop(seconds=1.0, count=1)
	async def birthday(self):
		guild = self.bot.get_guild(551753752781127680)
		channel = guild.get_channel(840003378062557202)
		if hour == "09":
			for i, data in enumerate(date_student):
				if day in data:
					if month in data:
						year_birth = year - int(year_date_students[i])
						message = ("Bon anniversaire **<@!" + ID_users[i] + ">**, tu es né(e) le " + data + " et tu as désormais " + str(year_birth) + " ans ! 🎉")
      
						embed = discord.Embed(title="Bon anniversaire !", colour=discord.Colour.dark_gold())
						embed.add_field(name="Wow c'est ton anniversaire aujourd'hui !", value=message, inline=False)
						embed.set_thumbnail(url="https://acegif.com/wp-content/gif/joyeux-anniversaire-chat-31.gif")
						await channel.send(embed=embed)
			else:
				await channel.send("Il n'y a pas d'anniversaire aujourd'hui :(")

	@birthday.before_loop
	async def before_printer(self):
		await self.bot.wait_until_ready()

	@commands.command(name='birthdayall', aliases=['bda'])
	async def birthdayall(self, ctx):
		embed=discord.Embed(title="All birthdays", colour=discord.Colour.dark_gold())
		embed.set_thumbnail(url="https://stickeramoi.com/8365-large_default/sticker-mural-couronne-jaune.jpg")
		embed.add_field(name="Clémentine", value="27/02/1999", inline=True)
		embed.add_field(name="Caton", value="02/04/1999", inline=True)
		embed.add_field(name="Max", value="21/04/2002", inline=True)
		embed.add_field(name="Eloi", value="11/05/2003", inline=True)
		embed.add_field(name="Louis", value="27/07/2002", inline=True)
		embed.add_field(name="Ivan", value="27/07/1999", inline=True)
		embed.add_field(name="Laurent", value="26/09/2002", inline=True)
		embed.add_field(name="Aurélien", value="23/10/2002", inline=True)
		embed.add_field(name="Karine", value="13/11/1985", inline=True)
		embed.add_field(name="Paul", value="14/11/0666", inline=True)
		embed.add_field(name="Salaheddine", value="03/12/1997", inline=True)
		embed.add_field(name="Théo", value="18/12/2001", inline=True)
		embed.add_field(name="Romain", value="20/12/2002", inline=True)
		embed.set_footer(text="Requested by : "+str(ctx.message.author.name) +" "+ str(time.strftime('%H:%M:%S')), icon_url=ctx.message.author.avatar_url)
		await ctx.send(embed=embed)

	@commands.command(name='myage', aliases=['ma'])
	async def mydate(self, ctx):
		userID = str(ctx.message.author.id)
		for i, data2 in enumerate(ID_users):
			if userID in data2:
				year_birth = year - int(year_date_students[i])
				message = ("<@!" + data2 + "> tu es agé(e) de " + str(year_birth) + " ans ! 🎉")

				embed = discord.Embed(title="Bon anniversaire !", color=0x12F932)
				embed.add_field(name="Wow c'est ton anniversaire aujourd'hui !", value=message, inline=False)	
				embed.set_thumbnail(url="https://acegif.com/wp-content/gif/joyeux-anniversaire-chat-31.gif")
				embed.set_footer(text="Requested by : "+str(ctx.message.author.name) +" "+ str(time.strftime('%H:%M:%S')), icon_url=ctx.message.author.avatar_url)
				await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Birthday(bot))
