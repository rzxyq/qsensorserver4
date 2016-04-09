var x;
$(document).ready(function() {
	// Deals with CSRF resolution on AJAX request 
	var csrftoken = Cookies.get('csrftoken'); // Received from the CSRF 
	
	function csrfSafeMethod(method) {
  	// these HTTP methods do not require CSRF protection
  	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}

	$.ajaxSetup({
  	beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
  	}	
	});

	//var globalX = 0;


	var data = []; 

	var place = 0


	// Global JSON to keep track of margins 
	// as well as the width and height 
	var margin = { top: 20, right: 20, bottom: 30, left: 50 }
	var width = 960 - margin.left - margin.right; 
	var height = 500 - margin.top - margin.bottom; 

	var startDate = new Date();
	var endDate = new Date();
	var today = new Date();
	var globalX = new Date();

	endDate.setHours(startDate.getHours() + 2);

	console.log(startDate);
	console.log(endDate);

	var nowmin = today.getMinutes()

	var nowsec = today.getSeconds()
	//var timeFormat = d3.time.format("%X");
	console.log(nowmin, nowsec)
	//console.log(timeFormat)
	//var now = d3.time.minute
	//console.log(now)
	console.log("Start minute: " + today)

	// x-scale 
	//var x = d3.scale.linear().domain([0,250]).range([0,width]); 
	//var format = d3.time.format("%X")
	//var x = d3.time.scale.utc()
	//scale.range([values])

	x = d3.time.scale().domain([startDate,endDate]).range([0, width]);

	//var svg = d3.select('body').append('svg').attr('width', 800).attr('height', 800);

	var xAxis = d3.svg.axis().scale(x).orient('bottom').tickFormat(d3.time.format("%I:%M")).ticks(d3.time.minute,10).innerTickSize(-width)
    	.outerTickSize(0)
    	.tickPadding(10);;
	
	//svg.append('g').attr('class', 'axis').call(xAxis).attr('transform','translate(20, 10)');


	//var x = d3.time.scale().domain([today.getMinutes()-nowmin, (+80)]).range([0, width])
	//var x = d3.time.scale().domain([startmin]).range([0,width]); 


	// y-scale 
	var y = d3.scale.linear().domain([1.5,0]).range([0,height]); 


	// x-axis 
	//var xAxis = d3.svg.axis().scale(x).orient("bottom").ticks(20); 


	// y-axis 
	var yAxis = d3.svg.axis().scale(y).orient("left").innerTickSize(-width)
    	.outerTickSize(0)
    	.tickPadding(10);

    var line = d3.svg.line()
    	.x(function(d) { return x(d.x); })
    	.y(function(d) { return y(d.y); }); 

	// Area under the graph 
	var area = d3.svg.area()
		.x(function(d) { return x(d.x) })
		.y0(height-1)
		.y1(function(d) { return y(d.y) }); 

	// The physical line 
	var line = d3.svg.line()
		.x(function(d) { return d.x; }) //x(d.x)?
		.y(function(d) { return y(d.y); });

	var svg = d3.select(".svg-section").append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	    .style("margin-top", "40px")
	    .style("margin-left", "40px")
	  	.append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	    svg.append("text")
        	.attr("x", (width / 2))             
        	.attr("y", 0 - (margin.top / 10))
        	.attr("text-anchor", "middle")  
        	.style("font-size", "16px") 
        	.style("fill", "red")
        	.style("font-weight", "bold")  
        	.text("Raw EDA");

	// x-axis setup 
  	svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  // y-axis setup 
  	svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)

 	svg.append("path")
 		.datum(data)
 		.attr("class", "area")
 		.attr("d", area); 

	svg.append("path")
		.datum(data)
		.attr("class", "line")
		.attr("d", line);

	//vertical lines
	/*svg.selectAll(".vline").data(d3.range(200)).enter()
	    .append("line")
	    .attr("x1", function (d) { return d * 50; })
	    .attr("x2", function (d) { return d * 50; })
	    .attr("y1", function (d) { return 0; })
	    .attr("y2", function (d) { return height; })
	    .style("stroke", "#eee");
*/
	// Won't initially run 
	function UpdateGraph(num) {

		var myJSON = { 'trial_num': num }; 
		var url = "/data/post_graph"
		$.ajax({
			url: url,
			type: 'POST',
			data: JSON.stringify(myJSON),
			dataType: 'JSON',
			success: function(json) {
				//if (globalX>= 250) {
					//x = d3.scale.linear().domain([0,globalX]).range([0,width]);
					//x = d3.time.scale().domain(today,endDate).range([0, width]);
					//xAxis = d3.svg.axis().scale(60).orient("bottom");
					//xAxis = d3.svg.axis().scale(x).orient('bottom').tickFormat(d3.time.format("%H:%M:%S")).ticks(d3.time.minutes, 5);
					//xAxis = d3.svg.axis().scale(x).orient('bottom').tickFormat(d3.time.format("%H:%M:%S")).ticks(d3.time.minutes, 5);
					//var xaxis = d3.selectAll(".x.axis"); 
					//xaxis.remove(); 
					// x-axis setup 
	  				
				//}

				today = new Date()
				hourstamp = today.getHours()
				minutestamp = today.getMinutes()
				secondstamp = today.getSeconds()
				var curTime = hourstamp + ":" + minutestamp + ":" + secondstamp;
				console.log(curTime);
				// Log the data_text 
				console.log(json['data_text'])
				var eda = json['eda']; 
				if (eda == null) {
					eda = data[data.length-1].y;
				}
				data.push({ x: x(globalX), y: eda });
				
				var linez = d3.selectAll(".line"); 
				linez.remove(); // Remove the paths 
				var areaz = d3.selectAll(".area"); 
				areaz.remove(); // Remove all areas

				svg.append("path")
					.datum(data)
					.attr("class", "line")
					.attr("d", line);

				svg.append("path")
 					.datum(data)
 					.attr("class", "area")
 					.attr("d", area); 

 /*				if (secondstamp%10 == 0){
 				 	console.log("5 secs")
 				// 	place += 5
 				// 	console.log("Place,", place)
	 			 	var marker = d3.select(".svg-section").append("svg")

	 			 		marker.append("text")
	 			 			.attr("x", place)             
         					.attr("y", 0 - (margin.top / 10))
         					.attr("text-anchor", "middle")  
         					.style("font-size", "14px") 
         					.style("fill", "red")
         					.style("font-weight", "bold")  
         					.text("10s stamp");
	 			// 		//this is making a rectangle pop up every 5 seconds but the rectangle is in a random place and has no useful information. 
 				}
*/
				globalX.setMilliseconds(globalX.getMilliseconds()+300);
 				console.log(globalX);
 				// Delay 0.3 seconds 
				setTimeout(function() { UpdateGraph(num) }, 300); 
			}, 
			error: function(xhr, err, errmsg) {
				console.log("Erroorr..."); 
			}

		}); 

	}


	// On click, do this 
	$("#getData").on('click', function(e) {
		// Deals with CSRF resolution on AJAX request 
		var csrftoken = Cookies.get('csrftoken'); // Received from the CSRF 
		function csrfSafeMethod(method) {
	  	// these HTTP methods do not require CSRF protection
	  	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		}
		$.ajaxSetup({
	  	beforeSend: function(xhr, settings) {
	      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	          xhr.setRequestHeader("X-CSRFToken", csrftoken);
	      }
	  	}	
		});
		var test_num = prompt("Enter a trial number");
		UpdateGraph(test_num); // Update the graph
	}); 
}); 