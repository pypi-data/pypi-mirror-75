"""Run the helpdeskbot"""
from helpdeskbot import HelpDeskBot
from os import environ
from dotenv import load_dotenv


def main():
    load_dotenv()
    if not environ.get('DISCORD_CHANNEL') or not environ.get('DISCORD_TOKEN'):
        raise Exception('Missing DISORD_CHANNEL or DISCORD_TOKEN env var.')
    bot = HelpDeskBot(environ['DISCORD_CHANNEL'], environ['DISCORD_TOKEN'])
    bot.run()


if __name__ == '__main__':  # If invoked with `python -m`
    main()
