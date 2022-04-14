#bot.py
import os
import pickle
import ffmpeg
import asyncio
import discord
from discord.ext import commands
from numpy.random import choice
TOKEN = "OTYzMzMxNTY2NjYxMTUyODM4.YlUibw.deuoOvf3QjHwxhpB82rCD73hWuE"
bot = commands.Bot(command_prefix='$', intents = discord.Intents().all())

db = {"Bonk Bot": 9000}

try:
  file_to_read = open("data.pkl", "rb")
  db = pickle.load(file_to_read)
except Exception:
    pass

bonkList = ['bonk.mp3','bonk_s1.mp3','bonk_s2.mp3','bonk_s3.mp3']

@bot.event
async def on_ready():
    print('Bonk Bot has connected to Discord!')

# Bonk somebody
@bot.command(name='bonk', help="Mention somebody to bonk them!")
async def bonk(ctx):
  # bot not actively in call and author is in vc
  source = await discord.FFmpegOpusAudio.from_probe("bonk_sounds/"+choice(
  bonkList, p=[0.97, 0.01, 0.01, 0.01]))
  if ctx.voice_client is None and ctx.author.voice is not None:
    voice_channel = ctx.author.voice.channel
    if voice_channel != None:
      vc = await voice_channel.connect()
      vc.play(source)
  elif ctx.voice_client is not None and ctx.author.voice is not None:
    ctx.voice_client.play(source)
  else:
    await ctx.send("**B O N K ! U R NOT IN A VC**")
  if ctx.message.mentions:
    print(ctx.message.mentions)
    for user_mentioned in ctx.message.mentions:
      print(user_mentioned.name)
      if user_mentioned.name not in db.keys():
        add_user(user_mentioned.name)
        await ctx.send("{} has been bonked {} times!".format(user_mentioned.mention,db[user_mentioned.name]))
      else:
        update_bonk_count(user_mentioned.name)
        await ctx.send("{} has been bonked {} times!".format(user_mentioned.mention,db[user_mentioned.name]))
        
# Get bonk count for user
@bot.command(name='bonkcount', help ='Mention to get bonk count')
async def get_bonk_count(ctx):
  for user_mentioned in ctx.message.mentions:
    if user_mentioned.name in db.keys():
      await ctx.send("{} has been bonked {} times!".format(user_mentioned.mention,db[user_mentioned.name]))
    else:
      await ctx.send("This user hasn't been bonked.")
      print(user_mentioned.name, db[user_mentioned.name])

# Remove 1 bonk from count
@bot.command(name='removebonk', help= 'Mention to remove one bonk')
async def remove_bonk(ctx):
  if ctx.message.author.guild_permissions.administrator:
    for user_mentioned in ctx.message.mentions:
      if db[user_mentioned.name] < 1:
        await ctx.send("Can't be unbonked.")
      else:
        db[user_mentioned.name] -= 1
        save_db(db)
        print(user_mentioned.name, db[user_mentioned.name])

  else:
    await ctx.send("You can't unbonk.")

# Idle Timer
@bot.event
async def on_voice_state_update(member, before, after):
    if not member.id == bot.user.id:
        return
    elif before.channel is None:
        voice = after.channel.guild.voice_client
        time = 0
        while True:
            await asyncio.sleep(1)
            time = time + 1
            print(time)
            if voice.is_playing() and not voice.is_paused():
                time = 0
            if time == 20:
                await voice.disconnect()
            if not voice.is_connected():
                break

# bonk statistics
def add_user(user):
  db[user] = 1
  save_db(db)

def update_bonk_count(user):
  db[user] += 1
  save_db(db)

def save_db(db):
  a_file = open("data.pkl", "wb")
  pickle.dump(db, a_file)
  a_file.close()
  print("Saved Dictionary")

  
bot.run(TOKEN)
