
getUserData = $.ajax( {
	url: "db.php",
	async: true,
	type: "GET",
	dataType: "json",
	data: {"method":"getallusers"}
});
jQuery( document ).ready(function() {
	getUserData.done(function(data){
		for(var i = 0, l = data.length; i < l; ++i){
			var userstring = "<tr id="+data[i].id+"\">\n"+
								"<td class=\"firstname\">"+data[i].firstname+"</td>\n"+
								"<td class=\"lastname\">"+data[i].lastname+"</td>\n"+
								"<td class=\"nickname\">"+data[i].nickname+"</td>\n"+
							"</tr>";
			$( "#userlist" ).append( userstring );
		}
	});
});