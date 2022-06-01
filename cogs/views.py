import discord

from discord.ext import commands
from views import bool
from views import dropdown
from views import link
from views import modal

class Views(commands.Cog, name="views"):
	"""Cogs expérimentales, nouvelles fonctionnalités telles que les boutons, la liste déroulante ou le chuchotement."""
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

	def help_custom(self) -> tuple[str]:
		emoji = '🔘'
		label = "Views"
		description = "Démo : Nouvelles fonctionnalités du discord."
		return emoji, label, description

	@commands.command(name="bool")
	@commands.guild_only()
	async def boo(self, ctx):
		"""Découvrez la fonctionnalité des boutons avec cette commande."""
		view = bool.View(flabel="D'accord", slabel="Pas d'accord", sstyle=discord.ButtonStyle.red, emojis = True, source=ctx)
		await ctx.send("Démonstration de l'utilisation de la fonction Bool !", view=view)

	@commands.command(name="dropdown")
	@commands.guild_only()
	async def dro(self, ctx):
		"""Découvrez la fonctionnalité du menu de sélection avec cette commande."""
		options = [
			{"label":"Mandarin", "description":"你好", "emoji":"🇨🇳"},
			{"label":"Spanish", "description":"Buenos dias", "emoji":"🇪🇸"},
			{"label":"English", "description":"Hello", "emoji":"🇬🇧"},
			{"label":"Hindi", "description":"नमस्ते", "emoji":"🇮🇳"},
			{"label":"Arabic", "description":"صباح الخير", "emoji":"🇸🇦"},
			{"label":"Potuguese", "description":"Olá", "emoji":"🇵🇹"},
			{"label":"Bengali", "description":"হ্যালো", "emoji":"🇧🇩"},
			{"label":"Russian", "description":"Привет", "emoji":"🇷🇺"},
			{"label":"Japanese", "description":"こんにちは", "emoji":"🇯🇵"},
			{"label":"Turkish", "description":"Merhaba", "emoji":"🇹🇷"},
			{"label":"Korean", "description":"안녕하십니까", "emoji":"🇰🇷"},
			{"label":"French", "description":"Bonjour", "emoji":"🇫🇷"},
			{"label":"German", "description":"Hallo", "emoji":"🇩🇪"},
			{"label":"Vietnamese", "description":"xin chào", "emoji":"🇻🇳"},
			{"label":"Italian", "description":"Buongiorno", "emoji":"🇮🇹"},
			{"label":"Polish", "description":"dzień dobry", "emoji":"🇵🇱"},
			{"label":"Romanian", "description":"Buna ziua", "emoji":"🇷🇴"},
			{"label":"Dutch", "description":"Hallo", "emoji":"🇳🇱"},
			{"label":"Thai", "description":"สวัสดี", "emoji":"🇹🇭"},
			{"label":"Nepali", "description":"नमस्कार", "emoji":"🇳🇵"},
			{"label":"Greek", "description":"γεια σας", "emoji":"🇬🇷"},
			{"label":"Czech", "description":"Ahoj", "emoji":"🇨🇿"},
			{"label":"Persian", "description":"سلام", "emoji":"🇮🇷"}
		]
		view = dropdown.View(options=options, placeholder="Sélectionnez votre/vos langue(s)", min_val=1, max_val=9, source=ctx)
		await ctx.send("Démonstration de l'utilisation de la fonction Dropdown !", view=view)

	@commands.command(name="link")
	@commands.guild_only()
	async def lin(self, ctx):
		"""Découvrez le lien dans un bouton avec cette fonctionnalité."""
		view = link.View(label="Code source sur Github", url="https://github.com/RomainNicolaon/LavaL_Bot")
		await ctx.send("Découvrez ce qui se cache derrière LavaL Bot !", view=view)

	@commands.command(name="modal")
	@commands.guild_only()
	async def moda(self, ctx):
		"""Découvrez le lien dans cette feature."""
		view = modal.View(invoke=ctx)
		await ctx.send(view=view)

async def setup(bot):
	await bot.add_cog(Views(bot))