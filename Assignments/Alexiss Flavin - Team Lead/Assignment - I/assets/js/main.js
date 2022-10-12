function run_this_function(){
	console.log("dsda");
	var n = window.document.getElementById("name").value;
	var q = window.document.getElementById("qualification").value;
	var a = window.document.getElementById("age").value;
	var e = window.document.getElementById("email").value;
	var m = e.match("^\\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$")
	if(n === "" || q === ""  || a === "" || e === ""){
		alert("Please fill all the inputs.");
	}
	else if ( a <= '0' || a >= 100){
		alert("Age is limited within 1-99")
	}
	else if (m == null){
		alert("Enter a valid email")
	}
	else{
		var str = "Name : "+n+"\n\r"+"Qualification : "+q+"\n\r"+"Age : "+a+"\n\r"+"Email : "+e;
		alert(str);
	}
}