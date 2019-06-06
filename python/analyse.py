# -*- coding: utf-8 -*-

import os
from os import listdir
from os.path import isfile, join
from PIL import Image, ImageChops

def analyse():
  # Get files
  downloadPath = "../downloads"
  files = [f for f in listdir(downloadPath) if isfile(join(downloadPath, f)) and f.split(".")[-1] == "png"]
  
  #Create a new datafile
  count = 0
  while True:
    tempfilename = "datafile(%s).txt" % (str(count))
    if isfile(tempfilename):
      count+=1
    else:
      savefile = open(tempfilename, "w+")
      break

  current = 0
  for filename in files:
    print(filename, current)
    current += 1
    image = Image.open(join(downloadPath, filename))
    image = image.convert("RGBA")
    
    width, height = image.size
    mostPopular = None
    mostPopularCount = 0
    colorAddition = [0,0,0]
    count = 0
    pixeldatas = []

    #Average color
    for w in range(width):
      for h in range(height):
        pixeldata = image.getpixel((w,h))
        if pixeldata[3] == 255:
          pixeldatas.append(pixeldata)
          colorAddition = [colorAddition[0] + pixeldata[0], colorAddition[1] + pixeldata[1], colorAddition[2] + pixeldata[2]]
          count += 1

    #Most popular color
    for p in pixeldatas:
      c = pixeldatas.count(p)
      if c > mostPopularCount:
        mostPopular = p
        mostPopularCount = c

    #Write line to file
    colorAddition = [round(colorAddition[0]/count), round(colorAddition[1]/count), round(colorAddition[2]/count)]
    mostPopular = mostPopular[0:3]
    percentPopular = round(mostPopularCount / (width * height), 2)
    percentVisible = round(count / (width * height), 2)
    savefile.write("%s\n" % ("|".join([ 
      filename, ",".join(map(str, mostPopular)), 
      ",".join(map(str, colorAddition)), 
      str(percentPopular),
      str(percentVisible)])
    ))

  savefile.close()

if __name__ == '__main__':
  analyse()









