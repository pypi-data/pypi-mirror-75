from setuptools import setup


setup(
    name='helpdeskbot',
    version='2.1.0',
    description='Discord utility bot for DevDungeon.com',
    url='https://github.com/DevDungeon/HelpDeskBot',
    author='John Leon',
    author_email='nanodano@devdungeon.com',
    license='GPL-3.0',
    packages=['helpdeskbot'],
    entry_points={
        'console_scripts': [
            'helpdeskbot = helpdeskbot.__main__:main',
        ],
    },
    zip_safe=False,
    python_requires='>=3.7',
    install_requires=[
        'discord.py==1.3.3',
        'aiohttp==3.6.2',
        'python-dotenv==0.13.0',
    ]
)
