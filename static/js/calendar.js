

function Calendar(){}
Calendar.init = function(id){
	//$("#id tbody")
	var calendar = $("#"+id);
	var tbody = calendar.find("tbody.events")	
	// 7 am - 10pm
    for(var i=9; i<21; i++){        
    	// 7 days
    	var tr = $("<tr></tr>")
        tr.append("<td>"+i+":00</td>")
           
        for(var d=0; d<7; d++){
          if(i<=12 && d<5)
            tr.append("<td class='slot calendar-seller' data-day='" + d +"' data-hour='" + i+ "'></td>")
        	else
        	   tr.append("<td class='slot' data-day='" + d +"' data-hour='" + i+ "'></td>")
        }
    	tbody.append(tr)
    }   
	
	
	calendar.find("td.slot").mouseover(function(){
        $(this).addClass("state-hover")
    })
    calendar.find("td.slot").mouseout(function(){        
        $(this).removeClass("state-hover")
    })
    calendar.find("td.slot").click(function(){
        if( $(this).hasClass("calendar-buyer") ){
        	$(this).removeClass("calendar-buyer") 
        	$(this).text("")
        }
        else {
          $("td.calendar-seller.calendar-buyer").removeClass("calendar-buyer").text("")
          
        	$(this).addClass("calendar-buyer")
        	$(this).text( $(this).attr("data-hour") + ":00")

        }
    })
    calendar.find("td.slot").mouseout(function(){        
        
    })
}
