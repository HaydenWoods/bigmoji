const Discord = require("discord.js");
const PackageJSON = require("../package.json");
const fs = require("fs");

const BigMojiLog = require("./helpers/log");

// Constants
const COMMANDS_PREFIX = "🅱️";
const COMMANDS_ROOT = `${__dirname}/commands`;
const COMMANDS_FILE_TYPE = ".js";

BigMojiLog.info(`${PackageJSON.name} (${PackageJSON.version})`);

const client = new Discord.Client();

// Commands
const commandFiles = fs.readdirSync(COMMANDS_ROOT).filter((file) => file.endsWith(COMMANDS_FILE_TYPE));
client.commands = new Discord.Collection();
commandFiles.forEach((file) => {
  const command = require(`${COMMANDS_ROOT}/${file}`);

  command.aliases.forEach((alias) => {
    client.commands.set(alias, command);
  });
});

// Startup
client.on("ready", () => {
  BigMojiLog.info("Started successfully");
  
  // Status to annoy Sean
  client.user.setStatus("dnd");
});

client.on("message", (message) => {
  if (message.author.bot) {
    return;
  }
  if (!message.content.startsWith(COMMANDS_PREFIX)) {
    return;
  }

  const messageWithoutPrefix = message.content.slice(COMMANDS_PREFIX.length).trim();
  const messageArgs = messageWithoutPrefix.split(" ").filter(arg => arg[0] !== "-") || [];
  const messageFlags = messageWithoutPrefix.split(" ").filter(arg => arg[0] === "-") || [];

  const commandName = (messageArgs.shift() || "").toLowerCase();  
  const command = client.commands.get(commandName);

  if (!command) {
    return BigMojiLog.error("Error: Invalid BigMoji command.");
  }

  command.execute(message, messageArgs, messageFlags);
});

// Login
client.login(process.env.BOT_TOKEN);