document.getElementById("Button1").addEventListener("click", function() {}, false);

function test(){
	var text = document.getElementById("val1").value;
	var text2 = document.getElementById("val2").value;

	//Ensure the numbers are valid
	if (isNaN(parseFloat(text)) || isNaN(parseFloat(text2))){
		alert("Please enter valid numbers in your selections.");
	} else {
		alert(parseFloat(text) + parseFloat(text2));
	}
	//CallWebAPI("https://api.yelp.com/v3/businesses/search?term=delis&latitude=37.786882&longitude=-122.399972");
	//var call;
	//var data = httpGetAsync("https://api.yelp.com/v3/businesses/search?term=delis&latitude=37.786882&longitude=-122.399972", call);


	//alert(call[0]);


	event.preventDefault();



}

/*
function CallWebAPI(URL) {

    // New XMLHTTPRequest
    var request = new XMLHttpRequest();
    request.open("GET", URL, false);
    request.setRequestHeader("Authorization", "Bearer GDiZCRPhWsvt4Tm9iutxJo7dJPFbh7OKV1PwbI5j_8CdmETqvQWHIZ8nTRBYvSpnfXzNAShki4EwUwdmB28NW1psM4Bc2NCo_eBh8ccGaa-nevbE5vS91AK3LETMWHYx");  
    request.send();
    // view request status
    alert(request.status);
    response.innerHTML = request.responseText;
}*/

/*
function httpGetAsync(theUrl, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous
    xmlHttp.setRequestHeader("Authorization", "Bearer GDiZCRPhWsvt4Tm9iutxJo7dJPFbh7OKV1PwbI5j_8CdmETqvQWHIZ8nTRBYvSpnfXzNAShki4EwUwdmB28NW1psM4Bc2NCo_eBh8ccGaa-nevbE5vS91AK3LETMWHYx");
    xmlHttp.send(null);

    return xmlHttp;
}
*/