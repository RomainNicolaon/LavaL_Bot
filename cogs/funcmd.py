from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageChops
from io import BytesIO
from pytz import timezone
import discord
import random
from discord.ext import commands
from discord import Member
import aiohttp
import requests
from datetime import datetime
import json
from serpapi import GoogleSearch
from riotwatcher import LolWatcher, ApiError

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

		nekosbest_url = 'https://nekos.best/api/v2/hug'
		r = requests.get(nekosbest_url)
		link = r.json()
		link = json.dumps(link)
		python_obj = json.loads(link)
		result = python_obj["results"][0]

		anime_name = result["anime_name"]
		url = result["url"]

		embed = discord.Embed(title=f"{ctx.author.name} fait un gros câlin à {member.name}#{member.discriminator}", description="", color=0x83B5E3)

		embed.add_field(name="Provient de l'anime", value=anime_name, inline=True)

		embed.set_image(url=url)

		embed.add_field(name="API fournie par", value="[nekos.best](https://nekos.best/)", inline=True)

		embed.set_footer(text="Demandé par : "+str(ctx.message.author.name)+" à " +
						 Timer(), icon_url=ctx.message.author.display_avatar.url)

		await ctx.send(embed=embed)

	@commands.command(name='kiss')
	async def kiss(self, ctx, member: Member = None):
		"""Fais un bisous à quelqu'un ou à toi même"""
		if not member:
			member = ctx.author
		
		nekosbest_url = 'https://nekos.best/api/v2/kiss'
		r = requests.get(nekosbest_url)
		link = r.json()
		link = json.dumps(link)
		python_obj = json.loads(link)
		result = python_obj["results"][0]

		anime_name = result["anime_name"]
		url = result["url"]

		embed = discord.Embed(title=f"{ctx.author.name} embrasse passionnément {member.name}#{member.discriminator}", description="", color=0x83B5E3)

		embed.add_field(name="Provient de l'anime", value=anime_name, inline=True)

		embed.set_image(url=url)

		embed.add_field(name="API fournie par", value="[nekos.best](https://nekos.best/)", inline=True)

		embed.set_footer(text="Demandé par : "+str(ctx.message.author.name)+" à " +
						 Timer(), icon_url=ctx.message.author.display_avatar.url)

		await ctx.send(embed=embed)

	@commands.command(name='punch')
	async def punch(self, ctx, member: Member = None):
		"""Met un coup de poing à quelqu'un ou à toi même"""
		if not member:
			member = ctx.author
		
		nekosbest_url = 'https://anime-api.hisoka17.repl.co/img/punch'
		r = requests.get(nekosbest_url)
		link = r.json()
		link = json.dumps(link)
		python_obj = json.loads(link)

		url = python_obj["url"]

		embed = discord.Embed(title=f"{ctx.author.name} frappe violemment {member.name}#{member.discriminator}", description="", color=0x83B5E3)

		embed.set_image(url=url)

		embed.add_field(name="API fournie par", value="[anime-api.hisoka17](https://anime-api.hisoka17.repl.co)", inline=True)

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

	@commands.command(name='card')
	async def card(self, ctx, member: discord.Member = None):
		"""Affiche une carte de profil (soi même ou un utilisateur)"""
		if not member:
			member = ctx.author

		try:
			user = await self.bot.fetch_user(member.id)
			user_banner = user.banner.url
		except: 
			user_banner = None

		def circle(pfp,size = (215,215)):
			pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
			bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
			mask = Image.new('L', bigsize, 0)
			draw = ImageDraw.Draw(mask) 
			draw.ellipse((0, 0) + bigsize, fill=255)
			mask = mask.resize(pfp.size, Image.ANTIALIAS)
			mask = ImageChops.darker(mask, pfp.split()[-1])
			pfp.putalpha(mask)
			return pfp

		name, nick, Id, status = str(member), member.display_name, str(member.id), str(member.status).upper()

		created_at = member.created_at.strftime("%a %b\n%B %Y")
		joined_at = member.joined_at.strftime("%a %b\n%B %Y")

		yes, no = "Yes", "No"
		nitro, is_robot = yes if member.premium_since else no, yes if member.bot else no
		bg_list = ["img/bg1.png", "img/bg2.png", "img/bg3.png", "img/bg4.png", "img/bg5.png", "img/bg6.png"]
		base = Image.open("img/base.png").convert("RGBA")
		background = Image.open(random.choice(bg_list)).convert("RGBA")

		pfp = member.display_avatar
		data = BytesIO(await pfp.read())
		pfp = Image.open(data).convert("RGBA")

		banner = Image.open(BytesIO(requests.get(user_banner).content)).resize(background.size, Image.ANTIALIAS).convert("RGBA") if user_banner else background
  
		name = f"{name[:16]}.." if len(name) > 16 else name
		nick = f"AKA - {nick[:17]}.." if len(nick) > 17 else f"AKA - {nick}"

		draw = ImageDraw.Draw(base)
		pfp = circle(pfp, (215, 215))
		font = ImageFont.truetype("arial.ttf", 38)
		akafont = ImageFont.truetype("arial.ttf", 30)
		subfont = ImageFont.truetype("arial.ttf", 25)

		draw.text((280, 240), name, font = font)
		draw.text((270, 315), nick, font = akafont)
		draw.text((65, 490), Id, font = subfont)
		draw.text((405, 490), status, font = subfont)
		draw.text((65, 635), nitro, font = subfont)
		draw.text((405, 635), is_robot, font = subfont)
		draw.text((65, 770), created_at, font = subfont)
		draw.text((405, 770), joined_at, font = subfont)

		base.paste(pfp, (56, 158), pfp)
		banner.paste(base, (0, 0), base)

		with BytesIO() as a:
			banner.save(a, 'PNG')
			a.seek(0)
			await ctx.send(file = discord.File(a, "profile.png"))

	@commands.command(name='actualgame', aliases=['ag'])
	async def actual_game(self, ctx, member: Member = None):
		"""Affiche l'activité de quelqu'un ou de soi même (**EN DEVELEPPEMENT)**"""
		if not member:
			member = ctx.author

		try:
			game = member.activity.name
			details = member.activity.details
			state = member.activity.state
			s1 = Timer()
			s2 = member.activity.start
			s3 = s2.astimezone(timezone('Europe/berlin')).strftime('%H:%M:%S')
			FMT = '%H:%M:%S'
			start = datetime.strptime(s1, FMT) - datetime.strptime(s3, FMT)
			url = member.activity.large_image_url
		
			embed = discord.Embed(title=f"Affiche l'activité de {member.name}#{member.discriminator}", description="", color=discord.Colour.yellow())

			embed.add_field(name='__Joue à__ : ', value=game, inline=False)
			
			embed.add_field(name='__Détails__ : ', value=details, inline=False)
			
			embed.add_field(name='__Sous détails__ : ', value=state, inline=False)
			
			embed.add_field(name='__Depuis__ : ', value=start, inline=False)

			embed.set_thumbnail(url=url)
			
			embed.set_footer(text="Demandé par : "+str(ctx.message.author.name)+" à " +
							Timer(), icon_url=ctx.message.author.display_avatar.url)

			await ctx.send(embed=embed)

		except Exception:
			await ctx.send(f"{member.name} n'est pas en activité pour le moment, essaye en jouant à un jeu par exemple. (PS : Si vous avez Spotify d'actif, mettez votre musique en **pause**)")


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

	@commands.command(name='eval')
	async def waifurate(self, ctx, *waifu: commands.Greedy[discord.Member]):
		"""Évalue la/les personnes(s) mentionnée(s)."""

		waifu_text = "waifu"

		if not waifu:
			return await ctx.send("Vous n'avez mentionné personne que je puisse noter.")
		elif len(waifu) >= 20:
			return await ctx.send("Je pense que tu as trop de {} :thinking: Je ne vais même pas essayer de noter ça (gros weeb).".format(waifu_text))

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

	@commands.command(name='anilist', aliases=['anl'])
	async def anime(self, ctx, *, animeName: str):
		"""Recherche un anime sur AniList.co et renvoie les informations de base"""

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
    
	@commands.command(name='neko', aliases=['nk'])
	async def neko(self, ctx):
		"""Renvoie une image de neko"""
		nekosbest_url = 'https://nekos.best/api/v2/neko'
		r = requests.get(nekosbest_url)
		link = r.json()
		link = json.dumps(link)
		python_obj = json.loads(link)
		result = python_obj["results"][0]

		artist_href = result["artist_href"]
		artist_name = result["artist_name"]
		source_url = result["source_url"]
		url = result["url"]

		embed = discord.Embed(title="Neko", color=0xE01DE3)
		embed.add_field(name="Artist", value=f"[{artist_name}]({artist_href})", inline=True)
		embed.set_image(url=url)
		embed.add_field(name="Source", value=f"[url]({source_url})", inline=True)
		embed.add_field(name="API fournie par", value="[nekos.best](https://nekos.best/)")
		await ctx.send(embed=embed)

	@commands.command(name='kitsune', aliases=['ks'])
	async def kitsune(self, ctx):
		"""Renvoie une image de kitsune"""
		nekosbest_url = 'https://nekos.best/api/v2/kitsune'
		r = requests.get(nekosbest_url)
		link = r.json()
		link = json.dumps(link)
		python_obj = json.loads(link)
		result = python_obj["results"][0]

		artist_href = result["artist_href"]
		artist_name = result["artist_name"]
		source_url = result["source_url"]
		url = result["url"]

		embed = discord.Embed(title="Kitsune", color=0xE01DE3)
		embed.add_field(name="Artist", value=f"[{artist_name}]({artist_href})", inline=True)
		embed.set_image(url=url)
		embed.add_field(name="Source", value=f"[url]({source_url})", inline=True)
		embed.add_field(name="API fournie par", value="[nekos.best](https://nekos.best/)")
		await ctx.send(embed=embed)

	@commands.command(name='waifu', aliases=['wf'])
	async def waifu(self, ctx):
		"""Renvoie une image de waifu"""
		nekosbest_url = 'https://nekos.best/api/v2/waifu'
		r = requests.get(nekosbest_url)
		link = r.json()
		link = json.dumps(link)
		python_obj = json.loads(link)
		result = python_obj["results"][0]

		artist_href = result["artist_href"]
		artist_name = result["artist_name"]
		source_url = result["source_url"]
		url = result["url"]

		embed = discord.Embed(title="Waifu", color=0xE01DE3)
		embed.add_field(name="Artist", value=f"[{artist_name}]({artist_href})", inline=True)
		embed.set_image(url=url)
		embed.add_field(name="Source", value=f"[url]({source_url})", inline=True)
		embed.add_field(name="API fournie par", value="[nekos.best](https://nekos.best/)")
		await ctx.send(embed=embed)

	@commands.command(name='searchanimecharacter', aliases=['sac'])
	async def searchanimecharacter(self, ctx, name:str):
		"""Recherche un personnage ou une personne"""
		try:
			waifu_picst_url = 'https://animechan.vercel.app/api/quotes/character?name=' + name
			r = requests.get(waifu_picst_url)
			link = r.json()
			link = json.dumps(link)
			python_obj = json.loads(link)
			result = python_obj[0]

			anime_name = result["anime"]
			character_name = result["character"]

			embed = discord.Embed(title="Résultat de la recherche", color=0xbf79b4)
			embed.add_field(name="Nom de l'anime", value=anime_name, inline=True)
			embed.add_field(name="Nom du personnage", value=character_name, inline=True)
			embed.add_field(name="APIs fournies par", value="[animechan.vercel.app](https://animechan.vercel.app/)")
			await ctx.send(embed=embed)

		except:
			raise await ctx.reply("<a:no_animated:844992804480352257> Je n'ai pas trouvé de personnage correspondant !")

	@commands.command(name='searchongoogle', aliases=['sog'])
	async def searchongoogle(self, ctx, *, name:str):
		"""Recherche un personnage ou une personne"""
		params = {
			"api_key": "39454ef7b5a47ea83565a9e58cb5ca97484325e8de57168725234b272eb89838",
			"engine": "google",
			"ijn": "0",
			"q": name,
			"google_domain": "google.com",
			"tbm": "isch"
		}

		search = GoogleSearch(params)
		results = search.get_dict()
		num = 0
		images_results = results['images_results'][num]
		original = images_results['original']

		embed = discord.Embed(title="Résultat de la recherche", color=0xcc80cc)
		embed.add_field(name="Nom", value=name.title(), inline=True)
		embed.set_image(url=original)
		embed.add_field(name="API fournie par", value="[google](https://www.google.com/)")
		await ctx.send(embed=embed)
  
	@commands.command(name='hentai', aliases=['hen'])
	async def hentai(self, ctx):
		"""Renvoie une image/gif de hentai"""
		hentai_url = 'https://anime-api.hisoka17.repl.co/img/nsfw/hentai'
		r = requests.get(hentai_url)
		link = r.json()
		link = json.dumps(link)
		python_obj = json.loads(link)
		url = python_obj["url"]

		embed = discord.Embed(title="Hentai", color=0xE01DE3)
		embed.set_image(url=url)
		embed.add_field(name="API fournie par", value="[anime-api.hisoka17](https://anime-api.hisoka17.repl.co/)")
		await ctx.send(embed=embed)
  
	@commands.command(name='lolprofil', aliases=['lol'])
	async def lolprofil(self, ctx, *, username:str):
		"""Renvoie le profil de League of Legends"""
		lol_watcher = LolWatcher('RGAPI-e2690840-0500-4689-bd01-379f84847eac')
		my_region = 'euw1'

		try:
			me = lol_watcher.summoner.by_name(my_region, username)

			# Get the summoner's name, level, and profile picture URL
			name = me['name']
			summoner_lvl = me['summonerLevel']
			profile_icon_id = me["profileIconId"]
			version = 'https://ddragon.leagueoflegends.com/api/versions.json'
			r = requests.get(version)
			link = r.json()
			link = json.dumps(link)
			python_obj = json.loads(link)
			latest_version = python_obj[0]
			profil_picture_url = f'https://ddragon.leagueoflegends.com/cdn/{latest_version}/img/profileicon/{profile_icon_id}.png'
	
			# Get the summoner's ranked stats
			my_ranked_stats = lol_watcher.league.by_summoner(my_region, me['id'])
	
			embed = discord.Embed(title="Profil League of Legends", color=0xE01DE3)
			embed.add_field(name="Nom", value=name, inline=False)
			embed.add_field(name="Niveau", value=summoner_lvl, inline=False)

			try:
				# Solo/Duo
				for i in range(len(my_ranked_stats)):
					if my_ranked_stats[i]['queueType'] == 'RANKED_SOLO_5x5':
						queueType0 = my_ranked_stats[i]['queueType']
						tier0 = my_ranked_stats[i]['tier']
						rank0 = my_ranked_stats[i]['rank']
						lp0 = my_ranked_stats[i]['leaguePoints']
						wins0 = my_ranked_stats[i]['wins']
						losses0 = my_ranked_stats[i]['losses']
					if my_ranked_stats[i]['queueType'] == 'RANKED_FLEX_SR':
						queueType1 = my_ranked_stats[i]['queueType']
						tier1 = my_ranked_stats[i]['tier']
						rank1 = my_ranked_stats[i]['rank']
						lp1 = my_ranked_stats[i]['leaguePoints']
						wins1 = my_ranked_stats[i]['wins']
						losses1 = my_ranked_stats[i]['losses']

				embed.add_field(name=queueType0, value=f"{tier0} {rank0} {lp0} LP", inline=False)
				embed.add_field(name="Victoires", value=wins0, inline=True)
				embed.add_field(name="Défaites", value=losses0, inline=True)

				embed.add_field(name=queueType1, value=f"{tier1} {rank1} {lp1} LP", inline=False)
				embed.add_field(name="Victoires", value=wins1, inline=True)
				embed.add_field(name="Défaites", value=losses1, inline=True)

				embed.set_thumbnail(url=profil_picture_url)
				await ctx.send(embed=embed)

			except:
				await ctx.send("<a:no_animated:844992804480352257> Vous n'avez pas fait de parties en ranked.")
		except:
			await ctx.send("<a:no_animated:844992804480352257> Vous n'avez pas de compte League of Legends.")
		
def setup(bot):
	bot.add_cog(Funcmd(bot))
