const getColorPercentDiff = (colorOne, colorTwo) => {
  const rDiff = (Math.abs(colorOne.r - colorTwo.r) / 255) * 100;
  const gDiff = (Math.abs(colorOne.g - colorTwo.g) / 255) * 100;
  const bDiff = (Math.abs(colorOne.b - colorTwo.b) / 255) * 100;
  const diff = ((rDiff + gDiff + bDiff) / 300) * 100;

  return diff;
}

module.exports = {
  getColorPercentDiff
}