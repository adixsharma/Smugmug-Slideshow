
function getUrls() {
	var $btnPurgeData = $("#PurgeData");
	var $btnPopulateData = $("#PopulateData");
	var $btnGetData = $("#GetData");
	var $divOutput = $("#output");


	// Using the core $.ajax() method
	$.ajax({
	    url: "/slideshow/show/urls.json",
	    data: {
	        offset: 15,
	        limit: 5
	    },
	    type: "GET",
	    dataType : "json"
	})
	  // Code to run if the request succeeds (is done);
	  // The response is passed to the function
	  .done(function( json ) {
			// alert(data[0].id + " | " + data[0].album + " | " + data[0].url + " | " + data[0].datataken); 
			console.log(json);
			
			var urls = json.urls;
			
			var output="<ul>";
            
            for (var i=0; i< urls.length; i++) 
            {
                output+="<li>" + urls[i].id + ",  " + urls[i].album + ",  " + urls[i].url + ",  " + urls[i].datetaken +  "</li>";
            }
            output+="</ul>";
            $divOutput.html(output);

	  })
	  // Code to run if the request fails; the raw request and
	  // status codes are passed to the function
	  .fail(function( xhr, status, errorThrown ) {
	    alert( "Sorry, there was a problem!" );
	    console.log( "Error: " + errorThrown );
	    console.log( "Status: " + status );
	    console.dir( xhr );
	  })
	  // Code to run regardless of success or failure;
	  .always(function( xhr, status ) {
	    console.log( "The request is complete!" );
	  });

}


function xhr_get(url) {

  return $.ajax({
  	url: url,
  	type: 'get',
  	dataType: 'json'
  })
  .always(function() {
    // remove loading image maybe
    console.log( "The request is complete!" );
  })
  .fail(function() {
    // handle request failures
    console.log( "The request failed!" );
  });

}

function purgeData(){
	xhr_get('/slideshow/show/purgedata.json').done(function(data) {
	  // do stuff with data

	  var $divOutput = $("#output");
	  console.log(data);
	  var response = data.count;
	  $divOutput.html("The database now has " + response + " records!");
	});
}

function populateData() {
	xhr_get('/slideshow/show/populatedata.json').done(function(data) {
	  // do stuff with id data
	  var $divOutput = $("#output");
	  console.log(data);
	  var response = data.count;
	  $divOutput.html("The database now has " + response + " records!");

	});
}

function getData() {
	xhr_get('/slideshow/show/urls.json').done(function(data) {
	  // do stuff with id data
	  var $divOutput = $("#output");
	  console.log(data);
	});
}
