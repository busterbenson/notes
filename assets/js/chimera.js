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

  // Airtable
  var Airtable = require('airtable');
  Airtable.configure({
      endpointUrl: 'https://api.airtable.com',
      apiKey: 'keyYFIU6joNuVlc8D'
  });
  var base = Airtable.base('appTQedJfHdBgtXZk');

  base('Moon Data').select({
      // Selecting the first 1 record in Current Moon:
      maxRecords: 2,
      view: "Current Moon"
  }).eachPage(function page(records, fetchNextPage) {
      // This function (`page`) will get called for each page of records.

      // This moon
      var record = records[0]
      if (record) {
        var new_moon = moment(record.get('New Moon Date').toString()+' '+record.get('New Moon Time').toString()+' GMT+00:00')
        // console.log('This moon: ', new_moon.toDate())

        var days_since_new_moon = moment().diff(new_moon,'days');
        console.log('Days since new moon: '+days_since_new_moon)

        var full_moon = moment(record.get('Full Moon').toString()+' '+record.get('Full Moon Time').toString()+' GMT+00:00')
        // console.log('Full moon: ', full_moon.toDate())

        var days_til_full_moon = full_moon.diff(moment(), 'days');
        // console.log('Days til full moon: '+days_til_full_moon)

      }

      // Next moon
      var next_record = records[1]
      if (next_record) {
        var next_moon = moment(next_record.get('New Moon Date').toString()+' '+next_record.get('New Moon Time').toString()+' GMT+00:00')
        // console.log('Next moon: ', next_moon.toDate())

        var days_til_new_moon = next_moon.diff(moment(), 'days');
        // console.log('Days til next new moon: '+days_til_new_moon)
      }

      // console.log("DAYS: "+days_since_new_moon)
      var moon_phase = ""
      if (days_since_new_moon) {
        if (days_since_new_moon < 2 || days_since_new_moon >= 29) {
          moon_phase = "🌑 "
        } else if (days_til_full_moon == 0) {
          moon_phase = "🌕 "
        } else if (days_since_new_moon < 6) {
          moon_phase = "🌒 "
        } else if (days_since_new_moon < 10) {
          moon_phase = "🌓 "
        } else if (days_since_new_moon < 15) {
          moon_phase = "🌔 "
        } else if (days_since_new_moon < 17) {
          moon_phase = "🌕 "
        } else if (days_since_new_moon < 21) {
          moon_phase = "🌖 "
        } else if (days_since_new_moon < 24) {
          moon_phase = "🌗 "
        } else if (days_since_new_moon < 29) {
          moon_phase = "🌘 "
        }
      }

      // FULL MOONS
      if (days_til_full_moon < 7 && days_til_full_moon > -7) {
        if (days_til_full_moon == 0) {
          moon_phase += " Today is the full moon! "
        } else if (days_til_full_moon >= 1) {
          moon_phase += " The next full moon is in "
          if (days_til_full_moon == 1) {
            moon_phase += "1 day."
          } else {
            moon_phase += days_til_full_moon+" days."              
          }
        } else {
          moon_phase += " The full moon was "
          if (days_til_full_moon == -1) {
            moon_phase += "1 day ago."
          } else {
            moon_phase += Math.abs(days_til_full_moon)+" days ago."              
          }
        }

      // NEW MOONS
      } else {
        if (days_since_new_moon == 0) {
          moon_phase += " Today is a new moon! "
        } else if (days_til_new_moon > 0 && days_til_new_moon < 15) {
          moon_phase += " The next new moon is in "
          if (days_til_new_moon == 1) {
            moon_phase += "1 day."
          } else {
            moon_phase += days_til_new_moon+" days."              
          }
        } else {
          if (days_since_new_moon == -1) {
            moon_phase += " The new moon was "
            moon_phase += "1 day ago."
          } else if (days_since_new_moon) {
            moon_phase += " The new moon was "
            moon_phase += days_since_new_moon+" days ago."              
          } else {
            // Say nothing because it is confusing.
            console.log('days_since_new_moon = '+days_since_new_moon)
          }

        }
      }
      $('#chimera_date').html(moon_phase)

      // To fetch the next page of records, call `fetchNextPage`.
      // If there are more records, `page` will get called again.
      // If there are no more records, `done` will get called.
      // fetchNextPage();

  }, function done(err) {
      if (err) { console.error(err); return; }
  });
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
