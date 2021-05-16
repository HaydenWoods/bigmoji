module.exports = {
	name: "ping",
	aliases: ["ping"],
	description: "Pings the BigMoji bot.",
	execute(message) {
		message.channel.send("Pong.");
	},
};