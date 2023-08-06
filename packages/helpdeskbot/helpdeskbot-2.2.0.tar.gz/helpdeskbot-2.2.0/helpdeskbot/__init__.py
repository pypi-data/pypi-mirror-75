import logging
import random
import aiohttp
from urllib import parse
import discord
from discord.ext.commands import Bot


class HelpDeskBot:

    BOT_PREFIX = ("?", "!")

    def __init__(self, channel_name, token):
        logging.basicConfig(level=logging.INFO)
        logging.info("[*] Initializing bot...")
        self.token = token
        self.designated_channel_name = channel_name
        self.client = Bot(command_prefix=self.BOT_PREFIX)
        self.setup()

    def run(self):
        logging.info("[*] Running helpdeskbot...")
        self.client.run(self.token)

    def setup(self):

        @self.client.event
        async def on_ready():
            logging.info("[+] Connected as " + self.client.user.name)
            logging.info("[+] Listening for messages and in channel #" + self.designated_channel_name)
            game = discord.Game("Help Desk")
            await self.client.change_presence(status=discord.Status.online, activity=game)

        @self.client.event
        async def on_message(message):
            # Ignore messages by bots (including self)
            if message.author.bot:
                return

            # Only return help in designated channel
            if message.content.startswith(self.BOT_PREFIX):
                msg = message.content.strip("".join(list(self.BOT_PREFIX)))
                if msg.startswith("help"):
                    if message.channel.name != self.designated_channel_name:
                        return

            # Pass on to rest of the client commands
            if message.content.startswith(self.BOT_PREFIX):
                await self.client.process_commands(message)

        @self.client.command(description="Checks the current Bitcoin price in US Dollars from Coinbase.",
                             brief="Get current Bitcoin price",
                             aliases=['btc'],
                             pass_context=True)
        async def bitcoin(context):
            # Only respond to the channel designated and private messages.
            if context.message.channel.name != self.designated_channel_name:
                return

            url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
            async with aiohttp.ClientSession() as session:
                raw_response = await session.get(url)
                response = await raw_response.json(content_type='application/javascript')
                await context.message.channel.send("Bitcoin price is: $" + response['bpi']['USD']['rate'])

        @self.client.command(name='8ball',
                             description="Answers a yes/no question.",
                             brief="Answers from the beyond.",
                             aliases=['eight_ball', 'eightball', '8-ball'],
                             pass_context=True)
        async def eight_ball(context):
            # Only respond to the channel designated and private messages.
            if context.message.channel.name != self.designated_channel_name:
                return
            possible_responses = [
                'That is a resounding no',
                'It is not looking likely',
                'Too hard to tell',
                'It is quite possible',
                'Definitely',
            ]

            await context.message.channel.send(random.choice(possible_responses) + ", " + context.message.author.mention)

        @self.client.command(name='lmgtfy',
                             description="Let me Google that for you",
                             brief="Google help",
                             aliases=['letmegooglethatforyou', 'trygoogle', 'googlefirst', 'google', 'search'],
                             pass_context=True)
        async def lmgtfy(context):
            search_term = context.message.content.strip("".join(list(self.BOT_PREFIX))).replace("lmgtfy", "").strip()
            if search_term == "":
                return
            url = 'https://lmgtfy.com?' + parse.urlencode({"q": search_term})
            response = "Here is the link you requested: " + url
            await context.message.channel.send(response)

        @self.client.command(name='gethelp',
                             description='Print information about 1-on-1 coaching with NanoDano',
                             brief='Coaching details',
                             aliases=['1on1', 'tutoring', 'coaching', 'personal-help'],
                             pass_context=True)
        async def coaching(context):
            message = 'Help is offered for free by NanoDano when time permits, ' \
                      'otherwise other friendly server members might help answer questions. ' \
                      'If you want private 1-on-1 screenshare, schedule time at https://www.codementor.io/nanodano'
            await context.message.channel.send(message)

        @self.client.command(name='busy',
                             description='Busy message for NanoDano that links to tutoring scheduling',
                             brief='Busy message for NanoDano',
                             aliases=['busyatm', 'in-a-meeting', 'working', 'meeting'],
                             pass_context=True)
        async def coaching(context):
            message = 'AutoResponder for NanoDano: Sorry, I am busy or in a meeting right now. I get a lot of requests and I will respond when I have time, or ' \
                      'you might get help from other friendly server members. If you would like schedule a 1-on-1 screen share session with me, go to https://www.codementor.io/nanodano'
            await context.message.channel.send(message)

        @self.client.command(name='questions',
                             description='Provides tips on asking good questions',
                             brief='Tips on asking questions',
                             aliases=['asking-for-help'],
                             pass_context=True)
        async def questions(context):
            message = """```md
# Tips on asking questions:

## DO
- Clearly explain your problem.
- Provide code and error messages.
- Search the internet before you ask.
- Explain what you've already tried.

## DO NOT
- Demand help.
- Ask questions like "Is anyone here?" or "Does anyone know Java?" Just ask your question.
- Ask XY questions: http://xyproblem.info/```"""
            await context.message.channel.send(message)


        @self.client.command(name='cathy',
                             description='Provides documentation links for Cathy chat bot',
                             brief='Cathy documentation links',
                             aliases=['chattycathy', 'cathydocs', 'cathy-docs'],
                             pass_context=True)
        async def cathy(context):
            message = 'Cathy chat bot documentation: https://cathy-docs.readthedocs.io/en/latest/'
            await context.message.channel.send(message)

        @self.client.command(name='cannot_find_module',
                             description='Link to tutorial on Node.js error cannot find module',
                             brief='JS "Cannot find module" error link',
                             aliases=['js_cant_find_module', 'js_wrong_file'],
                             pass_context=True)
        async def cannot_find_module(context):
            message = 'How to solve "Error: Cannot find module \'*.js\'" with Node.js https://www.devdungeon.com/content/how-solve-error-cannot-find-module-js-nodejs'
            await context.message.channel.send(message)

        @self.client.command(name='forreach_not_a_function',
                             description='Troubleshoot common Discord.js error',
                             brief='Fix common Discord.js error',
                             pass_context=True,
                             aliases=['foreach'])
        async def foreach_not_a_function(context):
            message = """If you are working through the DevDungeon Discord.js bot tutorial and you get the error message:
`UnhandledPromiseRejectionWarning: TypeError: client.guilds.forEach is not a function`

Then you need to change the code to include the cache property like this: client.guilds.cache.forEach

This is due to the API changing in newer versions of [Discord.js](https://discord.js.org/#/docs/main/stable/general/welcome)."""
            await context.message.channel.send(message)

        @self.client.command(name='devnix',
                             description='Link to DevNix (a Fedora remix) information page',
                             brief='Information about DevNix Linux distribution',
                             pass_context=True)
        async def devnix(context):
            message = 'DevNix is a Linux distribution built by NanoDano. Learn more and download from https://www.devdungeon.com/devnix or view source at https://github.com/DevDungeon/DevNix/tree/f30/devnix'
            await context.message.channel.send(message)
