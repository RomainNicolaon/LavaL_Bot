import time
import random
import asyncio
import discord

from datetime import datetime, date
from discord.ext import commands, tasks

class Birthday(commands.Cog, name="birthday"):
	"""Je vous souhaite bientôt un joyeux anniversaire !"""
	def __init__(self, bot):
		self.bot = bot

		self.birthday_data = self.bot.database_data["birthday"]

		self.daily_birthday.start()

	def help_custom(self):
		emoji = '🎁'
		label = "Birthday"
		description = "Peut-être que je vous souhaiterai bientôt un joyeux anniversaire !"
		return emoji, label, description

	def cog_unload(self):
		self.daily_birthday.cancel()

	@tasks.loop(hours=1)
	async def daily_birthday(self):
		if datetime.now().hour == 10:
			guild = self.bot.get_guild(int(self.birthday_data["guild_id"]))
			channel = guild.get_channel(int(self.birthday_data["channel_id"]))

			response = await self.bot.database.select(self.birthday_data["table"], "*")
			for data in response:
				discord_id, date_of_birth = data[0], data[1]

				if date_of_birth.month == datetime.now().month and date_of_birth.day == datetime.now().day:
					timestamp = round(time.mktime(date_of_birth.timetuple()))

					message = f"Je me suis souvenu de cette date parce que c'est l'anniversaire de <@{str(discord_id)}> aujourd'hui !\nIl/Elle est né(e) <t:{timestamp}:R> !"
					images = [
						"https://sayingimages.com/wp-content/uploads/funny-birthday-and-believe-me-memes.jpg",
						"https://i.kym-cdn.com/photos/images/newsfeed/001/988/649/1e8.jpg",
						"https://winkgo.com/wp-content/uploads/2018/08/101-Best-Happy-Birthday-Memes-01-720x720.jpg",
						"https://www.the-best-wishes.com/wp-content/uploads/2022/01/success-kid-cute-birthday-meme-for-her.jpg"]

					embed = discord.Embed(title="🎉 Joyeux anniversaire !", description=message, colour=discord.Colour.dark_gold())
					embed.set_image(url=images[random.randint(0, len(images)-1)])
					await channel.send(embed=embed)

	@daily_birthday.before_loop
	async def before_daily_birthday(self):
		await self.bot.wait_until_ready()
		while self.bot.database.connector is None: await asyncio.sleep(0.01) #wait_for initBirthday

	@commands.command(name='birthday', aliases=['bd', 'setbirthday', 'setbirth', 'birth'])
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def birthday(self, ctx, date: str = None):
		"""Permet de définir/afficher votre date d'anniversaire."""
		if date:
			try:
				dataDate = datetime.strptime(date, "%d/%m/%Y").date()
				if dataDate.year > datetime.now().year - 15 or dataDate.year < datetime.now().year - 99: raise commands.CommandError("Veuillez indiquer votre année de naissance réelle.")
				# Insert
				await self.bot.database.insert(self.birthday_data["table"], {"pseudo": ctx.author.name, "discord_id": ctx.author.id, "date_of_birth": dataDate})
				# Update
				await self.bot.database.update(self.birthday_data["table"], "date_of_birth", dataDate, "discord_id = "+str(ctx.author.id))

				await self.show_birthday_message(ctx, ctx.author)
			except ValueError:
				raise commands.CommandError("Format de date non valide, essaye : `jour/mois/Année`.\nExample : `26/12/1995`")
			except Exception as e:
				raise commands.CommandError(str(e))
		else:
			await self.show_birthday(ctx, ctx.author)

	@commands.command(name='showbirthday', aliases=['showbirth', 'sbd'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def show_birthday(self, ctx, user:discord.Member = None):
		"""Permet d'afficher l'anniversaire de soi même ou d'un utilisateur"""
		if not user: user = ctx.author
		await self.show_birthday_message(ctx, user)

	async def show_birthday_message(self, ctx, user:discord.Member) -> None:
		response = await self.bot.database.lookup(self.birthday_data["table"], "date_of_birth", "discord_id", str(user.id))
		if response:
			dataDate : date = response[0][0]
			timestamp = round(time.mktime(dataDate.timetuple()))
			await ctx.send(f":birthday: L'anniversaire est le <t:{timestamp}:D> et il/elle est né(e) <t:{timestamp}:R>.")
		else:
			await ctx.send(":birthday: Rien n'a été trouvé. Essayez d'enregistrer votre anniversaire en utilisant `?birthday` et réessayez.")

def setup(bot):
	bot.add_cog(Birthday(bot))