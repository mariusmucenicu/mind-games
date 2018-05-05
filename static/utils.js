function randomint() {
  var raw_string = document.getElementById('user-gamble').elements['raw_data'].value;
  raw_string = JSON.parse(raw_string.replace(/'/g, '"'));
  left_bound = raw_string.left_bound;
  right_bound = raw_string.right_bound;
  random_number = Math.floor(Math.random() * (right_bound-left_bound+1) + left_bound);
  document.getElementById('user-gamble').elements['answer'].value = random_number
}
