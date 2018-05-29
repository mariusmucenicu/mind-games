function processFormData(btnId) {
    var userAnswerForm = document.getElementById('user-answer');
    var metaData = document.getElementById('user-answer').elements.metadata.value;
    var sendData = document.getElementById('user-answer').elements['hit-it-form'];
    metaData = JSON.parse(metaData.replace(/'/g, '"'));

    if (btnId === 'feeling-lucky-btn') {
        var lowerBound = metaData.start_internal;
        var upperBound = metaData.stop_internal;
        var randomNumber = Math.floor(Math.random() * (upperBound-lowerBound+1) + lowerBound);
        metaData.answer = randomNumber;
    } else {
        metaData.answer = Number(sendData.value);
  }
   sendData.type = 'hidden';
   sendData.name = 'data';
   sendData.value = JSON.stringify(metaData);
}


function checkEmptyForm() {
    if (document.getElementById('hit-it-form').value) {
        document.getElementById('hit-it-btn').disabled = false;
    } else {
        document.getElementById('hit-it-btn').disabled = true;
    }
}
