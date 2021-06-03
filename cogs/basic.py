from os import name
import time
import discord

from discord.ext import commands


class Basic(commands.Cog, name="basic"):
    """Basic description"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases=['?', 'h', 'commands'])
    async def help(self, ctx):
        page1 = discord.Embed(
            title='Commandes générales',
            description='Page 1/7',
            colour=discord.Colour.orange())
        page1.add_field(name="```?help``` ```??``` ```?h```",
                        value="Liste de toute les commandes", inline=False)
        page1.add_field(name="```?infos``` ```?i```",
                        value="Donne des informations sur le bot", inline=False)
        page1.add_field(name="```?server``` ```?serv``` ```?s```",
                        value="Donne des informations sur le serveur", inline=False)
        page1.add_field(name="```?ping```",
                        value="Temps de réponse du bot", inline=False)
        page1.add_field(name="```?avatar``` ```?a```",
                        value="Affiche la photo de profil de la personne mentionnée", inline=False)

        page2 = discord.Embed(
            title='Commandes fun',
            description='Page 2/7',
            colour=discord.Colour.orange())
        page2.add_field(
            name="```?punch```", value="Frappe violemment la personne mentionnée", inline=False)
        page2.add_field(
            name="```?kiss```", value="Embrasse passionnément la personne mentionnée", inline=False)
        page2.add_field(
            name="```?hug```", value="Faire un gros câlin à la personne mentionnée", inline=False)
        page2.add_field(
            name="```?stat``` ```?status``` ```?graph``` ```?gs``` ```?sg```", value="Stats", inline=False)
        page2.add_field(name="```?emojilist``` ```?ce``` ```?el```",
                        value="Emoji list", inline=False)

        page3 = discord.Embed(
            title='Commandes fun',
            description='Page 3/7',
            colour=discord.Colour.orange())
        page3.add_field(
            name="```?addprivate {channel}``` ```?create``` ```?add``` ```?+``` ```?>```", value="Nouveau salon textuel", inline=False)
        page3.add_field(name="```?delprivate {channel}``` ```?delete``` ```?del``` ```?-``` ```?<```",
                        value="Supprimer salon textuel", inline=False)
        page3.add_field(name="```?spotify``` ```?spy``` ```?spot```",
                        value="Infos spotify", inline=False)
        page3.add_field(
            name="```?strawpoll``` ```?straw``` ```?stp``` ```?sond``` ```?sondage```", value="Sondage", inline=False)
        page3.add_field(name="```?streamers``` ```?st```",
                        value="Liste des meilleurs streamers", inline=False)

        page4 = discord.Embed(
            title='Commandes admin',
            description='Page 4/7',
            colour=discord.Colour.orange())
        page4.add_field(name="```?deletechannel {channel}``` ```?dc```",
                        value="Supprimer le channel choisi", inline=False)
        page4.add_field(
            name="```?deletemessage {n}``` ```?dm```", value="Supprimer n messages", inline=False)

        page5 = discord.Embed(
            title='Commandes Musique',
            description='Page 5/7',
            colour=discord.Colour.orange())
        page5.add_field(name="```?join```",
                        value="Le bot rejoint ton salon vocal", inline=False)
        page5.add_field(name="```?summon```",
                        value="Le bot rejoins le salon vocal de ton choix", inline=False)
        page5.add_field(name="```?leave```",
                        value="Le bot quitte le salon vocal", inline=False)
        page5.add_field(
            name="```?play```", value="Jouer une musique (nom ou lien Youtube)", inline=False)
        page5.add_field(name="```?skip```",
                        value="Passe à la prochaine muqiue", inline=False)

        page6 = discord.Embed(
            title='Commandes Musique',
            description='Page 6/7',
            colour=discord.Colour.orange())
        page6.add_field(name="```?now```",
                        value="Musique en cours", inline=False)
        page6.add_field(name="```?pause```",
                        value="Musique en pause", inline=False)
        page6.add_field(name="```?resume```",
                        value="Reprise de la musique", inline=False)
        page6.add_field(name="```?stop```",
                        value="La musique s'arrete", inline=False)

        page7 = discord.Embed(
            title='Commandes Musique',
            description='Page 7/7',
            colour=discord.Colour.orange())
        page7.add_field(name="```?queue```",
                        value="Affiche la liste des musiques", inline=False)
        page7.add_field(name="```?shuffle```",
                        value="Lecture des musiques en aléatoire", inline=False)
        page7.add_field(name="```?remove```",
                        value="SUpprime une musique de la liste", inline=False)
        page7.add_field(name="```?loop```",
                        value="Lecture en boucle", inline=False)

        pages = [page1, page2, page3, page4, page5, page6, page7]

        message = await ctx.send(embed=page1)
        await message.add_reaction('⏮')
        await message.add_reaction('◀')
        await message.add_reaction('▶')
        await message.add_reaction('⏭')

        def check(reaction, user):
            return user == ctx.author

        i = 0
        reaction = None

        while True:
            if str(reaction) == '⏮':
                i = 0
                await message.edit(embed=pages[i])
            elif str(reaction) == '◀':
                if i > 0:
                    i -= 1
                    await message.edit(embed=pages[i])
            elif str(reaction) == '▶':
                if i < 6:
                    i += 1
                    await message.edit(embed=pages[i])
            elif str(reaction) == '⏭':
                i = 6
                await message.edit(embed=pages[i])

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                await message.remove_reaction(reaction, user)
            except:
                break

        await message.clear_reactions()

    @commands.command(name='ping', pass_context=True)
    async def ping(self, ctx):
        before = time.monotonic()
        message = await ctx.message.reply(":ping_pong: Pong !")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f":ping_pong: Pong ! in `{float(round(ping/1000.0,3))}s` ||{int(ping)}ms||")

    @commands.command(name='server', aliases=['serv', 's'])
    async def server(self, ctx):
        embed = discord.Embed(title="Donne des informations sur le serveur", color=0x12F932, description="Ce serveur s'appelle "+str(ctx.message.guild.name) +
                              " et totalise "+str(ctx.message.guild.member_count)+" membres et son créateur est <@!" + str(ctx.message.guild.owner_id)+">.", colour=discord.Colour(0x12F932))

        embed.set_thumbnail(
            url="https://steemitimages.com/DQmbQ9tUdvP98ruzMX6gCjXWz6N5yMBHbn7oJ1WeiiQoj68/16361360.png")

        embed.set_footer(text="Requested by : "+str(ctx.message.author.name) + " " +
                         str(time.strftime('%H:%M:%S')), icon_url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name='alliasinfos', aliases=['all', 'allias'])
    async def alliasinfos(self, ctx, *input):
        """Show help command, use : help {COMMAND/CATEGORY}"""
        embed = discord.Embed()
        remind = "\n**Remind** : Hooks such as {} must not be used when executing commands."
        title, description, color = "Help · ", "", discord.Color.blue()
        if not input:
            category_list = ''
            for cog in self.bot.cogs:
                cog_settings = self.bot.get_cog(cog).__cog_settings__
                if len(cog_settings) == 0 or not cog_settings['hidden']:
                    category_list += "{**"+str(cog).upper()+"**}\n *" + \
                        str(self.bot.cogs[cog].__doc__)+"*\n"
            embed.add_field(name="Category :",
                            value=category_list, inline=False)

        elif len(input) == 1:
            search, search_command, search_cog = input[0].lower(), False, False
            try:
                search_command = self.bot.get_command(search)
                search_cog = self.bot.cogs[search]
            except:
                pass

            title = "Help · " + str(search)
            if search_cog:
                description, command_list = str(search_cog.__doc__), ''
                for command in search_cog.get_commands():
                    command_list += "__" + \
                        str(command.name)+"__\n"+str(command.help)+'\n'
                embed.add_field(name="Commands :",
                                value=command_list, inline=False)
            elif search_command:
                description, color = '', discord.Color.green()
                embed.add_field(name=str(search_command.name), value="__Aliases__ : `"+"`, `".join(
                    search_command.aliases)+"`\n__Help__ : "+str(search_command.help), inline=False)
            else:
                title, description, color = "Help · Error", "Nothing was found", discord.Color.orange()

        elif len(input) > 1:
            title, description, color = "Help · Error", "Too many arguments", discord.Color.orange()

        embed.title, embed.description, embed.color = title, remind + description, color
        embed.set_footer(text="Requested by : "+str(ctx.message.author.name)+" at " +
                         str(time.strftime('%H:%M:%S')), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.Cog.listener('on_command_error')
    async def get_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(error)
        else:
            await ctx.send("`C0DE 3RR0R` : "+error)


def setup(bot):
    bot.add_cog(Basic(bot))
