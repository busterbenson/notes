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
        // console.log('Days since new moon: '+days_since_new_moon)

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
        } else if (days_til_full_moon > 1) {
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
          moon_phase += " The new moon was "
          if (days_since_new_moon == -1) {
            moon_phase += "1 day ago."
          } else {
            moon_phase += days_since_new_moon+" days ago."              
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

  // Stored here:
  // https://docs.google.com/spreadsheets/d/1d-A1ukLf1WWGEI1I0dxMrvqNEhV5iS9q0UZTnmGyP6I/edit#gid=841331532

  // var moon_data;
  // $.ajax({
  //   type: "GET",
  //   url: "https://docs.google.com/spreadsheets/d/e/2PACX-1vTdQ5uyfXljN9Bfihg82JL1eRcqvIJZzWLGHd2JR3tKR0IPES0MawDU-scNHHhovFY4ALV4cyFYZMhb/pub?gid=1303742322&single=true&output=csv",
  //   dataType: "text",       
  //   success: function(response)  
  //     {
  //       var moon_data = $.csv.toArrays(response);
  //       var moon_phase = ""
  //       // 0 lunation, 1 days since new moon, 2 last new moon, 
  //       // 3 days til next new moon, 4 next new moon,
  //       // 5 days til next full moon, 6 next full moon.
  //       if (moon_data[0]) {
  //         if (parseInt(moon_data[0][2]) < 2 || parseInt(moon_data[0][2]) >= 29) {
  //           moon_phase = "🌑 "
  //         } else if (parseInt(moon_data[0][2]) < 6) {
  //           moon_phase = "🌒 "
  //         } else if (parseInt(moon_data[0][2]) < 10) {
  //           moon_phase = "🌓 "
  //         } else if (parseInt(moon_data[0][2]) < 15) {
  //           moon_phase = "🌔 "
  //         } else if (parseInt(moon_data[0][2]) < 17) {
  //           moon_phase = "🌕 "
  //         } else if (parseInt(moon_data[0][2]) < 21) {
  //           moon_phase = "🌖 "
  //         } else if (parseInt(moon_data[0][2]) < 24) {
  //           moon_phase = "🌗 "
  //         } else if (parseInt(moon_data[0][2]) < 29) {
  //           moon_phase = "🌘 "
  //         }

  //         var chimera_date = moon_phase

  //         // FULL MOONS
  //         if (parseInt(moon_data[0][6]) < 7 && parseInt(moon_data[0][6]) > -7) {
  //           if (parseInt(moon_data[0][6]) == 0) {
  //             chimera_time = " Today is the full moon. "
  //           } else if (parseInt(moon_data[0][6]) > 0) {
  //             chimera_date += " The next full moon is in "
  //             if (moon_data[0][6] == '1') {
  //               chimera_date += "1 day."
  //             } else {
  //               chimera_date += moon_data[0][6]+" days."              
  //             }
  //           } else {
  //             chimera_date += " The full moon was "
  //             if (moon_data[0][6] == '-1') {
  //               chimera_date += "1 day ago."
  //             } else {
  //               chimera_date += Math.abs(moon_data[0][6])+" days ago."              
  //             }
  //           }

  //         // NEW MOONS
  //         } else if (parseInt(moon_data[0][4]) < 7 && parseInt(moon_data[0][4]) > -7) {
  //           if (parseInt(moon_data[0][4]) == 0) {
  //             chimera_date += " The next new moon is today."
  //           } else if (parseInt(moon_data[0][4]) > 0) {
  //             chimera_date += " The next new moon is in "
  //             if (parseInt(moon_data[0][4]) == 1) {
  //               chimera_date += "1 day."
  //             } else {
  //               chimera_date += moon_data[0][4]+" days."              
  //             }
  //           } else {
  //             chimera_date += " The next new moon was "
  //             if (parseInt(moon_data[0][4]) == -1) {
  //               chimera_date += "1 day ago."
  //             } else {
  //               chimera_date += Math.abs(moon_data[0][4])+" days ago."              
  //             }

  //           }

  //         // AFTER THE NEW MOON
  //         } else if (parseInt(moon_data[0][2]) < 31 && parseInt(moon_data[0][2]) > 0) {
  //           if (parseInt(moon_data[0][2]) == 1) {
  //             chimera_date += "1 day "
  //           } else {
  //             chimera_date += moon_data[0][2]+" days "              
  //           }
  //           chimera_date += "since the last new moon."
  //         }
  //         $('#chimera_date').html(chimera_date)
  //       }
  //     }
  //   }, 
  // ).fail(function(response) { 
  //   console.log(response); 
  // }) 
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
