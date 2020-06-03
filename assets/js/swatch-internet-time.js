$(document).ready(function() {
  if ($( "#unix_time" ).length) {
  	$('#unix_time').html(Math.round(new Date().getTime()/1000));
  	// display at page load
  	GetInternetTime();

  	// calculate every second
  	setInterval(GetInternetTime, 1000);

    // display the Colorian date
    if ($( "#colorian_date" ).length) {
      var date = new Date();
      date.setTime(date.getTime() + (1*60*60*1000));
      show_date = date.toISOString().slice(0,10);
      $( "#date_"+show_date ).removeClass("d-none");
    }
	}
});

// calculate the time of the future
function GetInternetTime() {
  // increment unix time
  $('#unix_time').html(parseInt($('#unix_time').text())+1);

  // get date in UTC/GMT
  var date = new Date();
  var hours = date.getUTCHours();
  var minutes = date.getUTCMinutes();
  var seconds = date.getUTCSeconds();

  // add hour to get time in Switzerland
  hours = (hours == 23) ? 0 : hours + 1;

  // time in seconds
  var timeInSeconds = (((hours * 60) + minutes) * 60) + seconds;

  // there are 86.4 seconds in a beat
  var secondsInABeat = 86.4;

  // calculate beats to two decimal places
  var beats = Math.abs(timeInSeconds / secondsInABeat).toFixed(2);

  // update page
  // http://www.swatchclock.com/about.php
  $('#swatch_time').html("Internet time is @"+beats+" beats.");
}
