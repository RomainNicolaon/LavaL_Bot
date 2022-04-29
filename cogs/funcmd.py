from datetime import datetime
import time
from PIL import Image, ImageDraw, ImageFont, ImageChops
from io import BytesIO
from pytz import timezone
import discord
import random
from discord.ext import commands
from discord import CategoryChannel, app_commands
import aiohttp
import requests
from datetime import datetime
import json
from serpapi import GoogleSearch
from riotwatcher import LolWatcher
from discord.utils import get

lol_watcher = LolWatcher('RGAPI-36c98b83-b452-427e-bf19-10a2c4a4cb94')

class Funcmd(commands.Cog, name="funcmd"):
	"""
		Description des commandes pour le fun

		Require intents:
			- presences
		
		Require bot permission:
			- use_external_emojis
	"""

	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot
  
		self.lol_profile = bot.config["database"]["lolprofile"]

	def help_custom(self) -> tuple[str]:
		emoji = '<a:CatGunner:876156284557221929>'
		label = "Commandes Fun"
		description = "Commandes pour le fun, comme avatar, etc.."
		return emoji, label, description

	@app_commands.command(name="hug", description="Fais un calin à quelqu'un ou à toi même")
	@app_commands.describe(user="Fais un calin à cet utilisateur")
	@app_commands.checks.bot_has_permissions(embed_links=True)
	async def hug(self, interaction: discord.Interaction, user: discord.Member = None):
		"""Fais un calin à quelqu'un ou à toi même"""
		if not user:
			user = interaction.user

		nekosbest_url = 'https://nekos.best/api/v2/hug'
		r = requests.get(nekosbest_url)
		link = r.json()
		link = json.dumps(link)
		python_obj = json.loads(link)
		result = python_obj["results"][0]

		anime_name = result["anime_name"]
		url = result["url"]

		embed = discord.Embed(title=f"{interaction.user.name} fait un gros câlin à {user.name}#{user.discriminator}", description="", color=0x83B5E3)

		embed.add_field(name="Provient de l'anime", value=anime_name, inline=True)

		embed.set_image(url=url)

		embed.add_field(name="API fournie par", value="[nekos.best](https://nekos.best/)", inline=True)

		embed.set_footer(text=f"Demandé par : {str(interaction.user.name)} à {time.strftime('%H:%M:%S')}", icon_url=interaction.user.display_avatar.url)

		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="kiss", description="Fais un bisous à quelqu'un ou à toi même")
	@app_commands.describe(user="Fais un bisous à cet utilisateur.")
	@app_commands.checks.bot_has_permissions(embed_links=True)
	async def kiss(self, interaction: discord.Interaction, user: discord.Member = None):
		"""Fais un bisous à quelqu'un ou à toi même"""
		if not user:
			user = interaction.user

		nekosbest_url = 'https://nekos.best/api/v2/kiss'
		r = requests.get(nekosbest_url)
		link = r.json()
		link = json.dumps(link)
		python_obj = json.loads(link)
		result = python_obj["results"][0]

		anime_name = result["anime_name"]
		url = result["url"]

		embed = discord.Embed(title=f"{interaction.user.name} embrasse passionnément {user.name}#{user.discriminator}", description="", color=0x83B5E3)

		embed.add_field(name="Provient de l'anime", value=anime_name, inline=True)

		embed.set_image(url=url)

		embed.add_field(name="API fournie par", value="[nekos.best](https://nekos.best/)", inline=True)

		embed.set_footer(text=f"Demandé par : {str(interaction.user.name)} à {time.strftime('%H:%M:%S')}", icon_url=interaction.user.display_avatar.url)

		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="punch", description="Met un coup de poing à quelqu'un ou à toi même")
	@app_commands.describe(user="Met un coup de poing à cet utilisateur.")
	@app_commands.checks.bot_has_permissions(embed_links=True)
	async def punch(self, interaction: discord.Interaction, user: discord.Member = None):
		"""Met un coup de poing à quelqu'un ou à toi même"""
		if not user:
			user = interaction.user
		
		nekosbest_url = 'https://anime-api.hisoka17.repl.co/img/punch'
		r = requests.get(nekosbest_url)
		link = r.json()
		link = json.dumps(link)
		python_obj = json.loads(link)

		url = python_obj["url"]

		embed = discord.Embed(title=f"{interaction.user.name} frappe violemment {user.name}#{user.discriminator}", description="", color=0x83B5E3)

		embed.set_image(url=url)

		embed.add_field(name="API fournie par", value="[anime-api.hisoka17](https://anime-api.hisoka17.repl.co)", inline=True)

		embed.set_footer(text=f"Demandé par : {str(interaction.user.name)} à {time.strftime('%H:%M:%S')}", icon_url=interaction.user.display_avatar.url)

		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="card", description="Affiche la carte de profil (soi même ou un utilisateur)")
	@app_commands.describe(user="Affiche la carte de profil de cet utilisateur).")
	@app_commands.checks.bot_has_permissions(embed_links=True)
	async def card(self, interaction: discord.Interaction, user: discord.Member = None):
		"""Affiche la carte de profil (soi même ou un utilisateur)"""
		if not user:
			user = interaction.user
		
		realuser: discord.Member = get(user.guild.members, id=user.id)
  
		try:
			user = await self.bot.fetch_user(user.id)
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

		name, nick, Id, status = str(user), user.display_name, str(user.id), str(realuser.status).upper()

		created_at = realuser.created_at.strftime("%a %b\n%B %Y")
		joined_at = realuser.joined_at.strftime("%a %b\n%B %Y")

		yes, no = "Yes", "No"
		nitro, is_robot = yes if realuser.premium_since else no, yes if user.bot else no
		bg_list = ["img/bg1.png", "img/bg2.png", "img/bg3.png", "img/bg4.png", "img/bg5.png", "img/bg6.png"]
		base = Image.open("img/base.png").convert("RGBA")
		background = Image.open(random.choice(bg_list)).convert("RGBA")

		pfp = user.display_avatar
		data = BytesIO(await pfp.read())
		pfp = Image.open(data).convert("RGBA")

		banner = Image.open(BytesIO(requests.get(user_banner).content)).resize(background.size, Image.ANTIALIAS).convert("RGBA") if user_banner else background
  
		name = f"{name[:16]}.." if len(name) > 16 else name
		nick = f"AKA - {nick[:17]}.." if len(nick) > 17 else f"AKA - {nick}"

		draw = ImageDraw.Draw(base)
		pfp = circle(pfp, (215, 215))
		font = ImageFont.truetype("fonts/arial.ttf", 38)
		akafont = ImageFont.truetype("fonts/arial.ttf", 30)
		subfont = ImageFont.truetype("fonts/arial.ttf", 25)

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
			await interaction.response.send_message(file = discord.File(a, "profile.png"))

	@app_commands.command(name="actualgame", description="Affiche l'activité de quelqu'un ou de soi même")
	@app_commands.describe(user="Affiche l'activité de cet utilisateur.")
	@app_commands.checks.bot_has_permissions(embed_links=True)
	async def actualgame(self, interaction: discord.Interaction, user: discord.Member = None):
		"""Affiche l'activité de quelqu'un ou de soi même (**EN DEVELEPPEMENT)**"""
		if not user:
			user = interaction.user

		realuser = get(self.bot.get_all_members(), id=user.id)
		for activity in realuser.activities:
			try:
				game = activity.name
				details = activity.details
				state = activity.state
				s1 = time.strftime('%H:%M:%S')
				s2 = activity.start
				s3 = s2.astimezone(timezone('Europe/berlin')).strftime('%H:%M:%S')
				FMT = '%H:%M:%S'
				start = datetime.strptime(s1, FMT) - datetime.strptime(s3, FMT)
				url = activity.large_image_url
			
				embed = discord.Embed(title=f"Affiche l'activité de {user.name}#{user.discriminator}", description="", color=discord.Colour.yellow())

				embed.add_field(name='__Joue à__ : ', value=game, inline=False)
				
				embed.add_field(name='__Détails__ : ', value=details, inline=False)
				
				embed.add_field(name='__Sous détails__ : ', value=state, inline=False)
				
				embed.add_field(name='__Depuis__ : ', value=start, inline=False)

				embed.set_thumbnail(url=url)
				
				embed.set_footer(text=f"Demandé par : {str(interaction.user.name)} à {time.strftime('%H:%M:%S')}", icon_url=interaction.user.display_avatar.url)

				await interaction.response.send_message(embed=embed)

			except Exception:
				await interaction.response.send_message(f"{user.name} n'est pas en activité pour le moment, essaye en jouant à un jeu par exemple. (PS : Si vous avez Spotify d'actif, mettez votre musique en **pause**)")

	@app_commands.command(name="rickroll", description="Troll quelqu'un ou toi même avec un rickroll")
	@app_commands.checks.bot_has_permissions(embed_links=True)
	@app_commands.describe(user="Troll cet utilisateur avec un rickroll.")
	async def rickroll(self, interaction: discord.Interaction, user: discord.Member = None):
		"""Troll quelqu'un ou toi même avec un rickroll"""
		if not user:
			user = interaction.user
		lyrics = ["Never gonna give you up",
					"Never gonna let you down",
					"Never gonna run around and desert you",
					"Never gonna say goodbye"]
		embed = discord.Embed(title=f'{random.choice(lyrics)}', description=f"{interaction.user.name} rickrolled {user.name}#{user.discriminator}", color=0x00ff00)
		embed.set_image(url="https://c.tenor.com/Z6gmDPeM6dgAAAAC/dance-moves.gif")
		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="eval", description="Évalue la/les personnes(s) mentionnée(s).")
	@app_commands.describe(user="Évalue cet utilisateur.")
	async def eval(self, interaction: discord.Interaction, user: discord.Member = None):
		"""Évalue la/les personnes(s) mentionnée(s)."""
		if not user:
			user = interaction.user

		if user.id == 405414058775412746:
			rating = 11
		else:
			rating = user.id/100000000000000000
			rating = round(rating)

		waifu_text = "waifu"

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

		await interaction.response.send_message("Oh that's your {}? I rate {} a {}/10. {}".format(waifu_text, user.name, rating, emoji))

	@app_commands.command(name="anilist", description="Recherche un anime sur AniList.co")
	@app_commands.describe(anime="Recherche cet anime sur AniList.co")
	@app_commands.checks.bot_has_permissions(embed_links=True)
	async def anilist(self, interaction: discord.Interaction, anime: str):
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
			'name': anime
		}

		async with aiohttp.ClientSession() as session:
			async with session.post(api, json={'query': query, 'variables': variables}) as r:
				if r.status == 200:
					json = await r.json()
					data = json['data']['Media']

					embed = discord.Embed(color=interaction.user.top_role.colour)
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
					await interaction.response.send_message(embed=embed)

				else:
					await interaction.response.send_message(":x: Je n'ai pas trouvé d'anime correspondant !")
    
	@app_commands.command(name="neko", description="Renvoie une image de neko")
	async def neko(self, interaction: discord.Interaction):
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
		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="kitsune", description="Renvoie une image de kitsune")
	async def kitsune(self, interaction: discord.Interaction):
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
		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="waifu", description="Renvoie une image de waifu")
	async def waifu(self, interaction: discord.Interaction):
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
		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="searchanimecharacter", description="Recherche un personnage d'anime")
	@app_commands.describe(name="Recherche du personnage")
	async def searchanimecharacter(self, interaction: discord.Interaction, name:str):
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
			await interaction.response.send_message(embed=embed)

		except:
			await interaction.response.send_message("<a:no_animated:844992804480352257> Je n'ai pas trouvé de personnage correspondant !")

	@app_commands.command(name="searchongoogle", description="Recherche un personnage ou une personne")
	@app_commands.describe(name="Recherche du personnage")
	async def searchongoogle(self, interaction: discord.Interaction, name:str):
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
		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="hentai", description="Renvoie une image/gif de hentai")
	async def hentai(self, interaction: discord.Interaction):
		"""Renvoie une image/gif de hentai"""
		hentai_url = 'https://anime-api.hisoka17.repl.co/img/nsfw/hentai'
		r = requests.get(hentai_url)
		link = r.json()
		link = json.dumps(link)
		python_obj = json.loads(link)
		url = python_obj["url"]

		result = interaction.channel.is_nsfw()
		if result:
			embed = discord.Embed(title="Hentai", color=0xE01DE3)
			embed.set_image(url=url)
			embed.add_field(name="API fournie par", value="[anime-api.hisoka17](https://anime-api.hisoka17.repl.co/)")
			await interaction.response.send_message(embed=embed)
		else:
			await interaction.response.send_message("<a:no_animated:844992804480352257> Tu ne peux utiliser cette commande que dans un channel NSFW !")

	@app_commands.command(name="registerlol", description="Permet d'enregistrer ton profil League of Legends")
	@app_commands.describe(username="Mets ton profil League of Legends")
	async def registerlol(self, interaction: discord.Interaction, username:str):
		"""Permet d'enregistrer ton profil League of Legends"""
		my_region = 'euw1'
  
		if username:
			try:
				me = lol_watcher.summoner.by_name(my_region, username)
				name = me['name']
				# Insert
				await self.bot.database.insert(self.lol_profile["table"], {"pseudo": interaction.user.name, "discord_id": interaction.user.id, "lol_account": name})
				# Update
				await self.bot.database.update(self.lol_profile["table"], "lol_account", name, "discord_id = "+str(interaction.user.id))
				await interaction.response.send_message("<a:yes_animated:844992841938894849> Votre profil a bien été enregistré ! Votre nom de compte est maintenant : **"+name+"**")
			except:
				raise await interaction.response.send_message("<a:no_animated:844992804480352257> Je n'ai pas trouvé de profil League of Legends correspondant !")
		else:
			await interaction.response.send_message("<a:no_animated:844992804480352257> Vous devez préciser un nom de profil League of Legends !")

	@app_commands.command(name="lolprofil", description="Permet d'enregistrer ton profil League of Legends")
	@app_commands.describe(username="Mets ton profil League of Legends")
	async def lolprofil(self, interaction: discord.Interaction, username:str=None):
		"""Renvoie le profil de League of Legends"""
		response = await self.bot.database.lookup(self.lol_profile["table"], "lol_account", "discord_id", str(interaction.user.id))
		my_region = 'euw1'

		if not username:
			username = response[0][0]
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
				for i in range(len(my_ranked_stats)):
					# Solo/Duo
					if my_ranked_stats[i]['queueType'] == 'RANKED_SOLO_5x5':
						queueType0 = my_ranked_stats[i]['queueType']
						tier0 = my_ranked_stats[i]['tier']
						rank0 = my_ranked_stats[i]['rank']
						lp0 = my_ranked_stats[i]['leaguePoints']
						wins0 = my_ranked_stats[i]['wins']
						losses0 = my_ranked_stats[i]['losses']
					# Flex
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
				await interaction.response.send_message(embed=embed)

			except:
				await interaction.response.send_message("<a:no_animated:844992804480352257> Vous n'avez pas fait de parties en ranked.")
		except:
			await interaction.response.send_message("<a:no_animated:844992804480352257> Je n'ai pas trouvé de compte League of Legends correspondant. Essayez d'enregistrer votre compte League of Legends en utilisant `?registerlol` ou `?rlol` et réessayez.")
		
async def setup(bot):
	await bot.add_cog(Funcmd(bot))
