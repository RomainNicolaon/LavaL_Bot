import os
import discord
import random
# import time
import asyncio
from discord.ext import tasks, commands
from discord.ext.commands import has_permissions
from discord import Member
from datetime import datetime
from pytz import timezone
from keep_alive import keep_alive

intents = discord.Intents().all()
intents.presences = True
intents.members = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("."), description='LavaL Bot', intents=intents)
bot.remove_command('help')

fmt = "%d-%m-%Y at %H:%M:%S"
hour = "%H:%M:%S"
# Current time in UTC
now_utc = datetime.now(timezone('UTC'))
now_berlin = now_utc.astimezone(timezone('Europe/berlin'))
local_time = now_berlin.strftime(fmt)
local_hour = now_berlin.strftime(hour)
# local_time = str(time.strftime('%d-%m-%Y at %H:%M:%S'))

# ----------------------------------------------------

@bot.event
async def on_ready():
	print('Connection en cours...')
	print("Link Start")
	await bot.change_presence(activity=discord.Game(name='Fais de la Dé'))

@bot.event
async def on_member_join(member):
	await member.send("👋 Bienvenue sur le serveur : " + str(member.guild.name) + " !")
  

@bot.event
async def on_member_remove(member):
	await member.send("😢 Vous avez quitté le serveur : " + str(member.guild.name) + ". Nous espérons que vous reviendrez vite !")


@bot.command(name="help", aliases=["h","."])
async def help(ctx):
	page1 = discord.Embed (
		title = 'Commandes disponibles',
		description = 'Page 1/3',
		colour = discord.Colour.orange())
	page1.add_field(name="```.help``` ```.?``` ```;h```", value="Liste de toute les commandes")
	page1.add_field(name="```.infos``` ```.i```", value="Donne des informations sur le bot")
	page1.add_field(name="```.streamers``` ```.str```", value="Affiche tout vos streamers préférés")

	page2 = discord.Embed (
		title = 'Commandes disponibles',
		description = 'Page 2/3',
		colour = discord.Colour.orange())
	page2.add_field(name="```.server``` ```.serv``` ```.s```", value="Donne des informations sur le serveur")
	page2.add_field(name="```.avatar``` ```.a```", value="Affiche la photo de profil de la personne mentionnée")
	page2.add_field(name="```.punch```", value="Frappe violemment la personne mentionnée")

	page3 = discord.Embed (
		title = 'Commandes disponibles',
		description = 'Page 3/3',
		colour = discord.Colour.orange())
	page3.add_field(name="```.kiss```", value="Embrasse passionnément la personne mentionnée")
	page3.add_field(name="```.hug```", value="Faire un gros câlin à la personne mentionnée")
	page3.add_field(name="```.del``` ```.-```", value="Supprimer n messages (uniquement utilisable par les admins)")

  
	pages = [page1, page2, page3]

	message = await ctx.send(embed = page1)
	await message.add_reaction('⏮')
	await message.add_reaction('◀')
	await message.add_reaction('▶')
	await message.add_reaction('⏭')

	def check(reaction, user):
			return user == ctx.author

	i = 0
	reaction = None

	while True:
			if str(reaction) == '⏮':
						i = 0
						await message.edit(embed = pages[i])
			elif str(reaction) == '◀':
					if i > 0:
							i -= 1
							await message.edit(embed = pages[i])
			elif str(reaction) == '▶':
					if i < 2:
							i += 1
							await message.edit(embed = pages[i])
			elif str(reaction) == '⏭':
					i = 2
					await message.edit(embed = pages[i])

			try:
					reaction, user = await bot.wait_for('reaction_add', timeout = 30.0, check = check)
					await message.remove_reaction(reaction, user)
			except:
				break

	await message.clear_reactions()


@bot.command(name="infos", aliases=["i"])
async def infos(ctx):
  embed = discord.Embed(title="Donne des informations sur moi", color=0x4F2B10, description="Ceci n'est pas la version finale ! \nYo, je suis le bot de <@!405414058775412746>, pour m'utiliser, tapez la commande : \n```.help``` ```.?```  ```.h```", colour=discord.Colour(0x4F2B10))

  embed.set_thumbnail(url="https://steemitimages.com/DQmbQ9tUdvP98ruzMX6gCjXWz6N5yMBHbn7oJ1WeiiQoj68/16361360.png")

  embed.set_footer(text="Requested by : "+str(ctx.message.author.name) +" "+ local_time, icon_url=ctx.message.author.avatar_url)

  await ctx.send(embed=embed)


@bot.command(name="del", pass_context=True, aliases=['-'])
@has_permissions(manage_messages=True)
async def _delete(ctx, number_of_messages: int):
  messages = await ctx.channel.history(limit=number_of_messages + 1).flatten()

  for each_message in messages:
      await each_message.delete()


