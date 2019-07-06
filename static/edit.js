document.getElementById("move-back").addEventListener("click", function(){
	window.location.href = "/admin";
})

$("#save").on("click", function(event){
	var title = $("input[name=title]").val();
	var content = $("#content").val();
	var blog_id = $("#blog-id");
	var data = {};
	if (blog_id != null){
		data.p = blog_id.attr('data-id');
	}
	data.title = title;
	data.contents = content;

	$.post("/edit", data, function(payload){
		if (payload.success == 1){
			window.location.href = "/admin";
		} else {
			alert("添加失败，请检查网络");
		}
	})
})


function addContent(data){
	$("#content").val(data);
}