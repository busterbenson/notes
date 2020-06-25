$(document).ready(function() {
  if ($( "#unix_time" ).length) {
  	$('#unix_time').html(Math.round(new Date().getTime()/1000));
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

  var moon_data;
  $.ajax({
    type: "GET",
    url: "https://docs.google.com/spreadsheets/d/e/2PACX-1vTdQ5uyfXljN9Bfihg82JL1eRcqvIJZzWLGHd2JR3tKR0IPES0MawDU-scNHHhovFY4ALV4cyFYZMhb/pub?gid=1303742322&single=true&output=csv",
    dataType: "text",       
    success: function(response)  
      {
        var moon_data = $.csv.toArrays(response);
        var moon_phase = ""
        // 0 lunation, 1 days since new moon, 2 last new moon, 
        // 3 days til next new moon, 4 next new moon,
        // 5 days til next full moon, 6 next full moon.
        if (moon_data[0]) {
          if (parseInt(moon_data[0][2]) < 2 || parseInt(moon_data[0][2]) >= 29) {
            moon_phase = "🌑 "
          } else if (parseInt(moon_data[0][2]) < 6) {
            moon_phase = "🌒 "
          } else if (parseInt(moon_data[0][2]) < 10) {
            moon_phase = "🌓 "
          } else if (parseInt(moon_data[0][2]) < 15) {
            moon_phase = "🌔 "
          } else if (parseInt(moon_data[0][2]) < 17) {
            moon_phase = "🌕 "
          } else if (parseInt(moon_data[0][2]) < 21) {
            moon_phase = "🌖 "
          } else if (parseInt(moon_data[0][2]) < 24) {
            moon_phase = "🌗 "
          } else if (parseInt(moon_data[0][2]) < 29) {
            moon_phase = "🌘 "
          }

          var chimera_date = moon_phase
          if (parseInt(moon_data[0][6]) < 5) {
            chimera_date += " The next full moon is in "
            if (moon_data[0][6] == '1') {
              chimera_date += "1 day."
            } else {
              chimera_date += moon_data[0][6]+" days."              
            }
          } else if (parseInt(moon_data[0][4]) < 5) {
            chimera_date += " The next new moon is in "
            if (parseInt(moon_data[0][4]) == 1) {
              chimera_date += "1 day."
            } else {
              chimera_date += moon_data[0][4]+" days."              
            }
          } else if (parseInt(moon_data[0][2]) < 31) {
            if (parseInt(moon_data[0][2]) == 1) {
              chimera_date += "1 day "
            } else {
              chimera_date += moon_data[0][2]+" days "              
            }
            chimera_date += "since the last new moon."
          }
          $('#chimera_date').html(chimera_date)
        }
      }
    }, 
  ).fail(function(response) { 
    console.log(response); 
  }) 
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
  $('#chimera_time').html("Internet time is @"+beats+" beats.");
}
