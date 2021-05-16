const fs = require("fs");

const file = fs.readFileSync(`${__dirname}/emojis.txt`);
const content = file.toString();
const lines = content.split("\n");

const emojis = lines.map(line => {
  const emoji = line.split("~")[0];
  let [fileName, popularColor, averageColor, percentPopular, percentVisible] = (line.split("~")[1] || "").split("|");

  const name = fileName.split(".")[0];

  if (!name) return;

  return {
    name,
    fileName,
    emoji,
    popularColor: {
      r: parseInt(popularColor.split(",")[0]),
      g: parseInt(popularColor.split(",")[1]),
      b: parseInt(popularColor.split(",")[2]),
    },
    averageColor: {
      r: parseInt(averageColor.split(",")[0]),
      g: parseInt(averageColor.split(",")[1]),
      b: parseInt(averageColor.split(",")[2]),
    },
    percentPopular: parseFloat(percentPopular),
    percentVisible: parseFloat(percentVisible),
  }
});

console.dir(emojis, { maxArrayLength: null })