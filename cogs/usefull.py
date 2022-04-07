import discord

from discord.ext import commands


class Usefull(commands.Cog, name="usefull", command_attrs=dict(hidden=False)):
	"""Commandes utiles pour les développeurs et autres"""
	def __init__(self, bot):
		self.bot = bot

	def help_custom(self):
		emoji = '🚩'
		label = "Utile"
		description = "Commandes utiles."
		return emoji, label, description

	@commands.command(name='strawpoll', aliases=['straw', 'stp', 'sond', 'sondage'], pass_context=True)
	async def strawpool(self, ctx, *, context):
		"""Posez un sondage, et ajoutez 2 réactions pour voter avec votre communauté."""
		crossmark, checkmark = self.bot.get_emoji(844992804480352257), self.bot.get_emoji(844992841938894849)
		await ctx.message.delete()
		message = await ctx.send("__*" + ctx.message.author.mention + "*__ : " + context)
		await message.add_reaction(emoji=checkmark)
		await message.add_reaction(emoji=crossmark)

	@commands.command(name='emojilist', aliases=['ce', 'el'], pass_context=True)
	async def getcustomemojis(self, ctx):
		"""Renvoie une liste de tous les emojis cutom du serveur actuel."""
		embed_list, embed = [], discord.Embed(title="Liste d'emojis personnalisés ("+str(len(ctx.guild.emojis))+") :")
		for i, emoji in enumerate(ctx.guild.emojis, start=1):
			if i == 0 : i += 1
			value = "`<:"+str(emoji.name)+":"+str(emoji.id)+">`" if not emoji.animated else "`<a:"+str(emoji.name)+":"+str(emoji.id)+">`"
			embed.add_field(name=str(self.bot.get_emoji(emoji.id))+" - **:"+str(emoji.name)+":** - (*"+str(i)+"*)",value=value)
			if i%6.25 == 400%6.25 and i != 0:
				embed_list.append(embed)
				embed = discord.Embed()
		embed_list.append(embed)

		for message in embed_list:
			await ctx.send(embed=message)

def setup(bot):
	bot.add_cog(Usefull(bot))
