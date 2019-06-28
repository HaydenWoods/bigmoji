# bigmoji

## Usage
### Command
```
:b:generate [WIDTH] [AVW] [PW] [VW]
```

1. Upload an image
2. In the comment add the command with chosen parameters
3. Send the image

### EXPLANATION
You must always supply the width for the emoji image.
**Width:** The width that the image will be in emojis (MAX: 80) 

When figuring out what emoji should be used for each pixel three parameters are taken into account:\
**Average Colour (AVW):** The average colour that is present in the emoji\
**Popular Colour (PW):** The most popular colour that is present in the emoji\
**Visible Pixels (VW):** The percentage amount of pixels that are not transparent in the emoji

You can assign a weight for each of these parameters(they must add up to 1.0 exactly). The default is:\
**AVW:** 0.5\
**PW:** 0.3\
**VW:** 0.2
This means that the Average Colour has a higher effect on what emoji is chosen than the Percent of Visible Pixels in the emoji.

## Installation
https://discordapp.com/oauth2/authorize?client_id=585850492882780164&scope=bot&permissions=75776
