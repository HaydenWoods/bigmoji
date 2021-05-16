const Jimp = require("jimp");

const emojis = require("../data/emojis");

const { getColorPercentDiff } = require("./colors");
const { chunkArray } = require("./arrays");
const { sleep } = require("./general");

const WEIGHT_POPULAR_COLOR = 0.75;
const WEIGHT_AVERAGE_COLOR = 0.15;
const WEIGHT_PERCENT_VISIBLE = 0.05;
const WEIGHT_PERCENT_POPULAR = 0.05;

const convertImageToEmojis = async ({ url, options }) => {
  const {
    desiredWidth,
  } = options;

  return await Jimp.read(url).then(image => {
    const beforeWidth = image.getWidth();
    const beforeHeight = image.getHeight();
    const scaleFactor = desiredWidth / beforeWidth;

    image.scale(scaleFactor);

    const scaledWidth = image.getWidth();
    const scaledHeight = image.getHeight();

    const imageEmojis = [];
    const imagePalette = [];

    Array(scaledHeight).fill(0).forEach((_, y) => {
      Array(scaledWidth).fill(0).forEach((_, x) => {
        const color = image.getPixelColor(x,y);
        const colorRGB = Jimp.intToRGBA(color);

        const { bestEmoji } = emojis.reduce((best, emoji) => {
          const {
            popularColor,
            averageColor,
            percentVisible,
            percentPopular,
          } = emoji;

          const {
            bestScore,
          } = best;

          const popularColorDiffPercent = (100 - getColorPercentDiff(popularColor, colorRGB));
          const averageColorDiffPercent = (100 - getColorPercentDiff(averageColor, colorRGB));
          const visiblePercent = percentVisible * 100;
          const popularPercent = percentPopular * 100;

          const score = (((
            (popularColorDiffPercent * WEIGHT_POPULAR_COLOR) + 
            (averageColorDiffPercent * WEIGHT_AVERAGE_COLOR) + 
            (visiblePercent * WEIGHT_PERCENT_VISIBLE) +
            (popularPercent * WEIGHT_PERCENT_POPULAR)
          ) / 400) * 100);

          if (score > bestScore) {
            if (!imagePalette.find(paletteEmoji => paletteEmoji.name === emoji.name)) {
              imagePalette.push(emoji);
            }

            return { 
              bestEmoji: emoji,
              bestScore: score,
            };
          }

          return best;
        }, { bestEmoji: null, bestScore: 0 }); 
        
        imageEmojis.push(bestEmoji);
      }); 
    });

    return {
      imageEmojis,
      imagePalette,
      beforeWidth,
      beforeHeight,
      scaledWidth,
      scaledHeight,
      scaleFactor,
    }
  }).catch(err => {
    return {};
  });
}

const sendEmojis = async ({ imageEmojis, width, channel }) => {
  const lines = chunkArray(imageEmojis, width);
  
  for (let i = 0; i < lines.length; i++) {
    await sleep(1000);

    const emojiLine = lines[i];
    const isLast = lines.length - 1 === i;

    await channel.send(emojiLine.map(emoji => emoji.emoji).join("")).then(async (message) => {
      if (isLast) {
        await message.react("🇩");
        await message.react("🇴");
        await message.react("🇳");
        await message.react("🇪");
      }
    });
  }
}

module.exports = {
  convertImageToEmojis,
  sendEmojis,
}