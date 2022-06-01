from datetime import datetime
import time
from PIL import Image, ImageDraw, ImageFont, ImageChops
from io import BytesIO
from pytz import timezone
import discord
import random
from discord.ext import commands
from discord import app_commands
import aiohttp
import requests
from datetime import datetime
import json
from serpapi import GoogleSearch
from riotwatcher import LolWatcher
from discord.utils import get
from views.modal import CustomModal
from lyrics_extractor import SongLyrics
from pbwrap import Pastebin
import io

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
		self.song_lyrics_config = bot.config["bot"]["song_lyrics"]

		self.lol_watcher = bot.config["bot"]["lol_watcher"]["api_key"]
		self.lyrics_api_key = self.song_lyrics_config["extract_lyrics_api_key"]
		self.lyrics_api_key2 = self.song_lyrics_config["extract_lyrics_api_key2"]
		self.pastebin_api = self.song_lyrics_config["pastebin_api_key"]

	def help_custom(self) -> tuple[str, str, str]:
		emoji = '<a:CatGunner:876156284557221929>'
		label = "Fun"
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
		try:
			for activity in realuser.activities:
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
		except:
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

					try:
						embed = discord.Embed(color=interaction.user.top_role.colour)
						embed.set_footer(text='API fourni par AniList.co | ID: {}'.format(str(data['id'])))
						embed.set_thumbnail(url=data['coverImage']['large'])
						if data['title']['english'] == None or data['title']['english'] == data['title']['romaji']:
							embed.add_field(name='Titre', value=data['title']['romaji'], inline=False)
						else:
							embed.add_field(name='Titre', value='{} ({})'.format(data['title']['english'], data['title']['romaji']), inline=False)

						if data['description'] == '' or 'None':
							if len(data['description']) >= 1024:
								embed.add_field(name='Description', value='{}...'.format(data['description'][:1024-3]).replace("<br>", ''), inline=False)
							else:
								embed.add_field(name='Description', value=data['description'].replace("<br>", ''), inline=False)
						else:
							embed.add_field(name='Description', value='Aucune description disponible.', inline=False)

						embed.add_field(name='Type', value=data['format'].replace('_', ' ').title().replace('Tv', 'TV'), inline=True)

						try: 
							if data['episodes'] > 1:
								embed.add_field(name="Nombre d'épisodes", value='{} ep de {} min'.format(data['episodes'], data['duration']), inline=True)
						except:
							embed.add_field(name="Nombre d'épisodes", value="Nombre d'épisodes inconnus", inline=True)
							
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
					except:
						await interaction.response.send_message('Aucun résultat pour `{}`.'.format(anime))
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
	async def registerlol(self, interaction: discord.Interaction):
		"""Permet d'enregistrer ton profil League of Legends"""
		lol_watcher = LolWatcher(self.lol_watcher)
		async def when_submit(_class: CustomModal, mod_interaction: discord.Interaction):
			username = _class.values['pseudo']
			my_region = 'euw1'
  
			try:
				me = lol_watcher.summoner.by_name(my_region, username)
				name = me['name']
				exist = await self.bot.database.exist(self.lol_profile["table"], "*", f"discord_id={mod_interaction.user.id}")
				if exist:
					# Update
					await self.bot.database.update(self.lol_profile["table"], "lol_account", name, f"discord_id = {mod_interaction.user.id}")
				else:
					# Insert
					await self.bot.database.insert(self.lol_profile["table"], {"pseudo": mod_interaction.user.name, "discord_id": mod_interaction.user.id, "lol_account": name})
				await mod_interaction.response.send_message("<a:yes_animated:844992841938894849> Votre profil a bien été enregistré ! Votre nom de compte est maintenant : **"+name+"**")
			except:
				raise await mod_interaction.response.send_message("<a:no_animated:844992804480352257> Je n'ai pas trouvé de profil League of Legends correspondant !")

		modal = CustomModal(
			title="Enregistrement de compte League of Legends",
			fields={
				"pseudo": discord.ui.TextInput(
					label="Pseudo League of Legends",
					placeholder="Ton pseudo ici...",
					style=discord.TextStyle.short,
					required=True,
					min_length=3
				)
			},
			when_submit=when_submit
		)

		await interaction.response.send_modal(modal)

	@app_commands.command(name="lolprofile", description="Permet d'enregistrer ton profil League of Legends")
	@app_commands.describe(username="Mets ton profil League of Legends")
	async def lolprofil(self, interaction: discord.Interaction, username:str=None):
		"""Renvoie le profil de League of Legends"""
		lol_watcher = LolWatcher(self.lol_watcher)
		response = await self.bot.database.lookup(self.lol_profile["table"], "lol_account", "discord_id", str(interaction.user.id))
		my_region = 'euw1'
		try:
			if not username:
				username = response[0][0]
		except:
			await interaction.response.send_message("<a:no_animated:844992804480352257> Vous n'avez pas encore enregistré de compte League of Legends !")
			return

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

	@app_commands.command(name="lyrics", description="Affichez les lyrics de votre chanson")
	async def lyrics(self, interaction: discord.Interaction, song:str):
		"""Affichez les lyrics de votre chanson"""
		try:
			extract_lyrics = SongLyrics(self.lyrics_api_key, self.lyrics_api_key2)

			extract_song = extract_lyrics.get_lyrics(song)
			final_song = extract_song['lyrics']

			pb = Pastebin(self.pastebin_api)
			file = pb.create_paste(final_song, 0, f'Lyrics de {song}', None, None)
			embed = discord.Embed(title="Lyrics", color=0xE01DE3)
			embed.add_field(name=f"Lyrics de : {song}".upper(), value=f"<{file}>", inline=False)
			embed.set_thumbnail(url="https://media.istockphoto.com/vectors/music-note-icon-vector-illustration-vector-id1175435360?k=20&m=1175435360&s=612x612&w=0&h=1yoTgUwobvdFlNxUQtB7_NnWOUD83XOMZHvxUzkOJJs=")
			await interaction.response.send_message(embed=embed)
		except:
			await interaction.response.send_message("<a:no_animated:844992804480352257> Je n'ai pas trouvé de chanson correspondante.")

	@app_commands.command(name="lolrecentgames", description="Affichez les stats de votre dernière partie League of Legends")
	async def lolrecentgames(self, interaction: discord.Interaction, username:str=None):
		"""Affichez les stats de votre dernière partie League of Legends"""
		lol_watcher = LolWatcher(self.lol_watcher)
		response = await self.bot.database.lookup(self.lol_profile["table"], "lol_account", "discord_id", str(interaction.user.id))
		my_region = 'euw1'
		try:
			if not username:
				username = response[0][0]
		except:
			await interaction.response.send_message("<a:no_animated:844992804480352257> Vous n'avez pas encore enregistré de compte League of Legends !")
			return

		me = lol_watcher.summoner.by_name(my_region, username)
		user_puuid = me['puuid']
		matches = lol_watcher.match.matchlist_by_puuid(my_region, user_puuid)[0]
		match = lol_watcher.match.by_id(my_region, matches)
		infos = match['info']
		participants = match['info']['participants']
		teams = match['info']['teams']
		version = 'https://ddragon.leagueoflegends.com/api/versions.json'
		r = requests.get(version)
		link = r.json()
		link = json.dumps(link)
		python_obj = json.loads(link)
		latest_version = python_obj[0]

		participants_name = []
		participants_level = []
		participants_kda = []
		participants_champion = []
		tower_destroyed = []
		inhibiteur_destroyed = []
		dragon_killed = []
		riftherald_killed = []
		baron_killed = []
		champions_killed = []
		participants_cs = []
		# participants_items = []

		def circle(pfp,size = (60,60)):
			pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
			bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
			mask = Image.new('L', bigsize, 0)
			draw = ImageDraw.Draw(mask) 
			draw.ellipse((0, 0) + bigsize, fill=255)
			mask = mask.resize(pfp.size, Image.ANTIALIAS)
			mask = ImageChops.darker(mask, pfp.split()[-1])
			pfp.putalpha(mask)
			return pfp

		for participant in participants:
			participants_name.append(participant['summonerName'])
			participants_level.append(participant['champLevel'])
			if participant['deaths'] != 0:
				kda = (participant['kills'] + participant['assists']) / participant['deaths']
				kda = round(kda, 2)
			else:
				kda = "Perfect"
			participants_kda.append(str(kda))
			participants_champion.append(participant['championName'])
			# participants_items.append((participant['item0']))
			participants_cs.append(str(participant['totalMinionsKilled'] + participant['neutralMinionsKilled']))
		for team in teams:
			tower_destroyed.append(team['objectives']['tower']['kills'])
			inhibiteur_destroyed.append(team['objectives']['inhibitor']['kills'])
			dragon_killed.append(team['objectives']['dragon']['kills'])
			riftherald_killed.append(team['objectives']['riftHerald']['kills'])
			baron_killed.append(team['objectives']['baron']['kills'])
			champions_killed.append(team['objectives']['champion']['kills'])

		match_background_image = Image.open('img/lol_template.png')
		match_background_image = match_background_image.convert('RGB')
		title_font = ImageFont.truetype('fonts/Friz_Quadrata_Bold.otf', size=60)
		basic_font = ImageFont.truetype('fonts/Friz_Quadrata_Regular.ttf', size=50)
		draw = ImageDraw.Draw(match_background_image, 'RGBA')
		# global draw
		draw.rectangle(((0, 0), (match_background_image.size[0], match_background_image.size[1])), fill=(187, 187, 187, 80))
		draw.rectangle((100, 100, 1800, 980), fill = (129, 172, 255, 63), outline = (255, 255, 255), width = 5)
		# blue draw
		draw.rectangle((100, 100, 1800, 500), fill = (58, 103, 231, 110), outline = (255, 255, 255), width = 5)
		# middle draw
		draw.rectangle((100, 500, 1800, 580), fill = (187, 187, 187, 160), outline = (255, 255, 255), width = 5)
		# red draw
		draw.rectangle((100, 580, 1800, 980), fill = (214, 9, 9, 110), outline = (255, 255, 255), width = 5)
		# lines draw
		draw.line((100, 180, 1800, 180), fill = (255, 255, 255), width = 5)
		draw.line((100, 260, 1800, 260), fill = (255, 255, 255), width = 5)
		draw.line((100, 340, 1800, 340), fill = (255, 255, 255), width = 5)
		draw.line((100, 420, 1800, 420), fill = (255, 255, 255), width = 5)
		draw.line((100, 500, 1800, 500), fill = (255, 255, 255), width = 5)
		draw.line((100, 580, 1800, 580), fill = (255, 255, 255), width = 5)
		draw.line((100, 660, 1800, 660), fill = (255, 255, 255), width = 5)
		draw.line((100, 740, 1800, 740), fill = (255, 255, 255), width = 5)
		draw.line((100, 820, 1800, 820), fill = (255, 255, 255), width = 5)
		draw.line((100, 900, 1800, 900), fill = (255, 255, 255), width = 5)

		# Blue team
		baron_b = Image.open('img/icon-baron-b.png').convert('RGBA').resize((50, 50))
		match_background_image.paste(baron_b, (140, 515), mask=baron_b)
		draw.text((205, 520), str(baron_killed[0]), (255, 255, 255, 110), font=basic_font)

		dragon_b = Image.open('img/icon-dragon-b.png').convert('RGBA').resize((50, 50))
		match_background_image.paste(dragon_b, (260, 515), mask=dragon_b)
		draw.text((325, 520), str(dragon_killed[0]), (255, 255, 255, 110), font=basic_font)
		tower_b = Image.open('img/icon-tower-b.png').convert('RGBA').resize((50, 50))
		match_background_image.paste(tower_b, (380, 515), mask=tower_b)
		draw.text((455, 520), str(tower_destroyed[0]), (255, 255, 255, 110), font=basic_font)

		game_mode = infos['gameMode']
		draw.text((1300, 1005), "Mode de Jeu : " + str(game_mode), (255, 255, 255, 110), font=basic_font)
		draw.text((110, 10), "Victoire", (58, 103, 231, 110), font=title_font)
		draw.text((110, 980), "Défaite", (236, 16, 16, 110), font=title_font)
		draw.text((680, 10), "K/D/A", (255, 255, 255, 110), font=title_font)
		draw.text((980, 10), "CS", (255, 255, 255, 110), font=title_font)
		draw.text((1150, 10), "Items", (255, 255, 255, 110), font=title_font)

		# Red team
		baron_r = Image.open('img/icon-baron-r.png').convert('RGBA').resize((50, 50))
		match_background_image.paste(baron_r, (1400, 515), mask=baron_r)
		draw.text((1475, 520), str(baron_killed[1]), (255, 255, 255, 110), font=basic_font)

		dragon_r = Image.open('img/icon-dragon-r.png').convert('RGBA').resize((50, 50))
		match_background_image.paste(dragon_r, (1520, 515), mask=dragon_r)
		draw.text((1595, 520), str(dragon_killed[1]), (255, 255, 255, 110), font=basic_font)

		tower_r = Image.open('img/icon-tower-r.png').convert('RGBA').resize((50, 50))
		match_background_image.paste(tower_r, (1640, 515), mask=tower_r)
		draw.text((1715, 520), str(tower_destroyed[1]), (255, 255, 255, 110), font=basic_font)

		# Players Names
		draw.text((200, 120), participants_name[0], font=basic_font, fill=(255, 255, 255))
		draw.text((200, 200), participants_name[1], font=basic_font, fill=(255, 255, 255))
		draw.text((200, 280), participants_name[2], font=basic_font, fill=(255, 255, 255))
		draw.text((200, 360), participants_name[3], font=basic_font, fill=(255, 255, 255))
		draw.text((200, 440), participants_name[4], font=basic_font, fill=(255, 255, 255))
		draw.text((200, 600), participants_name[5], font=basic_font, fill=(255, 255, 255))
		draw.text((200, 680), participants_name[6], font=basic_font, fill=(255, 255, 255))
		draw.text((200, 760), participants_name[7], font=basic_font, fill=(255, 255, 255))
		draw.text((200, 840), participants_name[8], font=basic_font, fill=(255, 255, 255))
		draw.text((200, 920), participants_name[9], font=basic_font, fill=(255, 255, 255))

		# Players Icons
		icons = []
		for participant in participants_champion:
			response = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{latest_version}/img/champion/{participant}.png")
			player_icon_url = io.BytesIO(response.content)
			player_icon = (Image.open(player_icon_url).convert('RGBA').resize((60, 60)))
			icons.append(circle(player_icon))

		match_background_image.paste(icons[0], (120, 115), mask=icons[0])
		match_background_image.paste(icons[1], (120, 190), mask=icons[1])
		match_background_image.paste(icons[2], (120, 270), mask=icons[2])
		match_background_image.paste(icons[3], (120, 350), mask=icons[3])
		match_background_image.paste(icons[4], (120, 430), mask=icons[4])
		match_background_image.paste(icons[5], (120, 590), mask=icons[5])
		match_background_image.paste(icons[6], (120, 670), mask=icons[6])
		match_background_image.paste(icons[7], (120, 750), mask=icons[7])
		match_background_image.paste(icons[8], (120, 830), mask=icons[8])
		match_background_image.paste(icons[9], (120, 910), mask=icons[9])

		# Players KDA
		draw.text((770, 160), participants_kda[0], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')
		draw.text((770, 240), participants_kda[1], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')
		draw.text((770, 320), participants_kda[2], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')
		draw.text((770, 400), participants_kda[3], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')
		draw.text((770, 480), participants_kda[4], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')
		draw.text((770, 640), participants_kda[5], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')
		draw.text((770, 720), participants_kda[6], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')
		draw.text((770, 800), participants_kda[7], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')
		draw.text((770, 880), participants_kda[8], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')
		draw.text((770, 960), participants_kda[0], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')

		# Players CS
		draw.text((1025, 160), participants_cs[0], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')
		draw.text((1025, 240), participants_cs[1], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')
		draw.text((1025, 320), participants_cs[2], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')
		draw.text((1025, 400), participants_cs[3], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')
		draw.text((1025, 480), participants_cs[4], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')
		draw.text((1025, 640), participants_cs[5], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')
		draw.text((1025, 720), participants_cs[6], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')
		draw.text((1025, 800), participants_cs[7], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')
		draw.text((1025, 880), participants_cs[8], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')
		draw.text((1025, 960), participants_cs[0], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')

		# Players Items
		# for i in range(0, 9):
		# 	if participants_items[i][0] != 0:
		# 		response = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{latest_version}/img/item/{participants_items[i][0]}.png")
		# 		item_icon_url = io.BytesIO(response.content)
		# 		item_icon = (Image.open(item_icon_url).convert('RGBA').resize((30, 30)))
		# 		match_background_image.paste(item_icon, (1300, (i * 40) + 115), mask=item_icon)
		# 	if participants_items[i][1] != 0:
		# 		response = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{latest_version}/img/item/{participants_items[i][1]}.png")
		# 		item_icon_url = io.BytesIO(response.content)
		# 		item_icon = (Image.open(item_icon_url).convert('RGBA').resize((30, 30)))
		# 		match_background_image.paste(item_icon, (1350, (i * 40) + 115), mask=item_icon)
		# 	if participants_items[i][2] != 0:
		# 		response = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{latest_version}/img/item/{participants_items[i][2]}.png")
		# 		item_icon_url = io.BytesIO(response.content)
		# 		item_icon = (Image.open(item_icon_url).convert('RGBA').resize((30, 30)))
		# 		match_background_image.paste(item_icon, (1390, (i * 40) + 115), mask=item_icon)
		# 	if participants_items[i][3] != 0:
		# 		response = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{latest_version}/img/item/{participants_items[i][3]}.png")
		# 		item_icon_url = io.BytesIO(response.content)
		# 		item_icon = (Image.open(item_icon_url).convert('RGBA').resize((30, 30)))
		# 		match_background_image.paste(item_icon, (1440, (i * 40) + 115), mask=item_icon)
		# 	if participants_items[i][4] != 0:
		# 		response = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{latest_version}/img/item/{participants_items[i][4]}.png")
		# 		item_icon_url = io.BytesIO(response.content)
		# 		item_icon = (Image.open(item_icon_url).convert('RGBA').resize((30, 30)))
		# 		match_background_image.paste(item_icon, (1490, (i * 40) + 115), mask=item_icon)
		# 	if participants_items[i][5] != 0:
		# 		response = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{latest_version}/img/item/{participants_items[i][5]}.png")
		# 		item_icon_url = io.BytesIO(response.content)
		# 		item_icon = (Image.open(item_icon_url).convert('RGBA').resize((30, 30)))
		# 		match_background_image.paste(item_icon, (1500, (i * 40) + 115), mask=item_icon)

		# items_icons0 = []
		# for item in participants_items0:
		# 	if item != 0:
		# 		response = requests.get(f"http://ddragon.leagueoflegends.com/cdn/12.9.1/img/item/{item}.png")
		# 		item_icon_url = io.BytesIO(response.content)
		# 		item_icon = (Image.open(item_icon_url).convert('RGBA').resize((60, 60)))
		# 		items_icons0.append(item_icon)
		# 	else:
		# 		item_icon = (Image.new(size=(60, 60), mode="RGBA"))
		# 		items_icons0.append(item_icon)

		# match_background_image.paste(items_icons0[0], (1150, 110), mask=items_icons0[0])
		# match_background_image.paste(items_icons0[1], (1150, 190), mask=items_icons0[1])
		# match_background_image.paste(items_icons0[2], (1150, 270), mask=items_icons0[2])
		# match_background_image.paste(items_icons0[3], (1150, 350), mask=items_icons0[3])
		# match_background_image.paste(items_icons0[4], (1150, 430), mask=items_icons0[4])
		# match_background_image.paste(items_icons0[5], (1150, 590), mask=items_icons0[5])
		# match_background_image.paste(items_icons0[6], (1150, 670), mask=items_icons0[6])
		# match_background_image.paste(items_icons0[7], (1150, 750), mask=items_icons0[7])
		# match_background_image.paste(items_icons0[8], (1150, 830), mask=items_icons0[8])
		# match_background_image.paste(items_icons0[9], (1150, 910), mask=items_icons0[9])

		# items_icons1 = []
		# for item in participants_items1:
		# 	if item != 0:
		# 		response = requests.get(f"http://ddragon.leagueoflegends.com/cdn/12.9.1/img/item/{item}.png")
		# 		item_icon_url = io.BytesIO(response.content)
		# 		item_icon = (Image.open(item_icon_url).convert('RGBA').resize((60, 60)))
		# 		items_icons1.append(item_icon)
		# 	else:
		# 		item_icon = (Image.new(size=(60, 60), mode="RGBA"))
		# 		items_icons1.append(item_icon)

		# match_background_image.paste(items_icons1[0], (1220, 110), mask=items_icons1[0])
		# match_background_image.paste(items_icons1[1], (1220, 190), mask=items_icons1[1])
		# match_background_image.paste(items_icons1[2], (1220, 270), mask=items_icons1[2])
		# match_background_image.paste(items_icons1[3], (1220, 350), mask=items_icons1[3])
		# match_background_image.paste(items_icons1[4], (1220, 430), mask=items_icons1[4])
		# match_background_image.paste(items_icons1[5], (1220, 590), mask=items_icons1[5])
		# match_background_image.paste(items_icons1[6], (1220, 670), mask=items_icons1[6])
		# match_background_image.paste(items_icons1[7], (1220, 750), mask=items_icons1[7])
		# match_background_image.paste(items_icons1[8], (1220, 830), mask=items_icons1[8])
		# match_background_image.paste(items_icons1[9], (1220, 910), mask=items_icons1[9])

		# items_icons2 = []
		# for item in participants_items2:
		# 	if item != 0:
		# 		response = requests.get(f"http://ddragon.leagueoflegends.com/cdn/12.9.1/img/item/{item}.png")
		# 		item_icon_url = io.BytesIO(response.content)
		# 		item_icon = (Image.open(item_icon_url).convert('RGBA').resize((60, 60)))
		# 		items_icons2.append(item_icon)
		# 	else:
		# 		item_icon = (Image.new(size=(60, 60), mode="RGBA"))
		# 		items_icons2.append(item_icon)

		# match_background_image.paste(items_icons2[0], (1290, 110), mask=items_icons2[0])
		# match_background_image.paste(items_icons2[1], (1290, 190), mask=items_icons2[1])
		# match_background_image.paste(items_icons2[2], (1290, 270), mask=items_icons2[2])
		# match_background_image.paste(items_icons2[3], (1290, 350), mask=items_icons2[3])
		# match_background_image.paste(items_icons2[4], (1290, 430), mask=items_icons2[4])
		# match_background_image.paste(items_icons2[5], (1290, 590), mask=items_icons2[5])
		# match_background_image.paste(items_icons2[6], (1290, 670), mask=items_icons2[6])
		# match_background_image.paste(items_icons2[7], (1290, 750), mask=items_icons2[7])
		# match_background_image.paste(items_icons2[8], (1290, 830), mask=items_icons2[8])
		# match_background_image.paste(items_icons2[9], (1290, 910), mask=items_icons2[9])

		# items_icons3 = []
		# for item in participants_items3:
		# 	if item != 0:
		# 		response = requests.get(f"http://ddragon.leagueoflegends.com/cdn/12.9.1/img/item/{item}.png")
		# 		item_icon_url = io.BytesIO(response.content)
		# 		item_icon = (Image.open(item_icon_url).convert('RGBA').resize((60, 60)))
		# 		items_icons3.append(item_icon)
		# 	else:
		# 		item_icon = (Image.new(size=(60, 60), mode="RGBA"))
		# 		items_icons3.append(item_icon)

		# match_background_image.paste(items_icons3[0], (1360, 110), mask=items_icons3[0])
		# match_background_image.paste(items_icons3[1], (1360, 190), mask=items_icons3[1])
		# match_background_image.paste(items_icons3[2], (1360, 270), mask=items_icons3[2])
		# match_background_image.paste(items_icons3[3], (1360, 350), mask=items_icons3[3])
		# match_background_image.paste(items_icons3[4], (1360, 430), mask=items_icons3[4])
		# match_background_image.paste(items_icons3[5], (1360, 590), mask=items_icons3[5])
		# match_background_image.paste(items_icons3[6], (1360, 670), mask=items_icons3[6])
		# match_background_image.paste(items_icons3[7], (1360, 750), mask=items_icons3[7])
		# match_background_image.paste(items_icons3[8], (1360, 830), mask=items_icons3[8])
		# match_background_image.paste(items_icons3[9], (1360, 910), mask=items_icons3[9])

		# items_icons4 = []
		# for item in participants_items4:
		# 	if item != 0:
		# 		response = requests.get(f"http://ddragon.leagueoflegends.com/cdn/12.9.1/img/item/{item}.png")
		# 		item_icon_url = io.BytesIO(response.content)
		# 		item_icon = (Image.open(item_icon_url).convert('RGBA').resize((60, 60)))
		# 		items_icons4.append(item_icon)
		# 	else:
		# 		item_icon = (Image.new(size=(60, 60), mode="RGBA"))
		# 		items_icons4.append(item_icon)

		# match_background_image.paste(items_icons4[0], (1430, 115), mask=items_icons4[0])
		# match_background_image.paste(items_icons4[1], (1430, 190), mask=items_icons4[1])
		# match_background_image.paste(items_icons4[2], (1430, 270), mask=items_icons4[2])
		# match_background_image.paste(items_icons4[3], (1430, 350), mask=items_icons4[3])
		# match_background_image.paste(items_icons4[4], (1430, 430), mask=items_icons4[4])
		# match_background_image.paste(items_icons4[5], (1430, 590), mask=items_icons4[5])
		# match_background_image.paste(items_icons4[6], (1430, 670), mask=items_icons4[6])
		# match_background_image.paste(items_icons4[7], (1430, 750), mask=items_icons4[7])
		# match_background_image.paste(items_icons4[8], (1430, 830), mask=items_icons4[8])
		# match_background_image.paste(items_icons4[9], (1430, 910), mask=items_icons4[9])

		# items_icons5 = []
		# for item in participants_items5:
		# 	if item != 0:
		# 		response = requests.get(f"http://ddragon.leagueoflegends.com/cdn/12.9.1/img/item/{item}.png")
		# 		item_icon_url = io.BytesIO(response.content)
		# 		item_icon = (Image.open(item_icon_url).convert('RGBA').resize((60, 60)))
		# 		items_icons5.append(item_icon)
		# 	else:
		# 		item_icon = (Image.new(size=(60, 60), mode="RGBA"))
		# 		items_icons5.append(item_icon)

		# match_background_image.paste(items_icons5[0], (1500, 115), mask=items_icons5[0])
		# match_background_image.paste(items_icons5[1], (1500, 190), mask=items_icons5[1])
		# match_background_image.paste(items_icons5[2], (1500, 270), mask=items_icons5[2])
		# match_background_image.paste(items_icons5[3], (1500, 350), mask=items_icons5[3])
		# match_background_image.paste(items_icons5[4], (1500, 430), mask=items_icons5[4])
		# match_background_image.paste(items_icons5[5], (1500, 590), mask=items_icons5[5])
		# match_background_image.paste(items_icons5[6], (1500, 670), mask=items_icons5[6])
		# match_background_image.paste(items_icons5[7], (1500, 750), mask=items_icons5[7])
		# match_background_image.paste(items_icons5[8], (1500, 830), mask=items_icons5[8])
		# match_background_image.paste(items_icons5[9], (1500, 910), mask=items_icons5[9])

		# items_icons6 = []
		# for item in participants_items6:
		# 	if item != 0:
		# 		response = requests.get(f"http://ddragon.leagueoflegends.com/cdn/12.9.1/img/item/{item}.png")
		# 		item_icon_url = io.BytesIO(response.content)
		# 		item_icon = (Image.open(item_icon_url).convert('RGBA').resize((60, 60)))
		# 		items_icons6.append(item_icon)
		# 	else:
		# 		item_icon = (Image.new(size=(60, 60), mode="RGBA"))
		# 		items_icons6.append(item_icon)

		# match_background_image.paste(items_icons6[0], (1570, 115), mask=items_icons6[0])
		# match_background_image.paste(items_icons6[1], (1570, 190), mask=items_icons6[1])
		# match_background_image.paste(items_icons6[2], (1570, 270), mask=items_icons6[2])
		# match_background_image.paste(items_icons6[3], (1570, 350), mask=items_icons6[3])
		# match_background_image.paste(items_icons6[4], (1570, 430), mask=items_icons6[4])
		# match_background_image.paste(items_icons6[5], (1570, 590), mask=items_icons6[5])
		# match_background_image.paste(items_icons6[6], (1570, 670), mask=items_icons6[6])
		# match_background_image.paste(items_icons6[7], (1570, 750), mask=items_icons6[7])
		# match_background_image.paste(items_icons6[8], (1570, 830), mask=items_icons6[8])
		# match_background_image.paste(items_icons6[9], (1570, 910), mask=items_icons6[9])

		# print(f"{participants_items0}")
		
		# match_background_image.show()
		with BytesIO() as img_bin:
			match_background_image.save(img_bin, format="PNG")
			img_bin.seek(0)
			file = discord.File(img_bin, "img/lol.png")
		await interaction.response.defer()
		await interaction.edit_original_message(attachments=[file])
 
async def setup(bot):
	await bot.add_cog(Funcmd(bot))
