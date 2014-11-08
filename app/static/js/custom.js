$(document).ready(function() {

	$("[id$='-table']").hide(); 

	$(".expand").click(function() {
		var id = $(this).attr('id');  
		var end_index = id.indexOf("-expand"); 
		var resource_type = id.substring(0, end_index); 
		var table_to_expand = resource_type + "-table"; 
		if ($("#"+table_to_expand).is(":hidden")) {
			$("#"+table_to_expand).slideDown("medium", function() {
				$(this).show(); 
			});
		} else {
			$("#"+table_to_expand).slideUp("medium", function() {
				$(this).hide(); 
			});
		}
	})
});

