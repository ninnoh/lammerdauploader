<!DOCTYPE html> 
<html> 
<head> 
	<title> 
		Caricamentos,.
	</title> 
	
	<script src= 
"https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"> 
	</script> 
</head> 

<body> 
	<div align="center"> 
		<form method="post" action="" enctype="multipart/form-data"
				id="myform"> 

			<div > 
				<input type="file" id="file" name="file" /> 
				<input type="button" class="button" value="Upload"
						id="but_upload"> 
			</div> 
		</form> 
	</div>	 
	
	<script type="text/javascript"> 
		$(document).ready(function() { 






			$("#but_upload").click(function() { 
				var fd = new FormData(); 

				var files = $('#file')[0].files[0]; 

				fd.append(files.name, files); 
	
				$.ajax({ 
					url: 'https://diocane.ml/upload', 
					type: 'post', 
					data: fd, 
					contentType: false, 
					processData: false, 
					success: function(response){ 
						if(response != 0){ 
						alert("lo file e stato downloads!");
                        var res = (response.download_url);
                        document.getElementById("output").innerHTML=res;
                        document.getElementById("output2").setAttribute("href",res);
						} 
						else{ 
							alert('Errore pregasi riprovar'); 
						} 
					}, 
				}); 
			}); 
		}); 
	</script> 
</body> 
<center><a id="output2">Scaricalo,.,</p></center>
<center><p id='output'></p></center>
</html> 
