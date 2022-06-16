import asyncio
import functools
import itertools
import math
import random
import discord
import youtube_dl
from async_timeout import timeout
from discord.ext import commands
from classes.discordbot import DiscordBot

# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ''

class VoiceError(Exception):
	pass


class YTDLError(Exception):
	pass


class YTDLSource(discord.PCMVolumeTransformer):
	YTDL_OPTIONS = {
		'format': 'bestaudio/best',
		'extractaudio': True,
		'audioformat': 'mp3',
		'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
		'restrictfilenames': False,
		'noplaylist': False,
		'nocheckcertificate': True,
		'ignoreerrors': False,
		'logtostderr': False,
		'quiet': True,
		'no_warnings': False,
		'default_search': 'auto',
		'source_address': '0.0.0.0',
	}

	FFMPEG_OPTIONS = {
		'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
		'options': '-vn',
	}

	ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

	def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
		super().__init__(source, volume)

		self.requester = ctx.author
		self.channel = ctx.channel
		self.data = data

		self.uploader = data.get('uploader')
		self.uploader_url = data.get('uploader_url')
		date = data.get('upload_date')
		self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
		self.title = data.get('title')
		self.thumbnail = data.get('thumbnail')
		self.description = data.get('description')
		self.duration = self.parse_duration(int(data.get('duration')))
		self.tags = data.get('tags')
		self.url = data.get('webpage_url')
		self.views = data.get('view_count')
		self.likes = data.get('like_count')
		self.dislikes = data.get('dislike_count')
		self.stream_url = data.get('url')

	def __str__(self):
		return '**{0.title}** de **{0.uploader}**'.format(self)

	@classmethod
	async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
		loop = loop or asyncio.get_event_loop()

		partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
		data = await loop.run_in_executor(None, partial)

		if data is None:
			raise YTDLError('Je n\'ai rien trouvé qui corresponde `{}`'.format(search))

		if 'entries' not in data:
			process_info = data
		else:
			process_info = None
			for entry in data['entries']:
				if entry:
					process_info = entry
					break

			if process_info is None:
				raise YTDLError('Je n\'ai rien trouvé qui corresponde `{}`'.format(search))

		webpage_url = process_info['webpage_url']
		partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
		processed_info = await loop.run_in_executor(None, partial)

		if processed_info is None:
			raise YTDLError('Impossible d\'aller chercher `{}`'.format(webpage_url))

		if 'entries' not in processed_info:
			info = processed_info
		else:
			info = None
			while info is None:
				try:
					info = processed_info['entries'].pop(0)
				except IndexError:
					raise YTDLError('Impossible de trouver une correspondance pour `{}`'.format(webpage_url))

		return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

	@staticmethod
	def parse_duration(duration: int):
		minutes, seconds = divmod(duration, 60)
		hours, minutes = divmod(minutes, 60)
		days, hours = divmod(hours, 24)

		duration = []
		if days > 0:
			duration.append('{} days'.format(days))
		if hours > 0:
			duration.append('{} hours'.format(hours))
		if minutes > 0:
			duration.append('{} minutes'.format(minutes))
		if seconds > 0:
			duration.append('{} seconds'.format(seconds))

		return ', '.join(duration)


class Song:
	__slots__ = ('source', 'requester')

	def __init__(self, source: YTDLSource):
		self.source = source
		self.requester = source.requester

	def create_embed(self):
		embed = (discord.Embed(title='Lecture en cours',
							   description='```css\n{0.source.title}\n```'.format(self),
							   color=discord.Color.blurple())
				 .add_field(name='Durée', value=self.source.duration)
				 .add_field(name='Demandé par', value=self.requester.mention)
				 .add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
				 .add_field(name='URL', value='[Click]({0.source.url})'.format(self))
				 .set_thumbnail(url=self.source.thumbnail))

		return embed


class SongQueue(asyncio.Queue):
	def __getitem__(self, item):
		if isinstance(item, slice):
			return list(itertools.islice(self._queue, item.start, item.stop, item.step))
		else:
			return self._queue[item]

	def __iter__(self):
		return self._queue.__iter__()

	def __len__(self):
		return self.qsize()

	def clear(self):
		self._queue.clear()

	def shuffle(self):
		random.shuffle(self._queue)

	def remove(self, index: int):
		del self._queue[index]


