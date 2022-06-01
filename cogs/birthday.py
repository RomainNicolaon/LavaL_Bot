import time
import random
import asyncio
import discord

from datetime import datetime, date
from discord.ext import commands, tasks
from discord.utils import get
from discord import app_commands
from discord.app_commands import Choice

class Birthday(commands.Cog, name="birthday"):
	"""
		Enregistres ton anniversaire, et le moment venu, je te souhaiterai un joyeux anniversaire !
		
		Require intents: 
			- default
		
		Require bot permission:
			- None
	"""
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

		self.birthday_data = bot.config["database"]["birthday"]

	def help_custom(self) -> tuple[str, str, str]:
		emoji = '🎁'
		label = "Birthday"
		description = "Peut-être que je vous souhaiterai bientôt un joyeux anniversaire !"
		return emoji, label, description

	async def cog_load(self):
		self.daily_birthday.start()

	async def cog_unload(self):
		self.daily_birthday.cancel()

	@tasks.loop(hours=1)
	async def daily_birthday(self):
		if datetime.now().hour == 9:
			guild = get(self.bot.guilds, id=self.birthday_data["guild_id"])
			channel = get(guild.channels, id=self.birthday_data["channel_id"])

			response = await self.bot.database.select(self.birthday_data["table"], "*")
			for data in response:
				user_id, user_birth = data

				if user_birth.month == datetime.now().month and user_birth.day == datetime.now().day:
					timestamp = round(time.mktime(user_birth.timetuple()))

					message = f"Retenez cette date car c'est l'aniversaire de <@{user_id}> !\nIl/Elle est né(e) <t:{timestamp}:R> !"
					images = [
						"https://sayingimages.com/wp-content/uploads/funny-birthday-and-believe-me-memes.jpg",
						"https://i.kym-cdn.com/photos/images/newsfeed/001/988/649/1e8.jpg",
						"https://winkgo.com/wp-content/uploads/2018/08/101-Best-Happy-Birthday-Memes-01-720x720.jpg",
						"https://www.the-best-wishes.com/wp-content/uploads/2022/01/success-kid-cute-birthday-meme-for-her.jpg"
					]

					embed = discord.Embed(title="🎉 Happy birthday !", description=message, colour=discord.Colour.dark_gold())
					embed.set_image(url=images[random.randint(0, len(images)-1)])
					await channel.send(embed=embed)

	@daily_birthday.before_loop
	async def before_daily_birthday(self):
		await self.bot.wait_until_ready()
		while self.bot.database.connector is None: await asyncio.sleep(0.01) #wait_for initBirthday

	async def year_suggest(self, _: discord.Interaction, current: str):
		years = [str(i) for i in range(datetime.now().year - 99, datetime.now().year - 15)]
		if not current: 
			out = [app_commands.Choice(name=i, value=i) for i in range(datetime.now().year - 30, datetime.now().year - 15)]
		else:
			out = [app_commands.Choice(name=year, value=int(year)) for year in years if str(current) in year]
		if len(out) > 25:
			return out[:25]
		else:
			return out

	async def day_suggest(self, _: discord.Interaction, current: str):
		days = [str(i) for i in range(1, 32)]
		if not current:
			out = [app_commands.Choice(name=i, value=i) for i in range(1, 16)]
		else:
			out = [app_commands.Choice(name=day, value=int(day)) for day in days if str(current) in day]
		if len(out) > 25:
			return out[:25]
		else:
			return out

	@app_commands.command(name="birthday", description="Enregistrez votre propre date d'anniversaire.")
	@app_commands.describe(month="Votre mois de naissance.", day="Votre jour de naissance.", year="Votre année de naissance.")
	@app_commands.choices(month=[Choice(name=datetime(1, i, 1).strftime("%B"), value=i) for i in range(1, 13)])
	@app_commands.autocomplete(day=day_suggest, year=year_suggest)
	@app_commands.checks.cooldown(1, 15.0, key=lambda i: (i.guild_id, i.user.id))
	async def birthday(self, interaction: discord.Interaction, month: int, day: int, year: int):
		"""Permet de définir/afficher votre date d'anniversaire."""
		if day > 31 or day < 0 or year > datetime.now().year - 15 or year < datetime.now().year - 99:
			raise ValueError("Veuillez fournir une date de naissance réelle.")

		try:
			dataDate = datetime.strptime(f"{day}{month}{year}", "%d%m%Y").date()
			if dataDate.year > datetime.now().year - 15 or dataDate.year < datetime.now().year - 99: 
				raise commands.CommandError("Veuillez indiquer votre année de naissance réelle.")
			exist = await self.bot.database.exist(self.birthday_data["table"], "*", f"user_id={interaction.user.id}")
			if exist:
				await self.bot.database.update(self.birthday_data["table"], "user_birth", dataDate, f"user_id = {interaction.user.id}")
			else:
				await self.bot.database.insert(self.birthday_data["table"], {"user_id": interaction.user.id, "user_birth": dataDate})

			await self.show_birthday_message(interaction, interaction.user)
		except Exception as e:
			raise commands.CommandError(str(e))

	@app_commands.command(name="showbirthday", description="Affichee l'anniversaire d'un utilisateur.")
	@app_commands.describe(user="Obtenir la date de naissance de cet utilisateur.")
	@app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
	async def show_birthday(self, interaction: discord.Interaction, user: discord.Member = None):
		"""Permet d'afficher l'anniversaire des autres utilisateurs."""
		if not user: 
			user = interaction.user
		await self.show_birthday_message(interaction, user)

	async def show_birthday_message(self, interaction: discord.Interaction, user:discord.Member) -> None:
		response = await self.bot.database.lookup(self.birthday_data["table"], "user_birth", "user_id", str(user.id))
		if response:
			dataDate : date = response[0][0]
			timestamp = round(time.mktime(dataDate.timetuple()))
			await interaction.response.send_message(f":birthday: Ton anniversaire est <t:{timestamp}:D> et tu es né(e) <t:{timestamp}:R>.")
		else:
			await interaction.response.send_message(":birthday: Rien n'a été trouvé. Réglez l'anniversaire et réessayez.")


async def setup(bot):
	await bot.add_cog(Birthday(bot))
