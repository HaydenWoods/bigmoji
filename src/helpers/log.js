const PackageJSON = require("../../package.json");

const info = (message) => {
  return console.log(`${PackageJSON.title} - Info - ${message}`);
}

const warn = (message) => {
  return console.log(`${PackageJSON.title} - Warn - ${message}`);
}

const error = (message) => {
  return console.log(`${PackageJSON.title} - Error - ${message}`);
}

module.exports = {
  info,
  warn,
  error,
}