class VoiceState:
	def __init__(self, bot: DiscordBot, ctx: commands.Context):
		self.bot = bot
		self._ctx = ctx

		self.current = None
		self.voice = None
		self.next = asyncio.Event()
		self.songs = SongQueue()

		self._loop = False
		self._volume = 0.5
		self.skip_votes = set()

		self.audio_player = bot.loop.create_task(self.audio_player_task())

	def __del__(self):
		self.audio_player.cancel()

	@property
	def loop(self):
		return self._loop

	@loop.setter
	def loop(self, value: bool):
		self._loop = value

	@property
	def volume(self):
		return self._volume

	@volume.setter
	def volume(self, value: float):
		self._volume = value

	@property
	def is_playing(self):
		return self.voice and self.current

	async def audio_player_task(self):
		while True:
			self.next.clear()

			if not self.loop:
				# Try to get the next song within 3 minutes.
				# If no song will be added to the queue in time,
				# the player will disconnect
				try:
					async with timeout(180):  # 3 minutes
						self.current = await self.songs.get()
				except asyncio.TimeoutError:
					self.bot.loop.create_task(self.stop())
					return

			self.current.source.volume = self._volume
			self.voice.play(self.current.source, after=self.play_next_song)
			await self.current.source.channel.send(embed=self.current.create_embed())

			await self.next.wait()

	def play_next_song(self, error=None):
		if error:
			raise VoiceError(str(error))

		self.next.set()

	def skip(self):
		self.skip_votes.clear()

		if self.is_playing:
			self.voice.stop()

	async def stop(self):
		self.songs.clear()

		if self.voice:
			await self.voice.disconnect()
			self.voice = None


