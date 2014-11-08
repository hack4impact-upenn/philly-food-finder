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
});

