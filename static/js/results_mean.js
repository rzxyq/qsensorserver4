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


    
    var globalX = 0;


    var data = []; 


    // Global JSON to keep track of margins 
    // as well as the width and height 
    var margin = { top: 20, right: 20, bottom: 30, left: 50 }
    var width = 960 - margin.left - margin.right; 
    var height = 500 - margin.top - margin.bottom; 



    // x-scale 
    var x = d3.scale.linear().domain([0,250]).range([0,width]); 


    // y-scale 
    var y = d3.scale.linear().domain([1.5,0]).range([0,height]); 


    // x-axis 
    var xAxis = d3.svg.axis().scale(x).orient("bottom"); 


    // y-axis 
    var yAxis = d3.svg.axis().scale(y).orient("left"); 

    // Area under the graph 
    var area = d3.svg.area()
                                        .x(function(d) { return x(d.x) })
                                        .y0(height-1)
                                        .y1(function(d) { return y(d.y) }); 



    // The physical line 
    var line = d3.svg.line()
        .x(function(d) { return x(d.x); })
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
            .text("Mean Peak Phasic Amplitude");


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





    // Won't initially run 
    function UpdateGraph(num) {

        var myJSON = { 'trial_num': num }; 
        var url = "/data/mean_post_graph"
        $.ajax({
            url: url,
            type: 'POST',
            data: JSON.stringify(myJSON),
            dataType: 'JSON',
            success: function(json) {

                if (globalX>= 250) {
                    x = d3.scale.linear().domain([0,globalX]).range([0,width]); 
                    xAxis = d3.svg.axis().scale(x).orient("bottom"); 
                    var xaxis = d3.selectAll(".x.axis"); 
                    xaxis.remove(); 
                    // x-axis setup 
                svg.append("g")
                    .attr("class", "x axis")
                    .attr("transform", "translate(0," + height + ")")
                    .call(xAxis);
                }


                // Log the data_text 
                console.log(json['data_text'])
                var mean = json['mean']; 
                if (mean == null) {
                    mean = data[data.length-1].y; 
                }
                data.push({ x: globalX, y: mean });
                
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


                globalX+=0.3; 
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