class Musicplayer(commands.Cog, name="musicplayer", command_attrs=dict(hidden=False)):
	"""Description des commandes du Lecteur de musiques"""
	def __init__(self, bot: DiscordBot):
		self.bot = bot
		self.voice_states = {}
		
	def help_custom(self) -> tuple[str, str, str]:
		emoji = '🎵'
		label = "Lecteur de musiques"
		description = "Description des commandes du Lecteur de musiques, comme play, pause, stop, etc"
		return emoji, label, description

	def get_voice_state(self, ctx: commands.Context):
		state = self.voice_states.get(ctx.guild.id)
		if not state:
			state = VoiceState(self.bot, ctx)
			self.voice_states[ctx.guild.id] = state

		return state

	def cog_unload(self):
		for state in self.voice_states.values():
			self.bot.loop.create_task(state.stop())

	def cog_check(self, ctx: commands.Context):
		if not ctx.guild:
			raise commands.NoPrivateMessage('Cette commande ne peut pas être utilisée dans les Messages Privés.')

		return True

	async def cog_before_invoke(self, ctx: commands.Context):
		ctx.voice_state = self.get_voice_state(ctx)

	

	@commands.hybrid_command(name='join', invoke_without_subcommand=True)
	async def _join(self, ctx: commands.Context):
		"""Rejoindre un canal vocal."""
		destination = ctx.author.voice.channel
		if ctx.voice_state.voice:
			await ctx.voice_state.voice.move_to(destination)
			return
		ctx.voice_state.voice = await destination.connect()
		await ctx.guild.change_voice_state(channel=destination, self_deaf=True)
		await ctx.send(f'Connecté à {destination}.', ephemeral=True)

	@commands.hybrid_command(name='summon')
	@commands.has_permissions(manage_guild=True)
	async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel):
		"""Invoque le bot sur un canal vocal. Si aucun canal n'a été spécifié, il rejoint votre canal."""
		
		if not channel and not ctx.author.voice:
			raise ctx.send('Vous n\'êtes ni connecté à un canal vocal ni n\'avez spécifié un canal à rejoindre.', ephemeral=True)

		destination = channel or ctx.author.voice.channel
		if ctx.voice_state.voice:
			await ctx.voice_state.voice.move_to(destination)
			return

		ctx.voice_state.voice = await destination.connect()
		await ctx.send(f'Connecté au canal {destination.name}', ephemeral=True)	

	def is_in_guild(guild_id):
		async def predicate(ctx):
			return ctx.guild and ctx.guild.id == guild_id
		return commands.check(predicate)

	@commands.hybrid_command(name='leave', aliases=['disconnect', 'deco'])
	async def _leave(self, ctx: commands.Context):
		"""Efface la file d'attente et quitte le canal vocal."""
		
		role_names = [role.name for role in ctx.author.roles]
		if any([ctx.author.guild_permissions.manage_guild, ctx.guild.get_role(907589778734718976) in ctx.author.roles, 'DJ' in role_names, 'admin' in role_names, 'Admins' in role_names, 'Moderators' in role_names]):

			if not ctx.voice_state.voice:
				return await ctx.send('Non connecté à un canal vocal.', ephemeral=True)

			await ctx.voice_state.stop()
			del self.voice_states[ctx.guild.id]

			await ctx.send("<a:yes_animated:844992841938894849> Correctement déconnecté du canal vocal.", ephemeral=True)

	@commands.hybrid_command(name='volume')
	async def _volume(self, ctx: commands.Context, *, volume: int):
		"""Règle le volume du lecteur."""
  
		role_names = [role.name for role in ctx.author.roles]
		if any([ctx.author.guild_permissions.manage_guild, ctx.guild.get_role(907589778734718976) in ctx.author.roles, 'DJ' in role_names, 'admin' in role_names, 'Admins' in role_names, 'Moderators' in role_names]):
	  
			if not ctx.voice_state.is_playing:
				return await ctx.send('Rien n\'est joué pour le moment.', ephemeral=True)

			if 0 > volume > 100:
				return await ctx.send('Le volume doit être compris entre 0 et 100%')

			ctx.voice_state.volume = volume / 100
			await ctx.send('Volume du lecteur réglé sur {}%'.format(volume))

	@commands.hybrid_command(name='now', aliases=['current', 'playing'])
	async def _now(self, ctx: commands.Context):
		"""Affiche la chanson en cours de lecture."""
		if not ctx.voice_state.is_playing:
			return await ctx.send('Rien n\'est joué pour le moment.', ephemeral=True)
		await ctx.send(embed=ctx.voice_state.current.create_embed())

	@commands.hybrid_command(name='stop')
	async def _stop(self, ctx: commands.Context):
		"""Arrête la lecture de la chanson et efface la file d'attente."""
  
		role_names = [role.name for role in ctx.author.roles]
		if any([ctx.author.guild_permissions.manage_guild, ctx.guild.get_role(907589778734718976) in ctx.author.roles, 'DJ' in role_names, 'admin' in role_names, 'Admins' in role_names, 'Moderators' in role_names]):

			ctx.voice_state.songs.clear()

			if not ctx.voice_state.is_playing:
				ctx.voice_state.voice.stop()
				await ctx.send('<a:yes_animated:844992841938894849> Arrêté.', ephemeral=True)

	@commands.hybrid_command(name='skip')
	async def _skip(self, ctx: commands.Context):
		"""Vote pour skip une chanson. 3 votes sont nécessaires pour que la chanson soit skip."""

		if not ctx.voice_state.is_playing:
			return await ctx.send('Je ne joue pas de musique en ce moment...', ephemeral=True)

		if not ctx.voice_state.songs:
			return await ctx.send('La file d\'attente est vide.', ephemeral=True)

		voter = ctx.message.author
		if voter == ctx.voice_state.current.requester:
			await ctx.message.add_reaction('⏭')
			ctx.voice_state.skip()

		elif voter.id not in ctx.voice_state.skip_votes:
			ctx.voice_state.skip_votes.add(voter.id)
			total_votes = len(ctx.voice_state.skip_votes)

			if total_votes >= 3:
				await ctx.message.add_reaction('⏭')
				ctx.voice_state.skip()
			else:
				await ctx.send('Vote pour skip ajouté, actuellement à **{}/3**'.format(total_votes))

		else:
			await ctx.send('Vous avez déjà voté pour skip cette chanson.', ephemeral=True)

	@commands.hybrid_command(name='forceskip', aliases=['fs'])
	@commands.is_owner()
	async def _forceskip(self, ctx: commands.Context):
		"""Vote pour forcer le skip d'une chanson.
		"""
		if not ctx.voice_state.is_playing:
			return await ctx.send('Je ne joue pas de musique en ce moment...', ephemeral=True)

		if not ctx.voice_state.songs:
			return await ctx.send('La file d\'attente est vide.', ephemeral=True)

		voter = ctx.message.author
		if voter == ctx.voice_state.current.requester:
			await ctx.message.add_reaction('⏭')
			ctx.voice_state.skip()

	@commands.hybrid_command(name='queue')
	async def _queue(self, ctx: commands.Context, *, page: int = 1):
		"""Affiche la file d'attente du lecteur.
		"""

		if len(ctx.voice_state.songs) == 0:
			return await ctx.send('File d\'attente vide.', ephemeral=True)

		items_per_page = 10
		pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

		start = (page - 1) * items_per_page
		end = start + items_per_page

		queue = ''
		for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
			queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

		embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
				 .set_footer(text='Page actuelle {}/{}'.format(page, pages)))
		await ctx.send(embed=embed)

	@commands.hybrid_command(name='shuffle')
	async def _shuffle(self, ctx: commands.Context):
		"""Mélange la file d'attente."""

		role_names = [role.name for role in ctx.author.roles]
		if any([ctx.author.guild_permissions.manage_guild, ctx.guild.get_role(907589778734718976) in ctx.author.roles, 'DJ' in role_names, 'admin' in role_names, 'Admins' in role_names, 'Moderators' in role_names]):

			if len(ctx.voice_state.songs) == 0:
				return await ctx.send('File d\'attente vide.', ephemeral=True)

			ctx.voice_state.songs.shuffle()
			await ctx.send('File d\'attente mélangée.')

	@commands.hybrid_command(name='remove')
	async def _remove(self, ctx: commands.Context, index: int):
		"""Supprime un morceau de la file d'attente à un numéro donné."""
  
		role_names = [role.name for role in ctx.author.roles]
		if any([ctx.author.guild_permissions.manage_guild, ctx.guild.get_role(907589778734718976) in ctx.author.roles, 'DJ' in role_names, 'admin' in role_names, 'Admins' in role_names, 'Moderators' in role_names]):

			if len(ctx.voice_state.songs) == 0:
				return await ctx.send('File d\'attente vide.', ephemeral=True)

			ctx.voice_state.songs.remove(index - 1)
			await ctx.send('Morceau supprimé.')

	@commands.hybrid_command(name='loop')
	async def _loop(self, ctx: commands.Context):
		"""Met en boucle le morceau en cours de lecture. Refais cette commande pour annuler la boucle."""

		if not ctx.voice_state.is_playing:
			return await ctx.send('Rien n\'est joué en ce moment.', ephemeral=True)

		# Inverse boolean value to loop and unloop.
		ctx.voice_state.loop = not ctx.voice_state.loop
		await ctx.send('Loop {}.'.format('activé' if ctx.voice_state.loop else 'désactivé'))
		
	@commands.hybrid_command(name='pause')
	async def _pause(self, ctx:commands.Context):
		"""Met en pause la chanson en cours"""

		role_names = [role.name for role in ctx.author.roles]
		if any([ctx.author.guild_permissions.manage_guild, ctx.guild.get_role(907589778734718976) in ctx.author.roles, 'DJ' in role_names, 'admin' in role_names, 'Admins' in role_names, 'Moderators' in role_names]):
	  
			ctx.voice_client.pause()
			await ctx.send('Morceau en pause.')

	@commands.hybrid_command(name='resume')
	async def _resume(self, ctx:commands.Context):
		"""Reprends la chanson en cours"""

		role_names = [role.name for role in ctx.author.roles]
		if any([ctx.author.guild_permissions.manage_guild, ctx.guild.get_role(907589778734718976) in ctx.author.roles, 'DJ' in role_names, 'admin' in role_names, 'Admins' in role_names, 'Moderators' in role_names]):
		
			ctx.voice_client.resume()
			await ctx.send('Morceau en cours.', ephemeral=True)

	@commands.hybrid_command(name='play', aliases=['p'])
	@commands.cooldown(1, 15, commands.BucketType.guild)
	async def _play(self, ctx: commands.Context, *, search: str):
		"""Joue une chanson.
		S'il y a des chansons en attente, celles-ci seront mises en attente.
		"""
		await ctx.defer()
		if not ctx.voice_state.voice:
			await ctx.invoke(self._join)

		# async with ctx.typing():
		try:
			source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
		except YTDLError as e:
			await ctx.send('Une erreur s\'est produite lors du traitement de cette demande : {}'.format(str(e)), ephemeral=True)
		else:
			song = Song(source)
			test = source.duration
			if "hours" in str(test):
				await ctx.send('Cette chanson est trop longue. (plus de 1 heure)', ephemeral=True)
			else:
				await ctx.voice_state.songs.put(song)
				await ctx.send('Prochaine musique : {}'.format(str(source)))


	@_join.before_invoke
	@_play.before_invoke
	async def ensure_voice_state(self, ctx: commands.Context):
		if not ctx.author.voice or not ctx.author.voice.channel:
			await ctx.send('Vous n\'êtes connecté à aucun canal vocal.', ephemeral=True)
		
		if ctx.voice_client:
			if ctx.voice_client.channel != ctx.author.voice.channel:
				await ctx.send('Le Bot est déjà dans un canal vocal.', ephemeral=True)


async def setup(bot: DiscordBot):
	await bot.add_cog(Musicplayer(bot))