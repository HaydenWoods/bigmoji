from PIL import Image, ImageChops
from bs4 import BeautifulSoup
import requests
import urllib

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

        print(emojichar, image)

        if image and shortcode:
          urllib.urlretrieve(image, "downloads/%s..%s.%s" % (emojichar, image.split(".")[-1]))
      except:
        pass

if __name__ == '__main__':
  download()
