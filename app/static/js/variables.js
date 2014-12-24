

var html = '<div id="{{ resource_info.id }}-table" class="admin-food-resource-type">' +
'	{% if not resources[resource_info.id] %}' +
'		<div class="no-resources-message">There are no {{ resource_info.lowercase_name }} in the database.</div>' +
'	{% endif %}' +

'	{% for resource in resources[resource_info.id] %}' + 
'		<div class="resource">' +

'			<!-- Resource header -->' + 
'			<div class= "row" id="food-resource-{{ resource.id }}">' + 
'				<div class="small-1 columns expand-food-resource" id="food-resource-expand-{{ resource.id }}">' + 
'					+' + 
'				</div>' + 
'				<div class="small-7 columns">' + 
'					data["{{ resource.name }}"]' + 
'				</div>' + 
'				<div class="small-2 columns">' + 
'					<a href="{{ url_for("new", id=resource.id) }}" class="food-resource-update-button">Edit</a>' + 
'				</div>' + 
'				<div class="small-2 columns">' + 
'					<div id="{{ resource.id }}-remove" class="food-resource-update-button">Remove</div>' + 
'				</div>' + 
'			</div>' + 
'			<!-- Resource content -->' +  
'			<div class="row admin-food-resource" id="food-resource-{{ resource.id }}-table">' + 
'				<div class="large-6 small-12 columns">' + 
'					<div class="row">' + 
'						<div class="small-3 columns">' + 
'							Name:' + 
'						</div>' + 
'						<div class="small-9 columns">' + 
'							{{ resource.name }}' + 
'						</div>' + 
'					</div>' + 
'					<div class="row">' + 
'						<div class="small-3 columns">' + 
'							Address:' + 
'						</div>' + 
'						<div class="small-9 columns">' + 
'							{% if resource.address.line1 %}' + 
'								{{ resource.address.line1 }}' + 
'							{% endif %}' + 
'							{% if resource.address.line2 %}' + 
'								<br>' + 
'								{{ resource.address.line2 }}' + 
'							{% endif %}' + 
'							<br>' + 
'							{{ resource.address.city }},' +  
'							{{ resource.address.state }}' +  
'							{{ resource.address.zip_code }}' + 
'						</div>' + 
'					</div>' + 
'					<div class="row">' + 
'						<div class="small-3 columns">' + 
'							Zip Code:' + 
'						</div>' + 
'						<div class="small-9 columns">' + 
'							{{ resource.address.zip_code }}' + 
'						</div>' + 
'					</div>' + 
'					<div class="row">' + 
'						<div class="small-3 columns">' + 
'							Phone Number:' + 
'						</div>' + 
'						<div class="small-9 columns">' + 
'							{{ resource.phone_numbers[0].number }}' + 
'						</div>' + 
'					</div>' + 
'					<div class="row">' + 
'						<div class="small-3 columns">' + 
'							Website:' + 
'						</div>' + 
'						<div class="small-9 columns">' + 
'							{% if resource.url %}' + 
'								<a href="{{ resource.url }}">{{ resource.url }}</a>' + 
'							{% else %}' + 
'								None listed.' + 
'							{% endif %}' + 
'						</div>' + 
'					</div>' + 
'					<div class="row">' + 
'						<div class="small-3 columns">' + 
'							Description:' + 
'						</div>' + 
'						<div class="small-9 columns">' + 
'							{% if resource.description %}' + 
'								{{ resource.description }}' + 
'							{% else %}' + 
'								No description.' + 
'							{% endif %}' + 
'						</div>' + 
'					</div>' + 
'					<div class="row">' + 
'						<div class="small-3 columns">' + 
'							Family and children?' + 
'						</div>' + 
'						<div class="small-9 columns">' + 
'							{% if resource.is_for_family_and_children %}' + 
'								Yes' + 
'							{% else %}' + 
'								No' + 
'							{% endif %}' + 
'						</div>' + 
'					</div>' + 
'					<div class="row">' + 
'						<div class="small-3 columns">' + 
'							Seniors?' + 
'						</div>' + 
'						<div class="small-9 columns">' + 
'							{% if resource.is_for_seniors %}' + 
'								Yes' + 
'							{% else %}' + 
'								No' + 
'							{% endif %}' + 
'						</div>' + 
'					</div>' + 
'					<div class="row">' + 
'						<div class="small-3 columns">' + 
'							Wheelchair accessible?' + 
'						</div>' + 
'						<div class="small-9 columns">' + 
'							{% if resource.is_wheelchair_accessible %}' + 
'								Yes' + 
'							{% else %}' + 
'								No' + 
'							{% endif %}' + 
'						</div>' + 
'					</div>' + 
'					<div class="row">' + 
'						<div class="small-3 columns">' + 
'							Accepts SNAP?' + 
'						</div>' + 
'						<div class="small-9 columns">' + 
'							{% if resource.is_accepts_snap %}' + 
'								Yes' + 
'							{% else %}' + 
'								No' + 
'							{% endif %}' + 
'						</div>' + 
'					</div>' + 
'				</div>' + 
'				<div class="large-6 small-12 columns">' + 
'					<div class="row">' + 
'						<div class="small-3 columns">' + 
'							Hours: <!--{{ resource.timeslots }}-->' + 
'						</div>' + 
'						<div class="small-9 columns">' + 
'							{% for day in days_of_week %}' + 
'								<div class="row">' + 
'									<div class="small-6 columns">' + 
'										{{day["name"]}}' + 
'									</div>' + 
'									<div class="small-6 columns">' + 
'										{% for timeslot in resource.timeslots %}' + 
'											{% if timeslot.day_of_week == day["index"] %}' + 
'												{{ timeslot.start_time.strftime("%I:%M %p") }} - {{ timeslot.end_time.strftime("%I:%M %p") }}' + 
'											{% endif %}' + 
'										{% endfor %}' + 
'									</div>' + 
'								</div>' + 
'							{% endfor %}' + 
'						</div>' + 
'					</div>' + 
'				</div>' + 
'			</div>' + 
'		</div>' + 
'	{% endfor %}' + 
'</div>'; 