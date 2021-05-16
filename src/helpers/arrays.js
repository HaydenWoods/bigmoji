function chunkArray(array, chunk_size){
  var index = 0;
  var arrayLength = array.length;
  var tempArray = [];
  
  for (index = 0; index < arrayLength; index += chunk_size) {
    myChunk = array.slice(index, index+chunk_size);
    tempArray.push(myChunk);
  }

  return tempArray;
}

module.exports = {
  chunkArray,
}