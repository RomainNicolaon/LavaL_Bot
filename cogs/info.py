from email import utils
import io
import time
import discord
import matplotlib.pyplot as plt
import requests

from io import BytesIO
from datetime import datetime
from discord.utils import get
from discord.ext import commands
from discord import Guild, Permissions, app_commands
from PIL import Image, ImageDraw, ImageFont
from views import link
from classes.discordbot import DiscordBot
from classes.ansi import Format as fmt, Foreground as fg, Background as bg

def statServer(guild) -> dict:
	status = {}
	must = ["members", "bot", "streaming", "idle", "dnd", "online", "offline", "mobile"]
	for a in must:
		status[a] = 0
	for member in guild:
		status["members"] += 1
		status[str(member.status)] += 1
		if member.is_on_mobile(): 
			status["mobile"] += 1
		if member.bot: 
			status["bot"] += 1
		if member.activity or member.activities: 
			for activity in member.activities:
				if activity.type == discord.ActivityType.streaming:
					status["streaming"] += 1

	return status

class Info(commands.Cog, name="info"):
	"""
		Informations et statistiques.
	
		Require intents: 
			- members
			- presences
		
		Require bot permission:
			- use_external_emojis
	"""
	def __init__(self, bot: DiscordBot) -> None:
		self.bot = bot

	def help_custom(self) -> tuple[str, str, str]:
		emoji = '📊'
		label = "Info"
		description = "Commandes concernant les informations complémentaires telles que les statistiques."
		return emoji, label, description

	@app_commands.command(name="statistics", description="Afficher les statistiques sur le serveur.")
	@app_commands.checks.cooldown(1, 15.0, key=lambda i: (i.guild_id, i.user.id))
	@app_commands.checks.bot_has_permissions(use_external_emojis=True)
	async def stat(self, interaction: discord.Interaction) -> None:
		"""Show a graphic pie about the server's members.""" 
		plt.clf()
		ax, data, colors = plt.subplot(), statServer(interaction.guild.members), ["#747f8d","#f04747","#faa81a","#43b582"]
		ax.pie([data["offline"], data["dnd"], data["idle"], data["online"]], colors=colors, startangle=-40, wedgeprops=dict(width=0.5))
		leg = ax.legend(["Offline","dnd","idle","Online"],frameon=False, loc="lower center", ncol=5)
		for color,text in zip(colors,leg.get_texts()):
			text.set_color(color)
		image_binary = io.BytesIO()
		plt.savefig(image_binary, transparent=True)
		image_binary.seek(0)
		
		embed = discord.Embed(title=f"Statistiques actuelles du serveur ({data['members']})",description=f"<:offline:974206581828898836> : **`{data['offline']}`** (Offline)\n<:afk:974206581845684254> : **`{data['idle']}`** (AFK)\n<:dnd:974206581883424778> : **`{data['dnd']}`** (dnd)\n<:online:974206581862453289> : **`{data['online']}`** (Online)\n<:streaming:974206582030217256> : **`{data['streaming']}`** (Streaming)\n<:mobile:974206581820506181> : **`{data['mobile']}`** (on mobile)\n<:robot:974206581849882644> : **`{data['bot']}`** (Robot)")
		embed.set_image(url="attachment://stat.png")
		embed.set_footer(text=f"Demandé par : {interaction.user} at {time.strftime('%H:%M:%S')}", icon_url=interaction.user.display_avatar.url)
		await interaction.response.send_message(file=discord.File(fp=image_binary, filename="stat.png"), embed=embed)

	@app_commands.command(name="avatar", description="Affichez l'avatar.")
	@app_commands.describe(user="Affiche l'image de profil de l'utilisateur.")
	@app_commands.checks.bot_has_permissions(embed_links=True)
	async def avatar(self, interaction: discord.Interaction, user: discord.Member = None):
		if not user:
			user = interaction.user
  
		pfp = user.display_avatar.url
		embed = discord.Embed(title=f"Affiche la photo de profile de {user.name}#{user.discriminator}", color=0x00000, description=f"[Avatar URL]({pfp})")

		embed.set_image(url=pfp)

		embed.set_footer(text=f"Demandé par : {str(interaction.user.name)} à {time.strftime('%H:%M:%S')}", icon_url=interaction.user.display_avatar.url)

		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="banner", description="Display the banner.")
	@app_commands.describe(user="Affiche la bannière de profil de l'utilisateur.")
	@app_commands.checks.bot_has_permissions(embed_links=True)
	async def banner(self, interaction: discord.Interaction, user: discord.Member = None):
		if not user: 
			user = interaction.user
		user = await self.bot.fetch_user(user.id)

		try:
			embed = discord.Embed(title=f"Affiche la bannière de profile de {user.name}#{user.discriminator}", color=0x00000, description=f"[Banner URL]({user.banner.url})")

			embed.set_image(url=user.banner.url)

			embed.set_footer(text=f"Demandé par : {str(interaction.user.name)} à {time.strftime('%H:%M:%S')}", icon_url=interaction.user.display_avatar.url)

			await interaction.response.send_message(embed=embed)
		except:
			await interaction.response.send_message("Hmm cet utilisateur n'a pas de bannière personalisée")

	@app_commands.command(name="lookup", description="Affiche des informations sur un utilisateur Discord")
	@app_commands.describe(user="L'utilisateur à afficher les informations.")
	@app_commands.checks.bot_has_permissions(use_external_emojis=True)
	async def lookup(self, interaction: discord.Interaction, user: discord.Member = None):
		"""Affiche plus d'informations sur un utilisateur Discord"""
		if not user: 
			user = interaction.user

		realuser: discord.Member = get(user.guild.members, id=user.id)
  
		pfp = user.display_avatar.url
		embed = discord.Embed(title=f"Affiche des information sur le compte de {user.name}#{user.discriminator}")
		embed.add_field(name="ID", value=user.id, inline=True)
		embed.add_field(name="Créé depuis le :", value=f"<t:{round(datetime.timestamp(realuser.created_at))}:F>", inline=True)
		embed.set_thumbnail(url=pfp)
		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="informations", description="Affiche les informations sur le Bot")
	async def infos(self, interaction: discord.Interaction):
		"""Affiche les informations sur le Bot"""
	 
		collabs = ['78691006', '71769515']

		url0 = 'https://avatars.githubusercontent.com/u/' + collabs[0] + '?v=4/img'
		url1 = 'https://avatars.githubusercontent.com/u/' + collabs[1] + '?v=4/img'

		card0 = Image.open(requests.get(url0, stream=True).raw)
		card1 = Image.open(requests.get(url1, stream=True).raw)
		
		card0 = card0.resize((280,280))
		card1 = card1.resize((280,280))
  
		card = Image.open('img/github.png')
  
		card.paste(card0, (80,165))
		card.paste(card1, (580,165))
  
  
		####################################################################
  
		text = "Collaborateurs"
  
		draw = ImageDraw.Draw(card)
		font = ImageFont.truetype("fonts/arial.ttf", 60)
  
		draw.text((280,60), text, font=font, fill=(255,255,255,128))
  
		with BytesIO() as img_bin:
			card.save(img_bin, format="PNG")
			img_bin.seek(0)
			file = discord.File(img_bin, "final_card.png")
  
		embed = discord.Embed(title="Donne des informations sur moi", color=0x4F2B10, description="Yo, je suis le bot de <@!405414058775412746>", colour=discord.Colour(0x4F2B10))
  
		embed.add_field(name="Ajoutes moi sur ton serveur en cliquant ici :", value="__[Invitation](https://discord.com/oauth2/authorize?client_id=808008104628322334&permissions=8&scope=bot%20applications.commands)__")

		embed.set_image(url="attachment://final_card.png")
  
		embed.set_footer(text=f"Demandé par : {str(interaction.user.name)} à {time.strftime('%H:%M:%S')}", icon_url=interaction.user.display_avatar.url)

		await interaction.response.send_message(file=file, embed=embed)
  
	@app_commands.command(name="numbersofservers", description="Affiche la liste serveurs où LavaL Bot est")
	async def nbservers(self, interaction: discord.Interaction):
		await interaction.response.defer()
		"""Affiche la liste ainsi que le nombre de serveurs où LavaL Bot est"""
		number_servers = str(len(self.bot.guilds))
		int_number_servers = int(len(self.bot.guilds))
		percent = int_number_servers*100/75
		percent = round(percent, 1)

		embed = discord.Embed(title=f"Objectif de serveurs de {self.bot.user.name}", description=f"Actuellement {self.bot.user.name} est sur **" + number_servers + "** serveurs", colour=discord.Colour(0xFA8072))

		embed.add_field(name="But à atteindre : 75 serveurs", value=number_servers + '/75 serveurs soit ≃ ' + str(percent) +'% atteint', inline=False)

		embed.add_field(name=f"Utilisateurs de {self.bot.user.name}", value=len(self.bot.users))

		embed.set_footer(text=f"Demandé par : {str(interaction.user.name)} à {time.strftime('%H:%M:%S')}", icon_url=interaction.user.display_avatar.url)

		await interaction.followup.send(embed=embed)
  
		paginator = commands.Paginator(prefix="```ansi", suffix="```")
		for guild in self.bot.guilds:
			paginator.add_line(f"{fg.RED + fmt.BOLD}Name{fmt.RESET}={fg.GREEN + fmt.BOLD}{guild.name}{fmt.RESET} |{fg.RED + fmt.BOLD} Total Of Users{fmt.RESET}={fg.GREEN + fmt.BOLD}{guild.member_count}{fmt.RESET} |{fg.RED + fmt.BOLD} ID{fmt.RESET}={fg.GREEN + fmt.BOLD}{guild.id}{fmt.RESET} |{fg.RED + fmt.BOLD} Owner{fmt.RESET}={fg.GREEN + fmt.BOLD}{guild.owner}{fmt.RESET} |{fg.RED + fmt.BOLD} Is Admin{fmt.RESET}={fg.GREEN + fmt.BOLD}{[channel.permissions_for(guild.me).administrator for channel in guild.channels][0]}{fmt.RESET}")

		if interaction.user.id == 405414058775412746:
			for page in paginator.pages:
				await interaction.followup.send(content=page)

	@app_commands.command(name="server", description="Donne des informations sur le serveur")
	@commands.guild_only()
	async def server(self, interaction: discord.Interaction):
		"""Donne des informations sur le serveur"""
		server_icon = interaction.guild.icon
		embed = discord.Embed(title="Donne des informations sur le serveur", color=0x12F932, description="Ce serveur s'appelle "+str(interaction.guild.name) + " et totalise "+str(interaction.guild.member_count)+" membres et son créateur est <@!" + str(interaction.guild.owner_id)+">.", colour=discord.Colour(0x12F932))

		embed.set_thumbnail(url=server_icon)

		embed.set_footer(text=f"Demandé par : {str(interaction.user.name)} à {time.strftime('%H:%M:%S')}", icon_url=interaction.user.display_avatar.url)

		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="invitation", description="Comment inviter LavaL Bot")
	async def invitation(self, interaction: discord.Interaction):
		"""Comment inviter LavaL Bot"""

		view = link.View(label=f"Cliquez ici pour ajouter {self.bot.user.name}", url="https://discord.com/api/oauth2/authorize?client_id=808008104628322334&permissions=8&scope=bot")

		embed = discord.Embed(title = "Invitation", color = 0x12F932, description=f"Comment inviter {self.bot.user.name}", colour=discord.Colour(0x12F932))

		embed.add_field(name="Ajoutes moi sur ton serveur en cliquant ici :", value="__[Invitation](https://discord.com/api/oauth2/authorize?client_id=808008104628322334&permissions=8&scope=bot)__")
  
		embed.set_thumbnail(
			url=self.bot.user.display_avatar.url)

		embed.set_footer(text=f"Demandé par : {str(interaction.user.name)} à {time.strftime('%H:%M:%S')}", icon_url=interaction.user.display_avatar.url)

		await interaction.response.send_message(embed=embed, view=view)
  
	@app_commands.command(name='create_invite', description="Créer un lien d'invitation")
	async def create_invite(self, interaction: discord.Interaction):
		"""Créer un lien d'invitation"""
		invite = await interaction.channel.create_invite(max_age=0, max_uses=1, unique=True)
		await interaction.response.send_message(f"Lien d'invitation : {invite}")

async def setup(bot: DiscordBot):
	await bot.add_cog(Info(bot))
