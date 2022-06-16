import discord
import io
import requests
import json
from classes.discordbot import DiscordBot
from views.modal import CustomModal
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont, ImageChops
from io import BytesIO

from riotwatcher import LolWatcher

class LeagueOfLegends(commands.GroupCog, name="leagueoflegends", group_name="leagueoflegends", group_description="Commands related to leagueoflegends."):
	"""Description des commandes pour LeagueOfLegends

		Require intents:
			- presences
		
		Require bot permission:
			- use_external_emojis
	"""

	def __init__(self, bot: DiscordBot) -> None:
		self.bot = bot

		self.subconfig_data: dict = self.bot.config["cogs"][self.__cog_name__.lower()]
		self.lol_profile = self.subconfig_data["lolprofile"]
		self.lol_watcher = self.subconfig_data["lol_watcher"]["api_key"]

	def help_custom(self) -> tuple[str, str, str]:
		emoji = '<:LoL:983661145980284989>'
		label = "LeagueOfLegends"
		description = "Retrouve toutes les commandes concernant League Of Legends !"
		return emoji, label, description
	
	@app_commands.command(name="register", description="Permet d'enregistrer ton profil League of Legends")
	async def registerlol(self, interaction: discord.Interaction):
		"""Permet d'enregistrer ton profil League of Legends"""
		lol_watcher = LolWatcher(self.lol_watcher)
		async def when_submit(_class: CustomModal, mod_interaction: discord.Interaction):
			username = _class.values['pseudo']
			my_region = 'euw1'
  
			try:
				me = lol_watcher.summoner.by_name(my_region, username)
				name = me['name']
			except:
				await mod_interaction.response.send_message("<a:no_animated:844992804480352257> Je n'ai pas trouvé de profil League of Legends correspondant !")
			try:
				await self.bot.database.insert_onduplicate(self.lol_profile["table"], {"pseudo": mod_interaction.user.name, "discord_id": mod_interaction.user.id, "lol_account": name})
				await mod_interaction.response.send_message("<a:yes_animated:844992841938894849> Votre profil a bien été enregistré ! Votre nom de compte est maintenant : **"+name+"**")
			except:
				await mod_interaction.response.send_message("<a:no_animated:844992804480352257> Une erreur est survenue lors de l'enregistrement de votre profil League of Legends !")

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

	@app_commands.command(name="profile", description="Permet d'enregistrer ton profil League of Legends")
	@app_commands.describe(username="Mets ton profil League of Legends")
	async def lolprofile(self, interaction: discord.Interaction, username:str=None):
		"""Renvoie le profil de League of Legends"""
		lol_watcher = LolWatcher(self.lol_watcher)
		response = await self.bot.database.lookup(self.lol_profile["table"], "lol_account", {"discord_id": str(interaction.user.id)})
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
			await interaction.response.send_message("<a:no_animated:844992804480352257> Je n'ai pas trouvé de compte League of Legends correspondant. Essayez d'enregistrer votre compte League of Legends en utilisant `/registerlol` ou `/rlol` et réessayez.")

	@app_commands.command(name="recentgames", description="Affichez les stats de votre dernière partie League of Legends")
	async def lolrecentgames(self, interaction: discord.Interaction, username:str=None):
		"""Affichez les stats de votre dernière partie League of Legends"""
		await interaction.response.defer()
		lol_watcher = LolWatcher(self.lol_watcher)
		response = await self.bot.database.lookup(self.lol_profile["table"], "lol_account", {"discord_id": str(interaction.user.id)})
		my_region = 'euw1'
		try:
			if not username:
				username = response[0][0]
		except:
			await interaction.followup.send("<a:no_animated:844992804480352257> Vous n'avez pas encore enregistré de compte League of Legends ou n'avez spécifier aucun pseudo dans votre recherche !")
			return

		try:
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
			results = []
			participants_items = []
			participants_golds = []

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
				kda = f"{participant['kills']}/{participant['deaths']}/{participant['assists']}"
				participants_kda.append(str(kda))
				participants_champion.append(participant['championName'])
				participants_items.append((participant['item0'], participant['item1'], participant['item2'], participant['item3'], participant['item4'], participant['item5'], participant['item6']))
				participants_cs.append(str(participant['totalMinionsKilled'] + participant['neutralMinionsKilled']))
				participants_golds.append(str(participant['goldEarned']))
			for team in teams:
				tower_destroyed.append(team['objectives']['tower']['kills'])
				inhibiteur_destroyed.append(team['objectives']['inhibitor']['kills'])
				dragon_killed.append(team['objectives']['dragon']['kills'])
				riftherald_killed.append(team['objectives']['riftHerald']['kills'])
				baron_killed.append(team['objectives']['baron']['kills'])
				champions_killed.append(team['objectives']['champion']['kills'])
				results.append(team['win'])

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
			if results[0] == True:
				draw.text((110, 10), "Victoire", (58, 103, 231, 110), font=title_font)
			else:
				draw.text((110, 10), "Défaite", (58, 103, 231, 110), font=title_font)
			if results[1] == True:
				draw.text((110, 980), "Victoire", (236, 16, 16, 110), font=title_font)
			else:
				draw.text((110, 980), "Défaite", (236, 16, 16, 110), font=title_font)

			draw.text((680, 10), "K/D/A", (255, 255, 255, 110), font=title_font)
			draw.text((955, 10), "CS", (255, 255, 255, 110), font=title_font)
			draw.text((1125, 10), "Items", (255, 255, 255, 110), font=title_font)
			draw.text((1600, 10), "Golds", (255, 255, 255, 110), font=title_font)

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
			for i in range(0, 5):
				draw.text((200, 125 + (i * 80)), participants_name[i], font=basic_font, fill=(255, 255, 255, 110))
			for i in range(5, 10):
				draw.text((200, 205 + (i * 80)), participants_name[i], font=basic_font, fill=(255, 255, 255, 110))

			# Players Icons
			icons = []
			for participant in participants_champion:
				response = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{latest_version}/img/champion/{participant}.png")
				player_icon_url = io.BytesIO(response.content)
				player_icon = (Image.open(player_icon_url).convert('RGBA').resize((60, 60)))
				icons.append(circle(player_icon))

			for i in range(0, 5):
				match_background_image.paste(icons[i], (120, 110 + (i * 80)), mask=icons[i])
			for i in range(5, 10):
				match_background_image.paste(icons[i], (120, 190 + (i * 80)), mask=icons[i])

			# Players KDA
			for i in range(0, 5):
				draw.text((770, 160 + (i * 80)), participants_kda[i], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')
			for i in range(5, 10):
				draw.text((770, 240 + (i * 80)), participants_kda[i], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')

			# Players CS
			for i in range(0, 5):
				draw.text((1000, 160 + (i * 80)), participants_cs[i], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')
			for i in range(5, 10):
				draw.text((1000, 240 + (i * 80)), participants_cs[i], font=basic_font, fill=(255, 255, 255, 110), anchor='ms')

			# Players Items
			items = []
			for i in range(0, 10):
				for participant in participants_items[i]:
					if participant != 0:
						response = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/img/item/{participant}.png")
						item_icon_url = io.BytesIO(response.content)
						item_icon = (Image.open(item_icon_url).convert('RGBA').resize((60, 60)))
						items.append(item_icon)
					if participant == 0:
						items.append(Image.new('RGBA', (60, 60), (0, 0, 0, 0)))

			for i in range(0, 7):
				match_background_image.paste(items[i], (1125 + (i * 70), 110), mask=items[i])
			for i in range(7, 14):
				match_background_image.paste(items[i], (1125 - (7*70) + (i * 70), 110 + 80), mask=items[i])
			for i in range(14, 21):
				match_background_image.paste(items[i], (1125 - (14*70) + (i * 70), 110 + 80*2), mask=items[i])
			for i in range(21, 28):
				match_background_image.paste(items[i], (1125 - (21*70) + (i * 70), 110 + 80*3), mask=items[i])
			for i in range(28, 35):
				match_background_image.paste(items[i], (1125 - (28*70) + (i * 70), 110 + 80*4), mask=items[i])
			for i in range(35, 42):
				match_background_image.paste(items[i], (1125 - (35*70) + (i * 70), 110 + 80*6), mask=items[i])
			for i in range(42, 49):
				match_background_image.paste(items[i], (1125 - (42*70) + (i * 70), 110 + 80*7), mask=items[i])
			for i in range(49, 56):
				match_background_image.paste(items[i], (1125 - (49*70) + (i * 70), 110 + 80*8), mask=items[i])
			for i in range(56, 63):
				match_background_image.paste(items[i], (1125 - (56*70) + (i * 70), 110 + 80*9), mask=items[i])
			for i in range(63, 70):
				match_background_image.paste(items[i], (1125 - (63*70) + (i * 70), 110 + 80*10), mask=items[i])


			# Team Kills
			team_kills = []
			blue_team_kill = []
			red_team_kill = []
			for participant in participants[0:5]:
				blue_team_kill.append(participant['kills'])
			blue_team_kill = sum(blue_team_kill)
			team_kills.append(blue_team_kill)

			for participant in participants[5:10]:
				red_team_kill.append(participant['kills'])
			red_team_kill = sum(red_team_kill)
			team_kills.append(red_team_kill)

			# Team Gold
			team_golds = []
			blue_team_gold = []
			red_team_gold = []
			for participant in participants[0:5]:
				blue_team_gold.append(participant['goldEarned'])
				total_blue_team_gold = sum(blue_team_gold)
				team_golds.append(total_blue_team_gold)

			for participant in participants[5:10]:
				red_team_gold.append(participant['goldEarned'])
				total_red_team_gold = sum(red_team_gold)
				team_golds.append(total_red_team_gold)

			total_kills = team_kills[0] + team_kills[1]
			space = 1350-510
			blue_team_kill_space = team_kills[0] * 100 / total_kills
			blue_team_kill_space = blue_team_kill_space * space / 100 + 510
			draw.rectangle((510, 510, 1350, 570), fill=(255, 255, 255, 110))
			draw.rectangle((510, 510, blue_team_kill_space, 570), fill=(0, 0, 255, 110)) # blue team
			draw.rectangle((blue_team_kill_space, 510, 1350, 570), fill=(255, 0, 0, 110)) # Red team
			draw.text((560, 555), str(team_kills[0]), font=basic_font, fill=(255, 255, 255, 255), anchor='ms')
			draw.text((1300, 555), str(team_kills[1]), font=basic_font, fill=(255, 255, 255, 255), anchor='ms')
			draw.text((920, 555), "Total Kill", font=basic_font, fill=(255, 255, 255, 255), anchor='ms')

			# Player Gold
			for i in range(0, 5):
				draw.text((1650, 125 + (i * 80)), participants_golds[i], font=basic_font, fill=(255, 255, 255, 110))
			for i in range(5, 10):
				draw.text((1650, 205 + (i * 80)), participants_golds[i], font=basic_font, fill=(255, 255, 255, 110))

			with BytesIO() as img_bin:
				match_background_image.convert('RGB').save(img_bin, format="PNG")
				img_bin.seek(0)
				file = discord.File(img_bin, "img/lol.png")

			await interaction.followup.send(file=file)
		except Exception as e:
			await interaction.followup.send("<a:no_animated:844992804480352257> Je n'ai pas trouvé de compte League of Legends correspondant. Essayez un autre pseudo ou enregistrer votre compte League of Legends en utilisant `/registerlol` ou `/rlol` et réessayez.")
			print(e)
   

async def setup(bot: DiscordBot):
	await bot.add_cog(LeagueOfLegends(bot))