const Discord = require("discord.js");

module.exports = {
	name: "help",
	aliases: ["help"],
	description: "Provides help around the BigMoji bot commands.",
	execute(message) {
		const debugEmbed = new Discord.MessageEmbed()
		.setTitle(":b: BigMoji")
		.setDescription("A Discord bot to create recreations of images using emojis.")
		.setAuthor("Hayden Woods")
		.setColor("#DC2D44")
		.addFields([
			{ name: "help", value: "You are here." },
			{ name: "ping", value: "Ping the bot." },
			{ name: "generate [size] -(debug|mock)", value: "When sent along with an attached image, will convert it into a series of messages that will roughly resemble in image. If you have trouble seeing the entire picture (some of the lines may wrap), try zooming out with `ctrl -`." },
		]);

		message.channel.send(debugEmbed);
	},
};