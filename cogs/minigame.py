import discord
from discord.ext import commands
import random


class Minigame(commands.Cog, name="minigame", command_attrs=dict(hidden=False)):
	"""Description des commandes des mini-jeux"""

	def __init__(self, bot):
		self.bot = bot
		self.gameOver = True
		self.player1 = ""
		self.player2 = ""
		self.turn = ""
		self.board = []
		self.winningConditions = [
			[0, 1, 2],
			[3, 4, 5],
			[6, 7, 8],
			[0, 3, 6],
			[1, 4, 7],
			[2, 5, 8],
			[0, 4, 8],
			[2, 4, 6]
		]
		
	def help_custom(self):
		emoji = '🎮'
		label = "Mini-jeux"
		description = "Commandes des mini-jeux, comme le TicTacToe (le Morpion en français)"
		return emoji, label, description

	@commands.command(name='tictactoe', aliases=['ttt'])
	async def tictactoe(self, ctx, p1: discord.Member, p2: discord.Member):
		"""Commande pour jouer au TicTacToe (le Morpion en français)"""
		if self.gameOver:
			self.board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
						  ":white_large_square:", ":white_large_square:", ":white_large_square:",
						  ":white_large_square:", ":white_large_square:", ":white_large_square:"]
			self.turn = ""
			self.gameOver = False
			self.count = 0
			self.player1 = p1
			self.player2 = p2
			# print the board
			line = ""
			for x in range(len(self.board)):
				if x == 2 or x == 5 or x == 8:
					line += " " + self.board[x]
					await ctx.send(line)
					line = ""
				else:
					line += " " + self.board[x]

			# determine who goes first
			num = random.randint(1, 2)
			if num == 1:
				self.turn = self.player1
				await ctx.send("Ce sera <@" + str(self.player1.id) + "> qui débute la partie !")
			elif num == 2:
				self.turn = self.player2
				await ctx.send("Ce sera <@" + str(self.player2.id) + "> qui débute la partie !")
		else:
			await ctx.send("Une partie est déjà en cours ! Terminez-la avant d'en commencer une nouvelle.")

	@commands.command(name='place', aliases=['tpl'])
	async def place(self, ctx, pos: int):
		"""Commande pour placer ses pions"""
		if not self.gameOver:
			mark = ""
			if self.turn == ctx.author:
				if self.turn == self.player1:
					mark = ":regional_indicator_x:"
				elif self.turn == self.player2:
					mark = ":o2:"
				if 0 < pos < 10 and self.board[pos - 1] == ":white_large_square:":
					self.board[pos - 1] = mark
					self.count
					# print the board
					line = ""
					for x in range(len(self.board)):
						if x == 2 or x == 5 or x == 8:
							line += " " + self.board[x]
							await ctx.send(line)
							line = ""
						else:
							line += " " + self.board[x]

					self.checkWinner(self.winningConditions, mark)
					print(self.count)
					if self.gameOver == True:
						await ctx.send(mark + "a gagné !")
					elif self.count >= 9:
						self.gameOver = True
						await ctx.send("C'est un match nul !")

					# switch turns
					if self.turn == self.player1:
						self.turn = self.player2
					elif self.turn == self.player2:
						self.turn = self.player1
					else:
						await ctx.send("Veillez à choisir un nombre entier compris entre **1 et 9 (__inclus__)** représentant une case **__non marquée__**.")
			else:
				await ctx.send("Ce n'est pas votre tour !")
		else:
			await ctx.send("Veuillez commencer une nouvelle partie en utilisant la commande `?tictactoe` ou `?ttt`")

	def checkWinner(self, winningConditions, mark):
		for condition in winningConditions:
			if self.board[condition[0]] == mark and self.board[condition[1]] == mark and self.board[condition[2]] == mark:
				self.gameOver = True

	@tictactoe.error
	async def tictactoe_error(self, ctx, error):
		print(error)
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Veuillez mentionner 2 joueurs pour utiliser cette commande.")
		elif isinstance(error, commands.BadArgument):
			await ctx.send("N'oubliez pas de mentionner les joueurs. (ex: <@405414058775412746>).")

	@place.error
	async def place_error(ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Veuillez saisir une position que vous souhaitez cocher")
		elif isinstance(error, commands.BadArgument):
			await ctx.send("Veillez à saisir un nombre entier.")
			
	@commands.command(name='tictactoehelp', aliases=['th'])
	async def tictactoehelp(self, ctx):
		"""Donne des informations sur la commande `tictactoe`"""
		await ctx.message.reply("Pour commencer une nouvelle partie, utilisez la commande `?tictactoe` ou `?ttt` puis pour jouer utilisez `?place` ou `?tpl`")


def setup(bot):
	bot.add_cog(Minigame(bot))
