$(document).ready(function() {
  var pusher = new Pusher('04baa22ea6e8b380ff7b', {
    cluster: 'eu'
  });
  var patientName;
  var channel = pusher.subscribe('my-channel');
  channel.bind('my-event', function(data) {
    console.log('Received data:', data);
    var id = data.id;
    var alertClass = data.class;
    var patientName = data.Name;
    var urineVolume = data.Volume;
    var room = data.Room
//    var changedDiaper = data.ChangedDiaper
//    var batteryStatus = data.batteryStatus
//    var passedTime = data.passedTime
    var message = data.message;
//    var columnClass = data.column;
    console.log(message + 'Message');
    console.log(patientName + 'PatientName')
	var existingElement = $('.diaper-alert-column .' + id);
    if (existingElement.length > 0) {
      //console.log(id + ' Updating existing element for patient ' + id);
      existingElement.find('.diaper-message').html(
        //'Patient ID: ' + id + '<br />' +
        '<p>' + 'Patient Name: ' + patientName + '<br />' +
        'Room: ' + room + '<br/>' +
        'Alert message: ' + message +'<br />' +
        //'Percentage: ' + urineVolume + '%' + '<br/>' + '</p>'
        'Volume: ' +  urineVolume + 'ml' + '<br/>' + '</p>'
        //'Passed Time: ' + passedTime + '%' + '<br/>' +
        //'Battery status: ' + batteryStatus + '%' + '<br/>' +
        //'Changed Diaper: ' + changedDiaper +  'min' + '</p>'
      );

      existingElement.removeClass('urgent warning well-being').addClass(alertClass);
      //if (alertClass === 'well-being' && (urineVolume > 60 && urineVolume < 90)) {
        if (urineVolume > 200 && urineVolume < 400) {
        console.log('Moving element from wellbeing to soon column');
        existingElement.detach().appendTo('.diaper-alert-column.yellow');
      } else if (urineVolume < 200 ) {
        console.log('Moving element from warning/urgent to well-being column');
        existingElement.detach().appendTo('.diaper-alert-column.green');
      } else if (urineVolume > 400 ) {
        //alert(alertClass)
        console.log('Moving element from warning/well being to Urgent column');
        existingElement.detach().appendTo('.diaper-alert-column.red');
      }
    } else {
      console.log('Creating new element for ID ' + id);
      if (urineVolume > 400) {
        console.log('Adding to emergency column');
        $('.diaper-alert-column.red').append(
          '<div class="diaper-alert ' + alertClass + ' ' + id + '">' +
          //'<p class="diaper-message"> Patient ID: ' + id + '<br />' +
          '<p class="diaper-message"> Patient Name: ' + patientName  + '<br />' +
          'Room: ' + room + '<br/>' +
          'Alert message: ' + message +'<br />' +
          //'Percentage: ' + urineVolume + '%' + '<br/>' +
          'Volume: ' +  urineVolume + 'ml' + ' <br/>' + '</p>' +
          //'Passed Time: ' + passedTime + '%' + '<br/>' +
          //'Battery status: ' + batteryStatus + '%' + '<br/>' +
          //'Changed Diaper: ' + changedDiaper +  'min' + '</p>' +
          '</div>'
        );
      } else if (urineVolume >= 200 && urineVolume < 400) {
          console.log('Adding to soon column');
          $('.diaper-alert-column.yellow').append(
          '<div class="diaper-alert ' + alertClass + ' ' + id + '">' +
          //'<p class="diaper-message"> Patient ID: ' + id + '<br />' +
          '<p class="diaper-message"> Patient Name: ' + patientName  + '<br />' +
          'Room: ' + room + '<br/>' +
          'Alert message: ' + message +'<br />' +
          //'Percentage: ' + urineVolume + '%' + '<br/>' +
          'Volume: ' +  urineVolume + 'ml' + ' <br/>' + '</p>' +
          //'Passed Time: ' + passedTime + '%' + '<br/>' +
          //'Battery status: ' + batteryStatus + '%' + '<br/>' +
          //'Changed Diaper: ' + changedDiaper +  'min' + '</p>' +
          '</div>'
        );

        } else {
        console.log('Adding to well-being column');
        $('.diaper-alert-column.green').append(
        '<div class="diaper-alert ' + alertClass + ' ' + id + '">' +
        //'<p class="diaper-message"> Patient ID: ' + id + '<br />' +
        '<p class="diaper-message"> Patient Name: ' + patientName  + '<br />' +
        'Room: ' + room + '<br/>' +
        'Alert message: ' + message +'<br />' +
        //'Percentage: ' + urineVolume + '%' + '<br/>' +
        'Volume: ' +  urineVolume + 'ml' + ' <br/>' + '</p>' +
          //'Passed Time: ' + passedTime + '%' + '<br/>' +
          //'Battery status: ' + batteryStatus + '%' + '<br/>' +
          //'Changed Diaper: ' + changedDiaper +  'min' + '</p>' +
        '</div>'
        );
      }

//      existingElement.removeClass('urgent warning well-being').addClass(alertClass);
//    } else {
//    	if (alertClass === 'urgent' && urineVolume >=90){
//          console.log('Adding to emergency column');
//		  	$('.diaper-alert-column.red').append(
//			  '<div class="diaper-alert ' + alertClass + ' ' + patientName + '">' +
//			  '<p class="diaper-message"> Patient Name: ' + patientName + '<br />' +
//			  'Room: ' + room + '<br/>' +
//			  ' Alert message: ' + message +'<br />' +
//			  'Volume: ' + urineVolume + '%' + '<br/>' +
//			  ' Passed Time: ' + passedTime + '%' + '<br/>' +
//			  ' Battery status: ' + batteryStatus + '%' + '<br/>' +
//			  'Changed Diaper: ' + changedDiaper +  'min' + '</p>' +
//			  '</div>'
//			);
//		  } else if (alertClass === 'warning' && (urineVolume >=60 && urineVolume<90)) {
//				console.log('Adding to soon column');
//				$('.diaper-alert-column.yellow').append(
//				  '<div class="diaper-alert ' + alertClass + ' ' + patientName + '">' +
//				  '<p class="diaper-message"> Patient Name: ' + patientName + '<br />' +
//				  'Room: ' + room + '<br/>' +
//				  ' Alert message: ' + message + '<br />' +
//				  'Volume: ' + urineVolume + '%' + '<br/>' +
//				  ' Passed Time: ' + passedTime + '%' + '<br/>' +
//				  ' Battery status: ' + batteryStatus + '%' + '<br/>' +
//				  'Changed Diaper: ' + changedDiaper +  'min' + '</p>' +
//			  '</div>'
//			  );
//			} else {
//				console.log('Adding to well-being column');
//				$('.diaper-alert-column.green').append(
//				'<div class="diaper-alert ' + alertClass + '">' +
//				'<p class="diaper-message"> Patient Name: ' + patientName + '<br />' +
//				'Room: ' + room + '<br/>' +
//				' Alert message: ' + message  +'<br />' +
//				'Volume: ' + urineVolume + '%' + '<br/>' +
//				' Passed Time: ' + passedTime + '%' + '<br/>' +
//				' Battery status: ' + batteryStatus + '%' + '<br/>' +
//				'Changed Diaper: ' + changedDiaper +  'min' + '</p>' +
//			  '</div>'
//		  );
//		}
//    };
    };
  });
});
