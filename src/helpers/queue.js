const queue = [];

const add = ({ message, messageArgs, messageFlags }) => {
  queue.push({
    message,
    messageArgs,
    messageFlags,
    status: "PENDING",
  });
}

const remove = ({ index }) => {
  queue.splice(index, 1);
}