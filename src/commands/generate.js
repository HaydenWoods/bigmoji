const Discord = require("discord.js");

const BigMojiLog = require("../helpers/log");

const { convertImageToEmojis, sendEmojis } = require("../helpers/generate")

const DEFAULT_DESIRED_WIDTH = 50;

module.exports = {
	name: "generate",
  aliases: ["", "g", "gen", "generate"],
	description: "Generates a BigMoji based on the attached image of the message.",
  execute: async (message, messageArgs, messageFlags) => {
    const isDebug = messageFlags.includes("-debug") || messageFlags.includes("-d");
    const isMock = messageFlags.includes("-mock") || messageFlags.includes("-m");

    const desiredWidth = messageArgs[0] || DEFAULT_DESIRED_WIDTH;
    const messageImage = message.attachments.array()[0];

    if (!messageImage) {
      return message.channel.send("Gonna have to send an image with that...");
    }

    BigMojiLog.info("Generating BigMoji");
    message.channel.send("Gimme two secs...");

    const { 
      imageEmojis, 
      imagePalette,
      beforeWidth,
      beforeHeight,
      scaledWidth,
      scaledHeight,
      scaleFactor,
    } = await convertImageToEmojis({ 
      url: messageImage.attachment, 
      options: { 
        desiredWidth 
      },
    });

    if (isDebug) {
      const debugEmbed = new Discord.MessageEmbed()
      .setTitle("Generate Debug")
      .setDescription("Debug information for generate function.")
      .setColor("#DC2D44")
      .addFields([
        { name: ":file_folder: File name", value: `${messageImage.name}` },
        { name: ":file_folder: File size", value: `${messageImage.size / 1000000}mb` },
        { name: ":link: URL", value: `${messageImage.url}` },
        { name: ":left_right_arrow: Desired width", value: `${desiredWidth}px` },
        { name: ":left_right_arrow: Width", value: `${beforeWidth}px`, inline: true },
        { name: ":arrow_up_down:  Height", value: `${beforeHeight}px`, inline: true },
        { name: "Compressed width", value: `${scaledWidth}px` },
        { name: "Compressed height", value: `${scaledHeight}px` },
        { name: ":scales: Scale factor", value: `${scaleFactor}` },
        { name: ":hash: Number of emojis used", value: imageEmojis.length },
        { name: ":artist: Palette", value: `${imagePalette.map((emoji) => emoji.emoji).join(" ")}` }
      ]);

      message.channel.send(debugEmbed);
    }

    if (!isMock) {
      sendEmojis({ imageEmojis, width: desiredWidth, channel: message.channel });
    }
	},
};