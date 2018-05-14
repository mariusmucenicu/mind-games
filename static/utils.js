function randomInt() {
  var rawString = document.getElementById('user-gamble').elements['raw_data'].value;
  rawString = JSON.parse(rawString.replace(/'/g, '"'));
  lowerBound = rawString.start;
  upperBound = rawString.stop;
  random_number = Math.floor(Math.random() * (upperBound-lowerBound+1) + lowerBound);
  document.getElementById('user-gamble').elements['answer'].value = random_number
}

function checkEmptyForm() {
    if (document.getElementById('hit-it-form').value) {
        document.getElementById('hit-it-button').disabled = false;
    } else {
        document.getElementById('hit-it-button').disabled = true;
    }
}
