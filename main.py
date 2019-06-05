# -*- coding: utf-8 -*-

from PIL import Image, ImageChops
from bs4 import BeautifulSoup
import requests
import urllib
import sys
import os
from os import listdir
from os.path import isfile, join
from math import sqrt
import discord
import datetime
import aiohttp        
import aiofiles

def download():
  url = "https://emojipedia.org"
  res = requests.get(url)
  soup = BeautifulSoup(res.text, 'html.parser')
  nav = soup.find("ul")
  nav_items = nav.find_all("li")

  pages = []

  for page in nav_items:
    pages.append(page.find("a")['href'])

  for page in pages:
    res = requests.get(url + page)
    soup = BeautifulSoup(res.text, 'html.parser')
    emojislist = soup.find("ul", class_="emoji-list")
    emojis = emojislist.find_all("li")

    for emoji in emojis:
      emojipage = emoji.find("a")['href']
      res = requests.get(url + emojipage)
      soup = BeautifulSoup(res.text, 'html.parser')

      try:
        shortcodesection = soup.find("ul", class_="shortcodes")
        shortcode = None

        if shortcodesection:
          shortcode = shortcodesection.find("li").text.replace(":", "")

        emojichar = soup.find("article").find("span", class_="emoji").text

        images = soup.find("section", class_="vendor-list").find_all("img")
        image = None

        for img in images:
          if "twemoji" in img['alt'].lower():
            image = img['src']
            break

        print(emojichar)
        if image and shortcode:
          urllib.urlretrieve(image, "downloads/%s~%s.%s" % (emojichar, shortcode, image.split(".")[-1]))
      except:
        pass

def anaylse():
  # Get files
  downloadPath = "downloads"

  files = [f for f in listdir(downloadPath) if isfile(join(downloadPath, f)) and f.split(".")[-1] == "png"]
  savefile = open("datafile.txt", "w+")
  current = 0

  for filename in files:
    print(filename, current)
    current += 1
    image = Image.open(join(downloadPath, filename))
    image.thumbnail((60,60))
    image = image.convert("RGBA")
    
    width, height = image.size
    mostPopular = None
    mostPopularCount = 0
    colorAddition = [0,0,0]
    count = 0
    pixeldatas = []

    for w in range(width):
      for h in range(height):
        pixeldata = image.getpixel((w,h))
        if pixeldata[3] == 255:
          pixeldatas.append(pixeldata)
          colorAddition = [colorAddition[0] + pixeldata[0], colorAddition[1] + pixeldata[1], colorAddition[2] + pixeldata[2]]
          count += 1

    for p in pixeldatas:
      c = pixeldatas.count(p)
      if c > mostPopularCount:
        mostPopular = p
        mostPopularCount = c


    colorAddition = [colorAddition[0]/count, colorAddition[1]/count, colorAddition[2]/count]
    mostPopular = mostPopular[0:3]
    savefile.write("%s\n" % ("|".join([filename, ",".join(map(str, mostPopular)), ",".join(map(str, colorAddition)), str(mostPopularCount)])))

  savefile.close()

def generate(file=None, width=None, ret=False, weight=0.0):
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
      "popcount": int(s[3]),
      "average": list(map(int, s[2].split(","))),
    })

  for h in range(int((float(image.size[1])/image.size[0])*float(width))):
    for w in range(width):
      pd = image.getpixel((w,h))
      bestemoji = None
      bestemojiscore = 100000

      if len(pd) > 3 and pd[3] < 255:
        output += "⬜"
      else:
        for emoji in emojis:
          bestemojis = []

          ac = emoji["average"]
          ascore = sqrt(abs(ac[0] - pd[0])**2 + abs(ac[1] - pd[1])**2 + abs(ac[2] - pd[2])**2)
          pc = emoji["popular"]
          pscore = sqrt(abs(pc[0] - pd[0])**2 + abs(pc[1] - pd[1])**2 + abs(pc[2] - pd[2])**2)

          score = pscore*weight + ascore*(1-weight)

          if score < bestemojiscore:
            bestemojiscore = score
            bestemoji = emoji["emoji"]
          # elif score == bestemojiscore:
          #   bestemojis.append(emoji)

          # bestemojisscore = 0
          # for be in bestemojis:
          #   if be["popcount"] > bestemojisscore:
          #     bestemojisscore = be["popcount"]
          #     bestemoji = be["emoji"]

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

def main():
  TOKEN = os.environ["DISCORD_TOKEN"]

  client = discord.Client()
  previousimage = None

  @client.event
  async def on_message(message):
    # we do not want the bot to reply to itself
    print(message.attachments)
    if len(message.attachments) > 0:
      previousimage = message.attachments[0]["url"]

    if message.author == client.user:
      return

    if message.content.startswith('!generate'):
      try:
        filename = str(datetime.datetime.utcnow().timestamp())
        imagefile = "temp/%s.%s" % (filename, previousimage.split(".")[-1])
        try:
          async with aiohttp.ClientSession() as session:
            async with session.get(previousimage) as resp:
              if resp.status == 200:
                f = await aiofiles.open(imagefile, mode='wb')
                await f.write(await resp.read())
                await f.close()
        except Exception as e:
          print(e)

        width = int(message.content.split(" ")[1])
        
        if width < 80:
          weight = float(message.content.split(" ")[2])
          msg = generate(imagefile, width, True, weight)
          l = msg.split("\n")
          linepermessage = 200//width
          print(l)
          for i in range(int(len(l)/linepermessage)):
            await client.send_message(message.channel, "\n".join(l[i*linepermessage:(i+1)*linepermessage]))
        else:
          await client.send_message(message.channel, "You want me to crash, do yah?")
      except Exception as e:
        print(e)
        await client.send_message(message.channel, "Bruh really thought he could bait me... smh")

  @client.event
  async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

  client.run(TOKEN)

if __name__ == '__main__':
  main()