@bot.command(name='streamers', aliases=['str'])
async def streamers(ctx):
  embed = discord.Embed(title="Streamers", description="Liste de vos Streamers préférés", color=0xE019F7, colour=discord.Colour(0xE019F7))

  embed.add_field(name="LavaL", value="https://www.twitch.tv/laval_tv", inline=False)

  embed.add_field(name="Rony", value="https://www.twitch.tv/ronytv_", inline=False)

  embed.set_thumbnail(url="https://gdncoworldwidemedia.com/wp-content/uploads/2020/07/twitch_web.png")

  embed.set_footer(text="Requested by : "+str(ctx.message.author.name) +" "+ local_time, icon_url=ctx.message.author.avatar_url)

  await ctx.send(embed=embed)


@bot.command(name='server', aliases=['serv','s'])
async def server(ctx):
  embed = discord.Embed(title="Donne des informations sur le serveur", color=0x12F932, description="Ce serveur s'appelle "+str(ctx.message.guild.name)+" et totalise "+str(ctx.message.guild.member_count)+" membres et son créateur est <@!" + str(ctx.message.guild.owner_id)+">.", colour=discord.Colour(0x12F932))

  embed.set_thumbnail(url="https://steemitimages.com/DQmbQ9tUdvP98ruzMX6gCjXWz6N5yMBHbn7oJ1WeiiQoj68/16361360.png")

  embed.set_footer(text="Requested by : "+str(ctx.message.author.name) +" "+ local_time, icon_url=ctx.message.author.avatar_url)

  await ctx.send(embed=embed)


@bot.command(name='avatar', aliases=['a'])
async def getpfp(ctx, member: Member = None):
  pfp = member.avatar_url
  if not member:
    member = ctx.author
  embed = discord.Embed(title=f"Affiche la photo de profile de {member.name}#{member.discriminator}", color=0x00000, description=f"[Avatar URL]({pfp})")

  embed.set_image(url=pfp)

  embed.set_footer(text="Requested by : "+str(ctx.message.author.name) +" "+ local_time, icon_url=ctx.message.author.avatar_url)

  await ctx.send(embed=embed)


@bot.command(name='hug')
async def hug(ctx, member: Member = None):
  gif_hug = random.choice([
    "https://cdn.zerotwo.dev/HUG/9300c260-931c-4572-9a11-9a0f1f54735d.gif", "https://media.giphy.com/media/fvN5KrNcKKUyX7hNIA/giphy.gif",
    "https://media.giphy.com/media/kooPUWvhaGe7C/giphy.gif",
    "https://media.giphy.com/media/3EJsCqoEiq6n6/giphy.gif",
    "https://cdn.zerotwo.dev/HUG/e2d1bb44-d211-423e-9130-ad86dc29c882.gif"
    ])

  embed = discord.Embed(title =f"{ctx.author.name} fait un gros câlin à {member.name}#{member.discriminator}", description="", color = 0x83B5E3)

  embed.set_image(url=gif_hug)

  embed.set_footer(text="Requested by : "+str(ctx.message.author.name) +" "+ local_time, icon_url=ctx.message.author.avatar_url)

  await ctx.send(embed=embed)

@bot.command(name='bdsm')
async def bdsm(ctx, member: Member = None):
  gif_hug = random.choice([
    "https://thumb-p6.xhcdn.com/a/sW-9_2RDDN6ItHh4HxiLBg/000/093/910/986_1000.gif", "https://thumb-p4.xhcdn.com/a/bS9AGQwGLstPdA3MKE6NVg/000/093/910/964_1000.gif",
    "https://thumb-p9.xhcdn.com/a/mcUUhvDD2Mu_69M4JHxlDg/000/093/910/949_1000.gif",
    "https://thumb-p9.xhcdn.com/a/iK473gM8hnZ4RzNAXrXwCg/000/093/910/959_1000.gif",
    "https://thumb-p0.xhcdn.com/a/YwH2byrzqI2bTll1OSrF5w/000/093/910/950_1000.gif"
    ])

  embed = discord.Embed(title =f"{ctx.author.name} baise salement {member.name}#{member.discriminator}", description="", color = 0x83B5E3)

  embed.set_image(url=gif_hug)

  embed.set_footer(text="Requested by : "+str(ctx.message.author.name) +" "+ local_time, icon_url=ctx.message.author.avatar_url)

  await ctx.send(embed=embed)

@bot.command(name='kiss')
async def kiss(ctx, member: Member = None):
  gif_kiss = random.choice([
    "https://cdn.zerotwo.dev/KISS/1afe24ba-5014-4ddd-9222-5969076e9de3.gif",
    "https://cdn.zerotwo.dev/KISS/1a43ff80-a5ca-4e78-929b-09714a51b557.gif",
    "https://cdn.zerotwo.dev/KISS/c769d606-869d-48c7-8fc7-a531010bcb27.gif",
    "https://cdn.zerotwo.dev/KISS/8b7dbe1a-ad13-48bf-9142-a9db21748f12.gif"
    ])

  embed = discord.Embed(title =f"{ctx.author.name} embrasse passionnément {member.name}#{member.discriminator}", description="", color = 0x83B5E3)

  embed.set_image(url=gif_kiss)

  embed.set_footer(text="Requested by : "+str(ctx.message.author.name) +" "+ local_time, icon_url=ctx.message.author.avatar_url)

  await ctx.send(embed=embed)


