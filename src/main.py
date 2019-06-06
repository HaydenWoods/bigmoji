# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import urllib
import sys
import os
from math import sqrt
import discord
from discord.ext import commands
import datetime
import aiohttp        
import aiofiles
from PIL import Image, ImageChops
import math

client = commands.Bot(command_prefix='!')

#Discord Events
@client.event
async def on_ready():
  game = discord.Game("games just like Karen smh")
  await client.change_presence(status=discord.Status.online, activity=game)
  print("Logged in as %s (%s)" % (client.user.name, client.user.id))

@client.event
async def on_message(message):
  print(message)
  #Dont accept attachments from itself
  if message.author == client.user:
    return

  await client.process_commands(message)
  

#Discord Commands
@client.command()
async def generate(ctx, width, avw=0.5, pw=0.3, vw=0.2):
  if len(ctx.message.attachments) != 1:
    await ctx.send("Mate... gonna have to give me an image")
    return

  image = ctx.message.attachments[0].url
  width = int(width)
  weight = (avw, pw, vw)

  filename = str(datetime.datetime.utcnow().timestamp())
  try:
    os.mkdir("temp")
  except:
    pass

  imagefile = "temp/%s.%s" % (filename, image.split(".")[-1])  
  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(image) as resp:
        if resp.status == 200:
          f = await aiofiles.open(imagefile, mode='wb')
          await f.write(await resp.read())
          await f.close()
  except Exception as e:
    print(e)
  
  if width < 160:
    msg = makeImage(imagefile, width, True, weight)
    l = msg.split("\n")
    linepermessage = 200//width

    print(l)
    for i in range(int(len(l)/linepermessage)):
      await ctx.send("\n".join(l[i*linepermessage:(i+1)*linepermessage]))
  else:
    await ctx.send("You want me to crash, do yah?")

#Functions
def makeImage(file=None, width=None, ret=False, weight=(0.5,0.3,0.2)):
  if not file:
    file = sys.argv[1]

  if not width:
    width = int(sys.argv[2])

  output = ""
  datafile = open("datafile.txt", "r")

  image = Image.open(file)
  image.thumbnail((width, (float(image.size[1])/image.size[0])*float(width)), Image.BICUBIC)
  image.save("lastthing.png")
  emojis = []

  for line in datafile.readlines():
    s = line.split("|")
    em = s[0].split("~")[0]
    short = ".".join(s[0].split("~")[1].split(".")[0:-1])
    emojis.append({
      "emoji": em,
      "shortcode": short,
      "popular": list(map(int, s[1].split(","))),
      "average": list(map(int, s[2].split(","))),
      "percentPop": float(s[3]),
      "percentVis": float(s[4]),
    })

  for h in range(int((float(image.size[1])/image.size[0])*float(width))):
    for w in range(width):
      pd = image.getpixel((w,h))
      bestemoji = None
      bestemojiscore = math.inf

      if len(pd) > 3 and pd[3] < 255:
        output += "⬜"
      else:
        for emoji in emojis:
          bestemojis = []

          ac = emoji["average"]
          ascore = sqrt(abs(ac[0] - pd[0])**2 + abs(ac[1] - pd[1])**2 + abs(ac[2] - pd[2])**2)
          pc = emoji["popular"]
          pscore = sqrt(abs(pc[0] - pd[0])**2 + abs(pc[1] - pd[1])**2 + abs(pc[2] - pd[2])**2)
          pv = emoji["percentVis"]
          pvscore = 255 * (1 - pv)

          score = (pscore*weight[0]) + (ascore*weight[1]) + (pvscore*weight[2])

          if score < bestemojiscore:
            bestemojiscore = score
            bestemoji = emoji["emoji"]

        #Defaults to white square if there is no emoji
        if bestemoji:
          output += bestemoji
        else:
          output += "⬜"

      if w % width == width - 1:
        output += "\n"

  if not ret:
    print(output)
  else:
    return output


if __name__ == '__main__':
  TOKEN = os.environ["DISCORD_TOKEN"]
  client.run(TOKEN)