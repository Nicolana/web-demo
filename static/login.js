$(".login").on("click", function(event){
	var data = {};
	$("input[name!=login]").each(function(i){
		data[$(this).attr('name')] = $(this).val();
	})
	$.post('/login', data, function(payload){
		console.log(payload);
		if (payload.login == 1){
			alert("登录成功");
			window.location.href = '/admin';
		}else{
			alert("登录失败，请重新登录");
		}
	})
})