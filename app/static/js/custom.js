$(document).ready(function() {

	// Hide all food resource tables initially.
	$(".admin-food-resource-type").hide(); 
	$(".admin-food-resource").hide(); 

	// Expand all resources on admin resources page.
	// Triggered when "Expand All" button pressed on admin resources page.
	$("#expand-all-resources-button").click(function() {
		showAll("-table", "expand-food-resource-type");
		showAll("-table", "expand-food-resource");
	}); 

	// Collapse all resources on admin resources page.
	// "Collapse All" button pressed on admin resources page.
	$("#collapse-all-resources-button").click(function() {
		hideAll("-table", "expand-food-resource-type");
		hideAll("-table", "expand-food-resource");
	}); 

	// Remove a food resource without reloading page.
	$("[id$='remove']").click(function() {
		var id = $(this).attr('id');
		var dashIndex = id.indexOf("-"); 
		var foodResourceID = id.substring(0, dashIndex); 
		$.getJSON($SCRIPT_ROOT + '/_remove', {
        		id: foodResourceID
        	},
        	function(data) {
        		hide("food-resource-" + foodResourceID);
        		hide("food-resource-" + foodResourceID + "-table");
        	});  
	});	

	// Approves a food resource without reloading page.
	$("[id$='approve']").click(function() {
		var id = $(this).attr('id');
		var dashIndex = id.indexOf("-"); 
		var foodResourceID = id.substring(0, dashIndex); 
		$.getJSON($SCRIPT_ROOT + '/_approve', {
        		id: foodResourceID
        	},
        	function(data) {
        		hide("food-resource-" + foodResourceID);
        		hide("food-resource-" + foodResourceID + "-table");
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
		toggleExpansion(table_to_expand, "expand-food-resource-type"); 
	})

	// If an "Expand" button is pressed, either show or hide the associated
	// food resource information. 
	$(".expand-food-resource").click(function() {
		var id = $(this).attr('id');  
		var prefix = "food-resource-expand-"; 
		var start_index = prefix.length; 
		var resource_id = id.substring(start_index); 
		var table_to_expand = "food-resource-" + resource_id + "-table"; 		
		toggleExpansion(table_to_expand, "expand-food-resource"); 
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

/**
@function toggleExpansion Expand or collapse the given ID if it is currently
hidden or visible, respectively.
@param {String} idToToggle - id of the element that should be hidden or shown. 
@param {String} classToToggleExpandSymbol - class of the element whose expand
symbol should be toggled (e.g., "+" to "-" if expanding an element).
*/
function toggleExpansion(idToToggle, classToToggleExpandSymbol) {
	if ($("#"+idToToggle).is(":hidden")) {
		show(idToToggle, classToToggleExpandSymbol);
	} else {
		hide(idToToggle, classToToggleExpandSymbol);
	}
}

/**
@function hide Collapse the element associated with the given ID.
@param {String} idToHide - id of the element that should be hidden. 
@param {String} classToToggleExpandSymbol - class of the element whose expand
symbol should be toggled (e.g., "+" to "-" if expanding an element).
*/
function hide(idToHide, classToToggleExpandSymbol) {
	$("#"+idToHide).slideUp("medium", function() {
		$(this).hide(); 
		$(this).parent().find("." + classToToggleExpandSymbol).html("+"); 
	});
}

/**
@function show Expand the element associated with the given ID.
@param {String} idToShow - id of the element that should be shown. 
@param {String} classToToggleExpandSymbol - class of the element whose expand
symbol should be toggled (e.g., "+" to "-" if expanding an element).
*/
function show(idToShow, classToToggleExpandSymbol) {
	$("#"+idToShow).slideDown("medium", function() {
		$(this).show();
		$(this).parent().find("." + classToToggleExpandSymbol).html("-"); 
	});
}

/**
@function hideAll Collapse all elements with the given ID suffix.
@param {String} idToHide - ID suffix of the elements that should be hidden. 
@param {String} classToToggleExpandSymbol - class of the element whose expand
symbol should be toggled (e.g., "+" to "-" if expanding an element).
*/
function hideAll(idToHide, classToToggleExpandSymbol) {
	$("[id$='" + idToHide + "']").each(function() {
		var id = $(this).attr("id");
		hide(id, classToToggleExpandSymbol);
	}); 
}

/**
@function showAll Expand all elements with the given ID suffix.
@param {String} idToShow - ID suffix of the elements that should be shown. 
@param {String} classToToggleExpandSymbol - class of the element whose expand
symbol should be toggled (e.g., "+" to "-" if expanding an element).
*/
function showAll(idToShow, classToToggleExpandSymbol) {
	$("[id$='" + idToShow + "']").each(function() {
		var id = $(this).attr("id");
		show(id, classToToggleExpandSymbol);
	});
}

function clearTablesOfFoodResources() {
	$(".admin-food-resource-type").remove(); 
	$(".expand-food-resource-type").html("+");
}

function getNoResourcesHtml(resourceInfoId, resourceInfoLowercaseNamePlural) {
	var html = 
	'<div id="' + resourceInfoId + '-table" class="admin-food-resource-type">' +
	'		<div class="no-resources-message">There are no ' 
			+ resourceInfoLowercaseNamePlural + ' in the database.</div>' +
	'</div>';
	return html;
}