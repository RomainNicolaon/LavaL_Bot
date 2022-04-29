import discord

from views.view import View as Parent

class SampleModal(discord.ui.Modal, title="Exemple de Modal"):
	name = discord.ui.TextInput(
		label = "Nom (requis)",
		placeholder = "Votre nom ici...",
		required = True,
		min_length = 3
	)

	feedback = discord.ui.TextInput(
		label = "Que pensez-vous de cette nouvelle fonctionnalité ?",
		placeholder = "Tapez vos commentaires ici...",
		style = discord.TextStyle.long,
		required = False,
		max_length = 300
	)

	async def on_submit(self, interaction: discord.Interaction):
		await interaction.response.send_message(f"Merci pour vos commentaires, `{self.name.value}` !\n{self.feedback.value}", ephemeral=True)

	async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
		await interaction.response.send_message("Oups ! Quelque chose a mal tourné.", ephemeral=True)


class View(Parent):
	"""Button to Modal"""
	def __init__(self, source, label, style=discord.ButtonStyle.grey, emoji=None, disabled=False):
		super().__init__()
		self.source = source
		self.button.label = label
		self.button.style = style
		self.button.emoji = emoji
		self.button.disabled = disabled

	async def button_func(self, interaction: discord.Interaction):
		if self.source.author != interaction.user:
			await interaction.response.send_message("Vous ne pouvez pas ouvrir ce Modal.", ephemeral=True)
		else:
			await interaction.response.send_modal(SampleModal())

	@discord.ui.button(style = discord.ButtonStyle.blurple)
	async def button(self, interaction: discord.Interaction, button: discord.ui.Button):
		await self.button_func(interaction)