import discord
from discord.ext import commands
import random

def get_embed(_title, _description, _color):
    return discord.Embed(title=_title, description=_description, color=_color)

class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='impo')
    async def findimposter(self, ctx):
        """Impostors can sabotage the reactor, 
        which gives Crewmates 30–45 seconds to resolve the sabotage. 
        If it is not resolved in the allotted time, The Impostor(s) will win."""


        # determining
        embed1 = discord.Embed(title = "Who's the imposter?" , description = "Find out who the imposter is, before the reactor breaks down!" , color=0xff0000)
        
        # fields
        embed1.add_field(name = 'Red' , value= '<:red_square:849223170523267073>' , inline=False)
        embed1.add_field(name = 'Blue' , value= '<:blue_square:849223194825064488>' , inline=False)
        embed1.add_field(name = 'Green' , value= '<:green_square:849223240894644244>' , inline=False)
        embed1.add_field(name = 'White' , value= '<:white_large_square:849223407149383750>' , inline=False)
        
        # sending the message
        msg = await ctx.send(embed=embed1)
        
        # emojis
        emojis = {
            'red': '<:red_square:849223170523267073>',
            'blue': '<:blue_square:849223194825064488>',
            'green': '<:green_square:849223240894644244>',
            'white': '<:white_large_square:849223407149383750>'
        }
        
        # who is the imposter?
        imposter = random.choice(list(emojis.items()))
        imposter = imposter[0]
        
        # for testing...
        print(emojis[imposter])
        
        # adding choices
        for emoji in emojis.values():
            await msg.add_reaction(emoji)
        
        # a simple check, whether reacted emoji is in given choises.
        def check(reaction, user):
            self.reacted = reaction.emoji
            return user == ctx.author and str(reaction.emoji) in emojis.values()

        # waiting for the reaction to proceed
        try: 
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        
        except TimeoutError:
            # reactor meltdown - defeat
            description = "Reactor Meltdown.{0} was the imposter...".format(imposter)
            embed = get_embed("Defeat", description, discord.Color.red())
            await ctx.send(embed=embed)
        else:
            # victory
            if str(self.reacted) == emojis[imposter]:
                description = "**{0}** was the imposter...".format(imposter)
                embed = get_embed("Victory", description, discord.Color.blue())
                await ctx.send(embed=embed)

            # defeat
            else:
                for key, value in emojis.items(): 
                    if value == str(self.reacted):
                        description = "**{0}** was not the imposter...".format(key)
                        embed = get_embed("Defeat", description, discord.Color.red())
                        await ctx.send(embed=embed)
                        break


def setup(bot):
    bot.add_cog(games(bot))