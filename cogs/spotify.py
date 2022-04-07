import discord
import requests
import dateutil.parser
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO


class Spotify(commands.Cog, name="spotify", command_attrs=dict(hidden=False)):
	"""Informations de l'activité d'un membre sur Spotify"""
	def __init__(self, bot):
		self.bot = bot
		
	def help_custom(self):
		emoji = '🎵'
		label = "Spotify"
		description = "Informations de l'activité d'un membre sur Spotify"
		return emoji, label, description

	@commands.command(name='track', aliases=['spotify', 'sp'])
	async def track(self, ctx, user: discord.Member = None):
		"""Activité d'un membre sur Spotify"""

		user = user or ctx.author

		try :
			spotify_result = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)

			# if spotify_result is None:
			# 	await ctx.send(f'{user.name} n\'écoute pas Spotify.')

			# Images
			track_background_image = Image.open('img/spotify_template.png')
			album_image = Image.open(requests.get(spotify_result.album_cover_url, stream=True).raw).convert('RGBA')

			# Fonts
			title_font = ImageFont.truetype('theboldfont.ttf', 16)
			artist_font = ImageFont.truetype('theboldfont.ttf', 14)
			album_font = ImageFont.truetype('theboldfont.ttf', 14)
			start_duration_font = ImageFont.truetype('theboldfont.ttf', 12)
			end_duration_font = ImageFont.truetype('theboldfont.ttf', 12)

			# Positions
			title_text_position = 150, 30
			artist_text_position = 150, 60
			album_text_position = 150, 80
			start_duration_text_position = 150, 122
			end_duration_text_position = 515, 122

			# Draws
			draw_on_image = ImageDraw.Draw(track_background_image)
			draw_on_image.text(title_text_position, spotify_result.title, 'white', font=title_font)
			draw_on_image.text(artist_text_position, f'by {spotify_result.artist}', 'white', font=artist_font)
			draw_on_image.text(album_text_position, spotify_result.album, 'white', font=album_font)
			draw_on_image.text(start_duration_text_position, '0:00', 'white', font=start_duration_font)
			draw_on_image.text(end_duration_text_position,
							f"{dateutil.parser.parse(str(spotify_result.duration)).strftime('%M:%S')}",
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

			await ctx.send(file=file)

		except Exception:
			await ctx.send(f'{user.name} n\'écoute pas Spotify.')


def setup(bot):
	bot.add_cog(Spotify(bot))