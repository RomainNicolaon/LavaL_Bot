import discord

from datetime import datetime
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice

class PrivateVocal(commands.Cog, name="privatevocal"):
	"""
		Créez et gérez des canaux vocaux privés.
	
		Require intents:
			- voice_states
		
		Require bot permission:
			- manage_channels
			- manage_permissions
			- move_members
	"""
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot
		self.private_config = bot.config["bot"]["private_vocal"]

		self.tracker = dict()
		self.MAIN_CHANNEL_NAME = self.private_config["main_channel_name"]
		self.CHANNEL_NAME = self.private_config["channel_name"]

	def help_custom(self) -> tuple[str]:
		emoji = '💭'
		label = "Private Vocal"
		description = "Créez un canal vocal privé."
		return emoji, label, description

	def __guild_in(self, member: discord.Member) -> None:
		if not member.guild.id in self.tracker: 
				self.tracker[member.guild.id] = dict()
				self.tracker[member.guild.id]["cooldown"] = dict()
				self.tracker[member.guild.id]["channels"] = dict()

	def __is_join_channel(self, channel: discord.VoiceChannel) -> bool:
		return channel.user_limit == 1 and channel.name == self.MAIN_CHANNEL_NAME
	
	def __is_user_on_cooldown(self, user: discord.Member, guild_cooldown: dict):
		return (user.id in guild_cooldown) and datetime.now().timestamp() - guild_cooldown[user.id].timestamp() < self.private_config["cooldown"]

	@commands.Cog.listener("on_voice_state_update")
	async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
		self.__guild_in(member)
		guild_id = self.tracker[member.guild.id]
		guild_cooldown = guild_id["cooldown"]
		guild_channels = guild_id["channels"]

		if after.channel is not None and self.__is_join_channel(after.channel):
			if self.__is_user_on_cooldown(member, guild_cooldown):
				await member.move_to(None)
				remaining = self.private_config["cooldown"] - (datetime.now() - guild_cooldown[member.id]).total_seconds()
				await member.send(f"Désolé, vous êtes en cooldown, temps restant : `{round(remaining)}` secondes.")
			
			else:
				private_vocal = await member.guild.create_voice_channel(self.CHANNEL_NAME.format(user = member), category=after.channel.category)
				await member.move_to(private_vocal)
				guild_cooldown[member.id] = datetime.now()
				guild_channels[private_vocal.id] = member.id

		if before.channel is not None and before.channel.id in guild_channels:
			if members := before.channel.members:
				user = members[0]
				guild_channels[before.channel.id] = user.id
				await before.channel.edit(name=self.CHANNEL_NAME.format(user = user))
			
			else:
				del guild_id["channels"][before.channel.id]
				await before.channel.delete()

	@app_commands.command(name="limitusers", description="Limite le nombre de personnes dans un channel vocal.")
	@app_commands.choices(limit=[Choice(name=str(i), value=i) for i in range(1, 16)])
	@app_commands.guilds(discord.Object(id=953311718275153941))
	@app_commands.checks.has_permissions(use_slash_commands=True)
	async def ping(self, interaction: discord.Interaction, limit:int=None):
		try:
			actual_channel = interaction.user.voice.channel
			members_in_chanel = len(interaction.channel.members)-1
			if limit is None:
				limit = 1
				await actual_channel.edit(user_limit=members_in_chanel)
			else:
				await actual_channel.edit(user_limit=limit)
			await interaction.response.send_message(f"Le nombre d'utilisateurs dans le channel vocal a été limité à `{limit}`.", ephemeral=True)
		except Exception as e:
			await interaction.response.send_message(f"<a:no_animated:844992804480352257> Tu dois être dans un salon vocal pour utiliser cette commande !", ephemeral=True)

async def setup(bot):
	await bot.add_cog(PrivateVocal(bot))