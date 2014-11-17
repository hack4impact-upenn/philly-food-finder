
$(document).ready(function() {

	// Hide all food resource tables initially.
	$("[id$='-table']").hide(); 

	// If an "Expand" button is pressed, either show or hide the associated
	// food resource table.
	$(".expand").click(function() {
		// Get the id of the associated food resource table.
		var id = $(this).attr('id');  
		var end_index = id.indexOf("-expand"); 
		var resource_type = id.substring(0, end_index); 
		var table_to_expand = resource_type + "-table"; 

		$.getJSON($SCRIPT_ROOT + '/_admin', {
        	a: "hello",
        	b: "goodbye"
      	}, function(data) {
        	console.log(data); 
        	// create table entries with data in them
      	});

		// If the table is currently hidden, show the table.
		if ($("#"+table_to_expand).is(":hidden")) {
			$("#"+table_to_expand).slideDown("medium", function() {
				$(this).show(); 
			});
		// Else hide the table.
		} else {
			$("#"+table_to_expand).slideUp("medium", function() {
				$(this).hide(); 
			});
		}
	})

	// Hide all time-selectors iniially.
	$("[class$='-time-picker']").hide(); 

	$('select.open-or-closed').on('change', function (e) {
	    var optionSelected = $("option:selected", this);
	    var valueSelected = this.value;
	    var parentName = optionSelected.parent().attr("name"); 
	    var endIndex = parentName.indexOf("-"); 
	    var dayOfWeek = parentName.substring(0, endIndex);
	    if (valueSelected == "open") {
	    	$("." + dayOfWeek + "-time-picker").show();
	    } else if (valueSelected == "closed") {
	    	$("." + dayOfWeek + "-time-picker").hide();
	    }
	});
});


