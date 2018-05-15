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

function changeIntervalDelimitersColor() {
    var interval = document.getElementById('interval');
    var intervalDelimiters = ['[', '(', ')', ']', ',']

    for (var i = 0; i < intervalDelimiters.length; i++) {
        var delimiter = intervalDelimiters[i]
        var delimiterExists = interval.innerHTML.indexOf(delimiter);
        if (delimiterExists !== -1) {
            var customHTML = '<span style="color:black;">{}</span>'.replace('{}', delimiter);
            interval.innerHTML = interval.innerHTML.replace(delimiter, customHTML);
        }
    }
}