@bot.command(name='punch')
async def punch(ctx, member: Member = None):
  gif_punch = random.choice([
    "https://media.giphy.com/media/Z5zuypybI5dYc/giphy.gif",
    "https://media.discordyui.net/reactions/slap/6784568.gif",
    "https://media.discordyui.net/reactions/slap/aVDQEfA.gif"
    ])

  embed = discord.Embed(title =f"{ctx.author.name} frappe violemment {member.name}#{member.discriminator}", description="", color = 0x83B5E3)

  embed.set_image(url=gif_punch)

  embed.set_footer(text="Requested by : "+str(ctx.message.author.name) +" "+ local_time, icon_url=ctx.message.author.avatar_url)

  await ctx.send(embed=embed)


@bot.command(name="time")
async def timeNow(ctx):
  embed = discord.Embed(title ="Time Zone", description="", color = 0x00FF12)

  fmttime = "%d-%m-%Y ➔ %H:%M:%S"
  # Current time in UTC
  now_utc = datetime.now(timezone('UTC'))
  now_berlin = now_utc.astimezone(timezone('Europe/berlin'))
  now_london = now_utc.astimezone(timezone('Europe/London'))
  now_canada_east = now_utc.astimezone(timezone('Canada/Eastern'))

  embed.add_field(name="UTC", value=now_utc.strftime(fmttime) + " (UTC)")

  embed.add_field(name="Berlin", value=now_berlin.strftime(fmttime))

  embed.add_field(name="London", value=now_london.strftime(fmttime))

  embed.add_field(name="Canada", value=now_canada_east.strftime(fmttime))

  embed.set_footer(text="Requested by : "+str(ctx.message.author.name) +" "+ local_time, icon_url=ctx.message.author.avatar_url)

  await ctx.send(embed=embed)



async def db():
	while(True):
		date_student = ["20/12", "23/10", "27/07", "14/11", "02/04", "11/05", "26/09"]
		ID = ["<@!405414058775412746>", "<@!354321839234744320>", "<@!501471077709381643>", "<@!265148938091233293>", "<@!219156294974570497>", "<@!456516058984087583>", "<@248910730122756108>"]
		today_date = "26/09"
		choosen_time = "00:10"
		actual_time = local_hour
		channel = bot.get_channel(840003378062557202)
		# await channel.send("test")
		if actual_time == choosen_time:
			for i in range(7):
				if today_date == date_student[i]:
					await channel.send("Bon anniversaire " + ID[i] + ", tu es né(e) le " + date_student[i])
		await asyncio.sleep(60)


@bot.command(name='bda')
async def bda(ctx):
	embed=discord.Embed(title="All birthdays", color=0xff00e1)
	embed.set_thumbnail(url="https://stickeramoi.com/8365-large_default/sticker-mural-couronne-jaune.jpg")
	embed.add_field(name="Louis", value="27/07/2002", inline=False)
	embed.add_field(name="Romain", value="20/12/2002", inline=False)
	embed.add_field(name="Aurélien", value="23/10/2002", inline=False)
	embed.add_field(name="Paul", value="14/11/0666", inline=False)
	embed.add_field(name="Caton", value="02/04/1999", inline=False)
	embed.add_field(name="Eloi", value="11/05/2003", inline=False)
	embed.add_field(name="Laurent", value="26/09/2002", inline=False)
	embed.set_footer(text="Requested by : "+str(ctx.message.author.name) +" "+ local_time, icon_url=ctx.message.author.avatar_url)
	await ctx.send(embed=embed)

class MyCog(commands.Cog):
		def __init__(self):
			self.db.start()

		def cog_unload(self):
			self.db.cancel()

		@tasks.loop(seconds=30.0)
		async def db():
				date_student = ["20/12", "23/10", "27/07", "14/11", "02/04", "11/05", "26/09"]
				ID = ["<@!405414058775412746>", "<@!354321839234744320>", "<@!501471077709381643>", "<@!265148938091233293>", "<@!219156294974570497>", "<@!456516058984087583>", "<@248910730122756108>"]
				today_date = "26/09"
				choosen_time = "10:45"
				actual_time = local_hour
				channel = bot.get_channel(551753752781127682)
				# await channel.send("test")
				if actual_time == choosen_time:
					for i in range(7):
						if today_date == date_student[i]:
							await channel.send("Bon anniversaire " + ID[i] + ", tu es né(e) le " + date_student[i])
				pass
anniv = MyCog()


# ----------------------------------------------------

keep_alive()
bot.run(os.getenv("TOKEN"))