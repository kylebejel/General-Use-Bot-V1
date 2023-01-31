import discord
import Paginator
import psycopg2
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def epic(ctx):
    conn = psycopg2.connect(
    database="", user='', password='', host='127.0.0.1', port= '5432'
    )
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM epic WHERE end_date >= CURRENT_DATE')

    embed_ls = []
    for row in cursor:
        embed = discord.Embed(title=row[2], url=row[3])
        embed.add_field(name="Free From:", value=row[4], inline=False)
        embed.set_thumbnail(url=row[5])
        embed_ls.append(embed)
    cursor.close()
    conn.close()
    await Paginator.Simple().start(ctx, pages=embed_ls)

bot.run('')