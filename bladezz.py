#from fs import open_fs
import discord
import json
with open('config.json') as f:
    config = json.load(f)
prefix = config['prefix']
token = config['token']

# command handler class

class CommandHandler:

    # constructor
    def __init__(self, client):
        self.client = client
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def command_handler(self, message):
        for command in self.commands:
            if message.content.startswith(command['trigger']):
                args = message.content.split(' ')
                if args[0] == command['trigger']:
                    args.pop(0)
                    if command['args_num'] == 0:
                        return self.client.send_message(message.channel,str(command['function'](message, self.client, args)))
                        break
                    else:
                        if len(args) >= command['args_num']:
                            return self.client.send_message(message.channel,str(command['function'](message, self.client, args)))
                            break
                        else:
                            return self.client.send_message(message.channel, 'command "{}" requires {} argument(s) "{}"'.format(command['trigger'], command['args_num'], ', '.join(command['args_name'])))
                            break
                else:
                    break


client = discord.Client()

# bot is ready
@client.event
async def on_ready():
    try:
        # print bot information
        print(config)
        print(client.user.name)
        print(client.user.id)
        print('Discord.py Version: {}'.format(discord.__version__))

        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for messages that start with a dash (-)"))

    except Exception as e:
        print(e)

# on new message
@client.event
async def on_message(message):
    if message.author == client.user:
        return    

    #put what's being sent into the terminal - for now - to help with debugging
    print('Message from {0.author}: {0.content}'.format(message))

    response = []

        # if the message starts with the prefix, try and do actual stuff with it!
    if message.content.startswith(prefix):
        # get rid of the prefix, then split all the words into individual commands. we'll use the first one as the Real Command, and the rest as arguments
        # message.content is the whole message
        # len(prefix) is the length of the prefix - almost always one character, but leaves it open to multi-char prefixes
        # the braces and colon are substring. [1:] means start at the second character and go to the end
        # split returns an array of all the words, with spaces removed
        args = message.content[len(prefix):].split()
        response.append('Here are the words that I saw:')
        for a in args:
            print(a)
            response.append(a)
        command = args.pop(0)
        
        response.append('Here is the command that I will follow:')
        response.append('**' +command + '**')
        
        if len(args):
            response.append('I found ' + str(len(args)) + ' argument(s):')
            for a in args:
                response.append('*'+a+'*')
        else:
            response.append('I didn\'t see any arguments.')

        await message.channel.send('\n'.join(response))


# start bot
client.run(token)
"""
class MyClient(discord.Client):
    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for messages that start with a dash (-)"))
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        reactions = []
        reactMessage = []
        response = []
        
        # don't let the bot respond to itself
        if message.author == client.user:
            return

        # print('trying to find {0.user.mention}'.format(message))
        
        # if the message starts with the prefix, try and do actual stuff with it!
        if message.content.startswith(prefix):
            # get rid of the prefix, then split all the words into individual commands. we'll use the first one as the Real Command, and the rest as arguments
            # message.content is the whole message
            # len(prefix) is the length of the prefix - almost always one character, but leaves it open to multi-char prefixes
            # the braces and colon are substring. [1:] means start at the second character and go to the end
            # split returns an array of all the words, with spaces removed
            args = message.content[len(prefix):].split()
            response.append('Here are the words that I saw:')
            for a in args:
                print(a)
                response.append(a)
            command = args.pop(0)
            
            response.append('Here is the command that I will follow:')
            response.append('**' +command + '**')
            
            if len(args):
                response.append('I found ' + str(len(args)) + ' argument(s):')
                for a in args:
                    response.append('*'+a+'*')
            else:
                response.append('I didn\'t see any arguments.')

            await message.channel.send('\n'.join(response))

        if message.content.startswith('-hello'):
            msg = 'Hello {0.author.mention}'.format(message)
            await message.channel.send(msg)

        if message.content.startswith('-blast'):
            msg = '{0.author.mention} WANTS TO PING @everyone'.format(message)
            await message.channel.send(msg)


        # otherwise we're in REACTION territory
        if client.user.mention in message.content:
            await message.channel.send('Hey that\'s me!')

        if 'dang' in message.content:
            reactions.append('🇫')
        
        if 'haha' in message.content:
            reactions.append('😊')
        
        if message.content == 'f':
            reactions.append('🇫')

        for r in reactions:
            await message.add_reaction(r)

client = MyClient()
client.run(token)
"""