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
import asyncio
from PIL import Image, ImageChops
import math

#Constant Values
MAXCHARS = 198
DEFAULTEMOJI = "⬜"
PREFIX = "🅱"
WIDTH = 50
AVERAGEWEIGHT = 0.5
POPULARWEIGHT = 0.3
VISIBLEWEIGHT = 0.2

MAXWIDTH = int(os.environ["MAX_WIDTH"])
TOKEN = os.environ["DISCORD_TOKEN"]

activeChannels = []
client = commands.Bot(command_prefix=PREFIX)
client.remove_command("help")

#Discord Events
@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.dnd)
  print("Logged in as %s (%s)" % (client.user.name, client.user.id))

@client.event
async def on_message(message):
  #Dont accept attachments from itself
  if message.author == client.user:
    return

  #Keep at end
  await client.process_commands(message)

#Discord Commands
@client.command()
async def help(ctx):
  err = ""
  if ctx.message.channel in activeChannels:
    err = "No, I don't think I will."
  if err != "":
    await ctx.send(err)
    return

  await ctx.send("""
  __**BIGMOJI BOT HELP**__

  **GENERAL**
  1. Upload an image
  2. In the comment add %sgenerate <WIDTH>
      a. Max width is 80
      b. Usually 30 - 70 looks good (50 is the default)
  3. Send the image

  **OPTIONAL**
  %sgenerate *<WIDTH> <AVW> <PW> <VW>*

  **EXPLANATION**
  **Width (WIDTH): Is the width in emojis that the image will be converted into. **
  When figuring out what emoji should be used for each pixel three parameters are taken into account:
  **Average Colour (AVW):** The average colour that is present in the emoji
  **Popular Colour (PW):** The most popular colour that is present in the emoji
  **Visible Pixels (VW):** The percentage amount of pixels that are not transparent in the emoji

  You can assign a weight for each of these parameters(they must add up to 1.0 exactly). The default is:
  **AVW:** 0.5
  **PW:** 0.3
  **VW:** 0.2
  This means that the Average Colour has a higher effect on what emoji is chosen than the Percent of Visible Pixels in the emoji.
  """ % (PREFIX, PREFIX))

@client.command(pass_context = True)
async def generate(ctx, w=WIDTH, avw=AVERAGEWEIGHT, pw=POPULARWEIGHT, vw=VISIBLEWEIGHT):
  width = int(w)

  #Error checking
  err = ""
  if ctx.message.channel in activeChannels:
    err = "No, I don't think I will."
  if width > 80:
    err = "You want me to crash, do yah?"
  if len(ctx.message.attachments) != 1:
    err = "Mate... gonna have to give me an image"
  if (float(avw) + float(pw) + float(vw)) != 1.0:
    err = "Can you add to 1. Go back to year 2 silly man"
  if err != "":
    sendError(err)
    return
  
  #Add it to the active channels
  activeChannels.append(ctx.message.channel)

  image = ctx.message.attachments[0].url
  weight = (avw, pw, vw)
  filename = str(datetime.datetime.utcnow().timestamp())

  try:
    if not os.path.isdir("temp"):
      os.mkdir("temp")
  except:
    pass

  try:
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
      
    await ctx.message.delete()

    await ctx.send("Gimme two secs...")
    msg = makeImage(imagefile, width, True, weight)
    lines = msg.split("\n")
    linepermessage = MAXCHARS//width
    remainingLines = len(lines) - (int(len(lines)/linepermessage) * linepermessage)

    #Send the majority
    for i in range(int(len(lines)/linepermessage)):
      await ctx.send("\n".join(lines[i*linepermessage:(i+1)*linepermessage]))
    #Send the remaining
    if (remainingLines > 0):
      await ctx.send("\n".join(lines[len(lines)-remainingLines:len(lines)]))
  except Exception as e:
    print(e)
    sendError("Something went wrong, big hmmm.")

  #Remove from active channels
  activeChannels.remove(ctx.message.channel)

#Functions
def makeImage(file=None, width=None, ret=False, weight=None):
  err = ""
  if not file:
    err = "No file"
  if not width:
    err = "No width"
  if not weight:
    err = "No weights"
  if err != "":
    sendError(err)
    return

  datafile = open("datafile.txt", "r")

  image = Image.open(file)
  image = image.convert('RGB')

  #Actual width / Desired width
  scaleFactor = image.size[0] / width
  height = math.floor(image.size[1] / scaleFactor)
  
  image.thumbnail((width, height), Image.BICUBIC)
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

  output = ""
  for h in range(height):
    for w in range(width):
      pd = image.getpixel((w,h))
      bestemoji = None
      bestemojiscore = math.inf

      #If pixel data is not useable give default emoji
      if len(pd) > 3 and pd[3] < 255:
        output += DEFAULTEMOJI
      else:
        for emoji in emojis:
          #Calc score based on 3 factors with different weighting
          ac = emoji["average"]
          ascore = sqrt(abs(ac[0] - pd[0])**2 + abs(ac[1] - pd[1])**2 + abs(ac[2] - pd[2])**2)
          pc = emoji["popular"]
          pscore = sqrt(abs(pc[0] - pd[0])**2 + abs(pc[1] - pd[1])**2 + abs(pc[2] - pd[2])**2)
          pv = emoji["percentVis"]
          pvscore = 255 * (1 - pv)

          score = (pscore*weight[0]) + (ascore*weight[1]) + (pvscore*weight[2])

          #Compare scores and reset variable
          if score < bestemojiscore:
            bestemojiscore = score
            bestemoji = emoji["emoji"]

        #Defaults to white square if there is no emoji
        if bestemoji != None:
          output += bestemoji
        else:
          output += DEFAULTEMOJI

        if w % width == width - 1:
          output += "\n"

  return output

async def sendError(err):
  errorMessage = await ctx.send(err)
  await errorMessage.delete(delay=10.0)


if __name__ == '__main__':
  client.run(TOKEN)