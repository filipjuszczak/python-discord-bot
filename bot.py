import discord
from discord.ext import commands
from random import choice


INTENTS = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
BOT = commands.Bot(command_prefix='!', intents=INTENTS)

BOT.remove_command('help')

PREFIX = BOT.command_prefix

COMMANDS = {
    f'{PREFIX}ping': "Sends bot's latency",
    f'{PREFIX}join': "Bot joins voice channel that user is in at the time",
    f'{PREFIX}leave': "Bot leaves voice channel",
    f'{PREFIX}play *link/song title*': "Bot plays specified song in voice channel",
    f'{PREFIX}queue': "Displays the current song queue",
    f'{PREFIX}remove *index*': "Removes a song at the specified index",
    f'{PREFIX}loop': "Loops current song",
    f'{PREFIX}loop-queue': "Loops current queue"
}


def read_token(file_name):
    try:
        with open(file_name, 'r') as token_file:
            return token_file.readlines()[0].strip()

    except FileNotFoundError:
        print('File {0} was not found!'.format(file_name))

        return None


TOKEN = read_token('token.txt')

if TOKEN is not None:

    GREETINGS = (
        'Hi, {0}!',
        'Hello, {0}!',
        'Hey, {0}!'
    )


    @BOT.event
    async def on_ready():
        print('Logged in as {0}!'.format(BOT.user))
    

    @BOT.event
    async def on_member_join(member):
        channel = BOT.get_channel(848227405952843846)

        await channel.send('👋 **{0}** just joined the server! 😃'.format(member.name))
    

    @BOT.event
    async def on_member_remove(member):
        channel = BOT.get_channel(848227405952843846)

        await channel.send('👋 **{0}** just left the server... 😔'.format(member.name))


    @BOT.listen('on_message')
    async def message_listener(message):
        if message.author == BOT.user:
            return
        
        if message.content.lower().startswith(('hi', 'hello', 'hey')):
            await message.channel.send(choice(GREETINGS).format(message.author.mention))
    

    @BOT.command()
    async def ping(ctx):
        await ctx.send('Pong! 🏓\n**Latency:** {0}ms'.format(round(BOT.latency, 1)))


    @BOT.command()
    @commands.has_any_role('Administrator', 'Moderator')
    async def kick(ctx, member: discord.Member, *, reason=None):
        if member == ctx.message.author:
            await ctx.send('⛔️ You cannot kick yourself, dummy!')
        
        elif member == BOT.user:
            await ctx.send('⛔️ I cannot kick myself... 😔')
        
        else:
            await member.kick(reason=reason)

            if reason:
                await ctx.send('✅ **{0}** has been kicked!\n**Reason:** {1}.'.format(member.mention, reason))
            
            else:
                await ctx.send('✅ **{0}** has been kicked!\n**Reason:** no reason provided.'.format(member.mention))


    @BOT.command()
    @commands.has_any_role('Administrator', 'Moderator')
    async def ban(ctx, member: discord.Member, *, reason=None):
            if member == ctx.message.author:
                await ctx.send('⛔️ You cannot ban yourself, dummy!')
            
            elif member == BOT.user:
                await ctx.send('⛔️ I cannot ban myself... 😔')
            
            else:
                await member.ban(reason=reason)

                if reason:
                    await ctx.send('✅ **{0}** has been banned!\n**Reason:** {1}.'.format(member.mention, reason))
                    
                else:
                    await ctx.send('✅ **{0}** has been banned!\n**Reason:** no reason provided.'.format(member.mention))


    @BOT.command()
    @commands.has_any_role('Administrator', 'Moderator')
    async def unban(ctx, *, member_id: int):
        banned_users = await ctx.guild.bans()
        user_to_unban = await BOT.fetch_user(member_id)
        found = False
        
        for banned_user in banned_users:
            user = banned_user.user

            if user.id == member_id:
                found = True
                break
        
        if found:
            await ctx.guild.unban(user_to_unban)
            await ctx.send('✅ {0} has been un-banned!'.format(user_to_unban.mention))
        
        else:
            await ctx.send('⛔️ {0} is not banned! No action performed.'.format(user_to_unban.mention))


    @BOT.command()
    @commands.has_any_role('Administrator', 'Moderator')
    async def bans(ctx):
        ban_entries = await ctx.guild.bans()

        if len(ban_entries) == 0:
            await ctx.send('⛔️ Currently there are no bans on this server!')

        else:
            response = '✅ Currently there are {0} bans on this server:\n\n-----'.format(len(ban_entries))
            
            for id, ban_entry in enumerate(ban_entries):
                user_name = ban_entry.user.name
                user_discriminator = ban_entry.user.discriminator
                user_id = ban_entry.user.id
                reason = ban_entry.reason

                response += '\n**Ban ID:** {0}\n**User:** {1}\n**User ID:** {2}\n**Reason: **{3}\n-----\n'.format(id + 1, f'{user_name}#{user_discriminator}', user_id, reason)

            await ctx.send(response)
    

    @BOT.command()
    async def avatar(ctx, member: discord.Member=None):
        if member:
            avatar = member.avatar_url
            response = "{0}, here is {1}'s avatar you are looking for!\n{2}".format(ctx.message.author.mention, member, avatar)

            await ctx.send(response)
        
        else:
            avatar = ctx.message.author.avatar_url
            response = '{0}, here is your avatar!\n{1}'.format(ctx.message.author.mention, avatar)

            await ctx.send(response)


    @BOT.command()
    @commands.has_any_role('Administrator', 'Moderator')
    async def clear(ctx, number_of_messages: int):
        if number_of_messages > 100:
            await ctx.send('❗️ Due to security reasons, I cannot delete more than 100 messages at once. Pick a lower number, then recall the command.')
        
        else:
            await ctx.channel.purge(limit=number_of_messages)
            await ctx.send('✅ Messages have been deleted!')
    

    @BOT.command()
    async def help(ctx):
        RESPONSE = "✅ A list of available commands:\n\n"
        index = 0

        for command, description in COMMANDS.items():
            if index != len(COMMANDS):
                RESPONSE += "{0}: {1} - {2},\n".format(index+1, command, description)
            else:
                RESPONSE += "{0}: {1} - {2}".format(index+1, command, description)
            
            index += 1
        
        await ctx.send(RESPONSE)
    

    @clear.error
    async def clear_error(ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send('⛔️ {0}, you do not have permissions to delete messages!'.format(ctx.message.author.mention))
        
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('❗️ {0}, please specify an amount of messages to delete.'.format(ctx.message.author.mention))
    

    @kick.error
    async def kick_error(ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send('⛔️ {0}, you do not have permissions to kick members!'.format(ctx.message.author.mention))
        
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('❗️ {0}, please specify a member to kick.'.format(ctx.message.author.mention))
    

    @ban.error
    async def ban_error(ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send('⛔️ {0}, you do not have permissions to ban members!'.format(ctx.message.author.mention))
        
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('❗️ {0}, please specify a member to ban.'.format(ctx.message.author.mention))
    

    @bans.error
    async def bans_error(ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send('⛔️ {0}, you do not have permissions to view banned members list!'.format(ctx.message.author.mention))


    BOT.run(TOKEN)

else:
    print('BOT not started!')
