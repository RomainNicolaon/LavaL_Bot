import discord
import functools

from views.view import View as Parent

class CustomModal(discord.ui.Modal):
	def __init__(self, title: str, fields: dict[str, discord.ui.TextInput], when_submit: functools.partial):
		super().__init__(title=title)

		self.values : dict[str, str] = {}
		self.when_submit = when_submit

		self.__fields : dict[str, functools.partial] = {}
		for i, item in enumerate(fields.items()):
			key, value = item
			self.__fields[key] = functools.partial(self.__get_value, self.add_item(value).children[i])

	def __get_value(self, children: discord.ui.TextInput) -> str:
		return children.value

	async def on_submit(self, interaction: discord.Interaction):
		for key, value in self.__fields.items():
			self.values[key] = value()

		await self.when_submit(self, interaction)