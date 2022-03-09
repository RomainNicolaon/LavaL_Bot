from datetime import datetime, date
from unicodedata import name
from pytz import timezone
import discord
import random
from discord.ext import commands
from discord import Member
import aiohttp

def Timer():
	fmt = "%H:%M:%S"
	# Current time in UTC
	now_utc = datetime.now(timezone('UTC'))
	now_berlin = now_utc.astimezone(timezone('Europe/berlin'))
	actual_time = now_berlin.strftime(fmt)
	return actual_time

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
		"""Affiche la photo de profil (soi même ou un utilisateur)"""
		if not member:
			member = ctx.author
		pfp = member.display_avatar.url
		embed = discord.Embed(title=f"Affiche la photo de profile de {member.name}#{member.discriminator}", color=0x00000, description=f"[Avatar URL]({pfp})")

		embed.set_image(url=pfp)

		embed.set_footer(text="Demandé par : "+str(ctx.message.author.name)+" à " +
						 Timer(), icon_url=ctx.message.author.display_avatar.url)

		await ctx.send(embed=embed)

	@commands.command(name='hug')
	async def hug(self, ctx, member: Member = None):
		"""Fais un calin à quelqu'un ou à toi même"""
		if not member:
			member = ctx.author
		gif_hug = random.choice([
			"https://cdn.zerotwo.dev/HUG/9300c260-931c-4572-9a11-9a0f1f54735d.gif", "https://media.giphy.com/media/fvN5KrNcKKUyX7hNIA/giphy.gif",
			"https://media.giphy.com/media/kooPUWvhaGe7C/giphy.gif",
			"https://media.giphy.com/media/3EJsCqoEiq6n6/giphy.gif",
			"https://cdn.zerotwo.dev/HUG/e2d1bb44-d211-423e-9130-ad86dc29c882.gif"
		])

		embed = discord.Embed(title=f"{ctx.author.name} fait un gros câlin à {member.name}#{member.discriminator}", description="", color=0x83B5E3)

		embed.set_image(url=gif_hug)

		embed.set_footer(text="Demandé par : "+str(ctx.message.author.name)+" à " +
						 Timer(), icon_url=ctx.message.author.display_avatar.url)

		await ctx.send(embed=embed)

	@commands.command(name='kiss')
	async def kiss(self, ctx, member: Member = None):
		"""Fais un bisous à quelqu'un ou à toi même"""
		if not member:
			member = ctx.author
		gif_kiss = random.choice([
			"https://cdn.zerotwo.dev/KISS/1afe24ba-5014-4ddd-9222-5969076e9de3.gif",
			"https://cdn.zerotwo.dev/KISS/1a43ff80-a5ca-4e78-929b-09714a51b557.gif",
			"https://cdn.zerotwo.dev/KISS/c769d606-869d-48c7-8fc7-a531010bcb27.gif",
			"https://cdn.zerotwo.dev/KISS/8b7dbe1a-ad13-48bf-9142-a9db21748f12.gif"
		])

		embed = discord.Embed(title=f"{ctx.author.name} embrasse passionnément {member.name}#{member.discriminator}", description="", color=0x83B5E3)

		embed.set_image(url=gif_kiss)

		embed.set_footer(text="Demandé par : "+str(ctx.message.author.name)+" à " +
						 Timer(), icon_url=ctx.message.author.display_avatar.url)

		await ctx.send(embed=embed)

	@commands.command(name='punch')
	async def punch(self, ctx, member: Member = None):
		"""Met un coup de poing à quelqu'un ou à toi même"""
		if not member:
			member = ctx.author
		gif_punch = random.choice([
			"https://media.giphy.com/media/Z5zuypybI5dYc/giphy.gif",
			"https://media.discordyui.net/reactions/slap/6784568.gif",
			"https://media.discordyui.net/reactions/slap/aVDQEfA.gif"
		])

		embed = discord.Embed(title=f"{ctx.author.name} frappe violemment {member.name}#{member.discriminator}", description="", color=0x83B5E3)

		embed.set_image(url=gif_punch)

		embed.set_footer(text="Demandé par : "+str(ctx.message.author.name)+" à " +
						 Timer(), icon_url=ctx.message.author.display_avatar.url)

		await ctx.send(embed=embed)

	@commands.command(name='banner', aliases=['b', 'bnr'])
	async def getbanner(self, ctx, member: Member = None):
		"""Affiche la bannière de profil (soi même ou un utilisateur)"""
		if not member:
			member = ctx.author
		usr = await self.bot.fetch_user(member.id)
		banner = usr.banner.url if usr.banner else await commands.CommandError("Hmm cet utilisateur n'a pas de bannière personalisée")
		embed = discord.Embed(title=f"Affiche la bannière de profile de {member.name}#{member.discriminator}", color=0x00000, description=f"[Banner URL]({banner})")

		embed.set_image(url=banner)

		embed.set_footer(text="Demandé par : "+str(ctx.message.author.name)+" à " +
						 Timer(), icon_url=ctx.message.author.display_avatar.url)

		await ctx.send(embed=embed)

	@commands.command(name='lookup', aliases=['lu'])
	async def lookup(self, ctx, member: Member = None):
		"""Affiche des information sur un compte Discord"""
		if not member:
			member = ctx.author
		pfp = member.display_avatar.url
		creation_date = member.created_at.strftime("%A %-d %B %Y at %H:%M:%S")
		embed = discord.Embed(title=f"Affiche des information sur le compte de {member.name}#{member.discriminator}")
		embed.add_field(name="ID", value=member.id, inline=True)
		embed.add_field(name="Créé depuis le :", value=str(creation_date), inline=True)
		embed.set_thumbnail(url=pfp)
		await ctx.send(embed=embed)

	@commands.command(name='actual_game', aliases=['ag'])
	async def actual_game(self, ctx, member: Member = None):
		"""Affiche l'activité de quelqu'un ou de soi même"""
		if not member:
			member = ctx.author
		
		embed = discord.Embed(title=f"Affiche l'activité de {member.name}#{member.discriminator}", description="", color=discord.Colour.yellow())

		embed.add_field(name='__Joue à__ : ', value=member.activity.name, inline=False)
		
		embed.add_field(name='__Détails__ : ', value=member.activity.details, inline=False)
		
		embed.add_field(name='__Sous détails__ : ', value=member.activity.state, inline=False)
		
		embed.add_field(name='__Depuis__ : ', value=member.activity.start.strftime("%H:%M:%S"), inline=False)
		
		embed.set_thumbnail(url=member.activity.large_image_url)
		
		embed.set_footer(text="Demandé par : "+str(ctx.message.author.name)+" à " +
						 Timer(), icon_url=ctx.message.author.display_avatar.url)

		if not member.activity.start:
			raise commands.CommandError("Tu n'as pas d'activité pour le moment, essaye en jouant à un jeu par exemple")
		else:
			await ctx.send(embed=embed)


	@commands.command(name='time')
	async def time(self, ctx):
		"""Affiche l'heure actuelle en France"""
		await ctx.reply(Timer())

	@commands.command(name='rickroll', aliases=['rr'])
	async def rickroll(self, ctx, member: Member = None):
		"""Troll quelqu'un ou toi même avec un rickroll"""
		lyrics = ["Never gonna give you up",
					"Never gonna let you down",
					"Never gonna run around and desert you",
					"Never gonna say goodbye"]
		embed = discord.Embed(title=f'{random.choice(lyrics)}', description=f"{ctx.author.name} rickroled {member.name}#{member.discriminator}", color=0x00ff00)
		embed.set_image(url="https://c.tenor.com/Z6gmDPeM6dgAAAAC/dance-moves.gif")
		await ctx.send(embed=embed)

	@commands.command(name='', aliases=['eval'])
	async def waifurate(self, ctx, *waifu: commands.Greedy[discord.Member]):
		"""
		Évalue la/les personnes(s) mentionnée(s).
		En utilisant les alias `husbandorate` ou `spousurate`, cela changera la façon dont LavaL Bot s'adresse aux personnes évaluées.
		Cela peut permettre à plusieurs personnes d'être évaluées en même temps :eyes :
		Exemple :
			?waifurate @user#9999
		Cette commande est dédiée à Hannah, qui a eu l'idée de cette commande. J'espère qu'elle est en train de faire évaluer ses waifus en paix.
		"""

		waifu_text = "waifu"

		if not waifu:
			return await ctx.send("Vous n'avez mentionné personne que je puisse noter.")
		elif len(waifu) >= 20:
			return await ctx.send("Je pense que tu as trop de {} :pensée : Je ne vais même pas essayer de noter ça (gros weeb).".format(waifu_text))

		rating = random.randrange(1, 11)
		if rating <= 2:
			emoji = ":sob:"
		elif rating <= 4:
			emoji = ":disappointed:"
		elif rating <= 6:
			emoji = ":thinking:"
		elif rating <= 8:
			emoji = ":blush:"
		elif rating == 9:
			emoji = ":kissing_heart:"
		else:
			emoji = ":heart_eyes:"

		waifu_list = []
		for x, w in enumerate(waifu):
			if w.name not in waifu_list:
				waifu_list.append(w.name)

		if len(waifu_list) > 1:
			if len(waifu_list) == 2:
				oxford_comma = " and {}"
			else:
				oxford_comma = ", and {}"

			waifus = ", ".join(waifu_list[:-1]).strip(", ") + oxford_comma.format(waifu_list[-1])
			return await ctx.send("Oh poly {0} rating? :smirk: Your combined {0} rating for {3} is {1}/10. {2}".format(waifu_text, rating, emoji, waifus))
		else:
			return await ctx.send("Oh that's your {}? I rate {} a {}/10. {}".format(waifu_text, waifu[0].name, rating, emoji))

	@commands.command(name='searchimage', aliases=['si'])
	async def searchimage(ctx, file_name):
		search_result = 'Search Results:'
		from os import listdir
		for file in listdir('data'):
			if file_name in file.lower():
				search_result = search_result+'\n'+file
		if search_result == 'Search Results:':
			await ctx.send('Error: Not matched with any file.')
		else:
			await ctx.send(search_result)

	@commands.command(name='anilist', aliases=['anl'])
	async def anime(self, ctx, *, animeName: str):
		""""Recherche un anime sur AniList.co et renvoie les informations de base"""

		api = 'https://graphql.anilist.co'
		query = '''
		query ($name: String){
		  Media(search: $name, type: ANIME) {
			id
			idMal
			description
			title {
			  romaji
			  english
			}
			coverImage {
			  large
			}
			startDate {
			  year
			  month
			  day
			}
			endDate {
			  year
			  month
			  day
			}
			synonyms
			format
			status
			episodes
			duration
			nextAiringEpisode {
			  episode
			}
			averageScore
			meanScore
			source
			genres
			tags {
			  name
			}
			studios(isMain: true) {
			  nodes {
				name
			  }
			}
			siteUrl
		  }
		}
		'''
		variables = {
			'name': animeName
		}

		async with aiohttp.ClientSession() as session:
			async with session.post(api, json={'query': query, 'variables': variables}) as r:
				if r.status == 200:
					json = await r.json()
					data = json['data']['Media']

					embed = discord.Embed(color=ctx.author.top_role.colour)
					embed.set_footer(text='API fourni par AniList.co | ID: {}'.format(str(data['id'])))
					embed.set_thumbnail(url=data['coverImage']['large'])
					if data['title']['english'] == None or data['title']['english'] == data['title']['romaji']:
						embed.add_field(name='Titre', value=data['title']['romaji'], inline=False)
					else:
						embed.add_field(name='Titre', value='{} ({})'.format(data['title']['english'], data['title']['romaji']), inline=False)

					embed.add_field(name='Description', value=data['description'].replace("<br>", ''), inline=False)

					embed.add_field(name='Type', value=data['format'].replace('_', ' ').title().replace('Tv', 'TV'), inline=True)
					if data['episodes'] > 1:
						embed.add_field(name="Nombre d'épisodes", value='{} ep de {} min'.format(data['episodes'], data['duration']), inline=True)
					else:
						embed.add_field(name='Durée', value=str(data['duration']) + ' min', inline=True)

					embed.add_field(name='Status', value=data['status'].replace('_', ' ').title(), inline=True)

					embed.add_field(name='Date de début', value='{}.{}.{}'.format(data['startDate']['day'], data['startDate']['month'], data['startDate']['year']), inline=True)
					if data['endDate']['day'] == None:
						embed.add_field(name='Épisodes diffusés', value=data['nextAiringEpisode']['episode'] - 1, inline=True)
					elif data['episodes'] > 1:
						embed.add_field(name='Date de fin', value='{}.{}.{}'.format(data['endDate']['day'], data['endDate']['month'], data['endDate']['year']), inline=True)

					try:
						embed.add_field(name='Studio principal', value=data['studios']['nodes'][0]['name'], inline=True)
					except IndexError:
						pass
					embed.add_field(name='Score (%)', value=data['averageScore'], inline=True)
					embed.add_field(name='Genres', value=', '.join(data['genres']), inline=False)
					tags = ''
					for tag in data['tags']:
						tags += tag['name'] + ', '
					embed.add_field(name='Tags', value=tags[:-2], inline=False)
					try:
						embed.add_field(name='Adapté de', value=data['source'].replace('_', ' ').title(), inline=True)
					except AttributeError:
						pass

					embed.add_field(name='Lien AniList', value=data['siteUrl'], inline=False)
					embed.add_field(name='Lien MyAnimeList', value='https://myanimelist.net/anime/' + str(data['idMal']), inline=False)
					await ctx.send(embed=embed)

				else:
					await ctx.send(":x: Je n'ai pas trouvé d'anime correspondant !")
		
def setup(bot):
	bot.add_cog(Funcmd(bot))
