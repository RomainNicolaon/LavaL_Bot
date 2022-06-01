import discord
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import requests
import dateutil.parser
from discord.utils import get
from discord.ext import commands
from discord import app_commands

class Spotify(commands.Cog, name="spotify"):
	"""
		Montrer la présence de Spotify sur le discord.
	
		Require intents:
			- presences
		
		Require bot permission:
			- use_external_emojis
	"""
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

	def help_custom(self) -> tuple[str, str, str]:
		emoji = '<:spotify:895219605105172502>'
		label = "Spotify"
		description = "Commandes de statut Spotify."
		return emoji, label, description

	@app_commands.command(name="spotify")
	@app_commands.describe(user="Informations de l'activité Spotify de ce membre")
	async def spotify_activity(self, interaction: discord.Interaction, user: discord.Member = None):
		"""Activité d'un membre sur Spotify"""
		if not user: 
			user = interaction.user
		realuser = get(self.bot.get_all_members(), id=user.id)

		for activity in realuser.activities:
			if isinstance(activity, discord.activity.Spotify):
				# Images
				track_background_image = Image.open('img/spotify_template.png')
				album_image = Image.open(requests.get(activity.album_cover_url, stream=True).raw).convert('RGBA')

				# Fonts
				title_font = ImageFont.truetype('fonts/theboldfont.ttf', 16)
				artist_font = ImageFont.truetype('fonts/theboldfont.ttf', 14)
				album_font = ImageFont.truetype('fonts/theboldfont.ttf', 14)
				start_duration_font = ImageFont.truetype('fonts/theboldfont.ttf', 12)
				end_duration_font = ImageFont.truetype('fonts/theboldfont.ttf', 12)

				# Positions
				title_text_position = 150, 30
				artist_text_position = 150, 60
				album_text_position = 150, 80
				start_duration_text_position = 150, 122
				end_duration_text_position = 515, 122

				# Draws
				draw_on_image = ImageDraw.Draw(track_background_image)
				draw_on_image.text(title_text_position, activity.title, 'white', font=title_font)
				draw_on_image.text(artist_text_position, f'by {activity.artist}', 'white', font=artist_font)
				draw_on_image.text(album_text_position, activity.album, 'white', font=album_font)
				draw_on_image.text(start_duration_text_position, '0:00', 'white', font=start_duration_font)
				draw_on_image.text(end_duration_text_position,
								f"{dateutil.parser.parse(str(activity.duration)).strftime('%M:%S')}",
								'white', font=end_duration_font)

				# Background colour
				album_color = album_image.getpixel((250, 100))
				background_image_color = Image.new('RGBA', track_background_image.size, album_color)
				background_image_color.paste(track_background_image, (0, 0), track_background_image)

				# Resize
				album_image_resize = album_image.resize((140, 160))
				background_image_color.paste(album_image_resize, (0, 0), album_image_resize)

				# Save image

				with BytesIO() as img_bin:
					background_image_color.convert('RGB').save(img_bin, format="PNG")
					img_bin.seek(0)
					file = discord.File(img_bin, "img/spotify.png")

				await interaction.response.send_message(file=file)
				return
    
		await interaction.response.send_message(f"{user.name} n'écoute pas Spotify.")


async def setup(bot):
	await bot.add_cog(Spotify(bot))