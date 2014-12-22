
$(document).ready(function() {

	// Hide all food resource tables initially.
	$(".admin-food-resource-type").hide(); 
	$(".admin-food-resource").hide(); 

	// Remove a food resource without reloading page.
	$("[id$='remove']").click(function() {
		var id = $(this).attr('id');
		var dashIndex = id.indexOf("-"); 
		var food_resource_id = id.substring(0, dashIndex); 
		$.getJSON($SCRIPT_ROOT + '/_remove', {
        		id: food_resource_id
        	},
        	function(data) {
        		hide("food-resource-" + food_resource_id);
        		hide("food-resource-" + food_resource_id + "-table");
        	});  
	});	

	// Approves a food resource without reloading page.
	$("[id$='approve']").click(function() {
		console.log('here1');
		var id = $(this).attr('id');
		var dashIndex = id.indexOf("-"); 
		var food_resource_id = id.substring(0, dashIndex); 
		$.getJSON($SCRIPT_ROOT + '/_approve', {
        		id: food_resource_id
        	},
        	function(data) {
        		hide("food-resource-" + food_resource_id);
        		hide("food-resource-" + food_resource_id + "-table");
        	});  
	});	

	// If an "Expand" button is pressed, either show or hide the associated
	// food resource table.
	$(".expand-food-resource-type").click(function() {
		var id = $(this).attr('id');  
		var prefix = "food-resource-type-expand-"; 
		var start_index = prefix.length; 
		var resource_type = id.substring(start_index); 
		var table_to_expand = resource_type + "-table"; 		
		expand(table_to_expand); 
		toggleExpandSymbol("food-resource-type-expand-" + resource_type);
	})

	$(".expand-food-resource").click(function() {
		var id = $(this).attr('id');  
		var prefix = "food-resource-expand-"; 
		var start_index = prefix.length; 
		var resource_id = id.substring(start_index); 
		var table_to_expand = "food-resource-" + resource_id + "-table"; 		
		expand(table_to_expand); 
		toggleExpandSymbol("food-resource-expand-" + resource_id);
	})

    $(".start-edit").click(function() {
		CKEDITOR.disableAutoInline = true;
    	var editor1 = CKEDITOR.inline("editor1", {
    		startupFocus: true,
    		autoGrow_onStartup: true
    	});
    	$(".start-edit").hide();
    	$(".end-edit").show();
    	$("#editor1").attr("contenteditable","true");
    });

    $(".end-edit").click(function() {
    	if ( editor1 ){
    		var json_data = {
    			page_name: $(".end-edit").attr("id"),
    			edit_data: CKEDITOR.instances.editor1.getData()
    		};
    		$.post(url = $SCRIPT_ROOT + '/_edit', data = json_data);
			CKEDITOR.instances.editor1.destroy();
		}
    	$(".end-edit").hide();
    	$(".start-edit").show();
    	$("#editor1").attr("contenteditable","false");
      	});

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

function expand(id) {
	if ($("#"+id).is(":hidden")) {
		show(id);
	} else {
		hide(id);
	}
}

function hide(id) {
	$("#"+id).slideUp("medium", function() {
		$(this).hide(); 
	});
}

function show(id) {
	$("#"+id).slideDown("medium", function() {
		$(this).show(); 
	});
}

function toggleExpandSymbol(id) {
	if ($("#"+id).html() == "-") {
		$("#"+id).html("+");
	} else {
		$("#"+id).html("-");
	}
}