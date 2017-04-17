
function updateTime() {
	var currentTime = new Date();
	var hours = currentTime.getHours();
	var minutes = currentTime.getMinutes();
	var seconds = currentTime.getSeconds();
	if (minutes < 10){
		minutes = "0" + minutes;
	}
	if (seconds < 10){
		seconds = "0" + seconds;
	}				
	setTimeout("updateTime()",1000);
	document.getElementById('time').innerHTML= hours + ":" + minutes + ":" + seconds;
}

function alert(link) {
	if (confirm('Вы уверены, что хотите удалить данную запись?')) {
		window.location = link;
	}
	else {
		return;
	}
}
