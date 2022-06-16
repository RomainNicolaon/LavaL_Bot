import discord
from discord.ext import commands
from views import link

class Welcome(commands.Cog, name="welcome", command_attrs=dict(hidden=False)):
	"""Description des commandes bienvenue"""
	def __init__(self, bot):
		self.bot = bot
		self.subconfig_data: dict = self.bot.config["cogs"][self.__cog_name__.lower()]

	@commands.Cog.listener()
	async def on_member_join(self, member):
		guild = member.guild
		response = await self.bot.database.lookup(self.subconfig_data["table"], "is_active", {"guild_id": str(member.guild.id)})
		if response and response[0][0]:
			if guild.id == 441962473583804416:
				if guild.system_channel:
					embed = discord.Embed(color=0x4a3d9a)
					embed.add_field(name="Bienvenue", value=f"**<@!{member.id}>** vient de rejoindre **{member.guild.name}**", inline=False)
					embed.set_thumbnail(url="https://c.tenor.com/PhhN-3LjE3AAAAAd/gatto-cibo.gif")
					await guild.system_channel.send(embed=embed)
			elif guild.system_channel:
				embed = discord.Embed(color=0x4a3d9a)
				embed.add_field(name="Bienvenue", value=f"**<@!{member.id}>** vient de rejoindre **{member.guild.name}**", inline=False)
				embed.set_thumbnail(url="https://media.tenor.com/images/d139e96072bae377be522258f7128881/tenor.gif")
				await guild.system_channel.send(embed=embed)
		if not response:
			if guild.system_channel:
				embed = discord.Embed(color=0x4a3d9a)
				embed.add_field(name="Bienvenue", value=f"**<@!{member.id}>** vient de rejoindre **{member.guild.name}**", inline=False)
				embed.set_thumbnail(url="https://media.tenor.com/images/d139e96072bae377be522258f7128881/tenor.gif")
				await guild.system_channel.send(embed=embed)

	
	@commands.Cog.listener()
	async def on_member_remove(self, member):
		guild = member.guild
		response = await self.bot.database.lookup(self.subconfig_data["table"], "is_active", {"guild_id": str(member.guild.id)})
		if response and response[0][0]:
			if guild.system_channel:
				if member.id != self.bot.user.id:
					embed = discord.Embed(color=0x4a3d9a)
					embed.add_field(name="Au revoir", value=f"**<@!{member.id}>** vient de quitter **{member.guild.name}**", inline=False)
					embed.set_thumbnail(url="https://i.pinimg.com/originals/2d/02/44/2d024443d7e18982443275923492ec5e.gif")
					await guild.system_channel.send(embed=embed)
	
	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		if guild.system_channel:
			view = link.View(label="Github", url="https://github.com/RomainNicolaon/LavaL_Bot")
			embed = discord.Embed(title="LavaL Bot - Un bot fun et utile créé par LavaL#9240", description="Merci de m'avoir ajouté à ton serveur !\n\nPour commencer, utilises la commande `?help` pour accerder aux commandes disponibles.\nTu peux aussi modifier le préfix du bot en utilisant la commande `?changeprefix`.\nSi tu souhaites activer / désactiver l'envoie de messages de bienvenue et au revoir, fais la commande `?setwelcome 1`\n\n**Nouveau**, les /commands sont arrivées, tape "/" pour afficher la liste des commandes disponibles, tu peux aussi retrouver le code source du bot en cliquant sur le lien ci-dessous.\nSi un problème survient, n'hésites pas à envoyer un message privé à <@!405414058775412746>", color=0x12F932)
			await guild.system_channel.send(embed=embed, view=view)


async def setup(bot):
	await bot.add_cog(Welcome(bot))
