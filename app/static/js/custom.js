
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

    $("#start_edit").click(function() {
		CKEDITOR.disableAutoInline = true;
    	var editor1 = CKEDITOR.inline("editor1");
    	$("#start_edit").hide();
    	$("#end_edit").show();
    	$("#editor1").attr("contenteditable","true");
    });

    $("#end_edit").click(function() {
    	if ( editor1 ){
    		var json_data = {edit_page: CKEDITOR.instances.editor1.getData()};
    		console.log(json_data);
    		$.post(url = $SCRIPT_ROOT + '/_edit', data = json_data);
			CKEDITOR.instances.editor1.destroy();
		}
    	$("#end_edit").hide();
    	$("#start_edit").show();
    	$("#editor1").attr("contenteditable","false");
      	});

		// DISPLAY CURRENT COURSES AT TOP OF PAGE
        /*$.ajax({
            url: '/_admin', 
            type: 'POST', 
            dataType: 'json',
            data: { step: 1 },
            success: function(response) {
            
                // save Timestamp
                current_timestamp = response.current_timestamp;
                
                // display agenda
                updateAgenda(response, current_timestamp);
            } 
        });*/

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


