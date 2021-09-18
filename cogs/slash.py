from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Slash(commands.Cog, name="slash"):
    """Slash description"""

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="ping")
    async def ping(self, ctx: SlashContext):
        await ctx.send(content="Pong!")
    
def setup(bot):
    bot.add_cog(Slash(bot))