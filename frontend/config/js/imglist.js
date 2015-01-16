var id = $.getUrlVar("id");
getUserImageIds = $.ajax( {
	url: "db.php",
	async: true,
	type: "POST",
	dataType: "json",
	data: {"method":"getuserimageids", "id": id }
});
getUserData = $.ajax( {
	url: "db.php",
	async: true,
	type: "POST",
	dataType: "json",
	data: {"method":"getuserdata", "id": id }
});
jQuery( document ).ready(function() {
	getUserData.done(function(data){
		$( "#name" ).html( "Photos for "+data[0].nickname+" ("+data[0].firstname+" "+data[0].lastname+")" );
	});
	getUserImageIds.done(function(data){
		for(var i = 0, l = data.length; i < l; ++i){
			$( "#body" ).append( '<img src="img.php?id='+ data[i].id +'">' );
		}
	});
});
