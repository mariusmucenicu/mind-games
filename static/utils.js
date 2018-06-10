function generateRandomNumber(leftGlyph, rightGlyph, upperBound, lowerBound=0) {
    /* the probability for rolling a correct answer is 100% for open & half-open intervals with the
     * same limits, i.e (2, 2) or [2, 2) will always yield 0 however there is only a 50% chance to
     * for the closed interval, i.e [2, 2] will yield either 0 or 1 (which is intended)
     * and the probability for the rest of the cases is 1/(upperBound + 1)
     */
    openInterval = leftGlyph == '(' && rightGlyph == ')';
    closedInterval = leftGlyph == '[' && rightGlyph == ']';

    if (openInterval) {
        upperBound = upperBound - 1;
    } else if (closedInterval) {
        upperBound = upperBound + 1;
    }

    var minimum = Math.ceil(lowerBound);
    var maximum = Math.floor(upperBound);
    return Math.floor(Math.random() * (maximum - minimum + 1)) + minimum;
}


function processFormData(btnId) {
    var userAnswerForm = document.getElementById('user-answer');
    var metaData = userAnswerForm.elements.metadata.value;
    var sendData = userAnswerForm.elements['hit-it-form'];
    metaData = JSON.parse(metaData.replace(/'/g, '"'));

    if (btnId === 'feeling-lucky-btn') {
        var leftGlyph = metaData.left_glyph;
        var rightGlyph = metaData.right_glyph;
        var upperBound = metaData.stop_internal - metaData.start_internal;
        var randomNumber = generateRandomNumber(leftGlyph, rightGlyph, upperBound);
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
