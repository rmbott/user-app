'use strict'

// Change this to your uvicorn server
const server = "http://127.0.0.1:8000";

async function getToken(username, password) {
    const response = await fetch(server + '/token', {
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            },
        body: "grant_type=&username=" + username + "&password=" + password + "&scope=&client_id=&client_secret=",
        method: "post",
        });
    const responseText = await response.text();
    return JSON.parse(responseText);
    }

async function getInfo(token_type, token) {
    const response2 = await fetch(server + '/users/me', {
    method: "GET",
    headers: {
        'accept': 'application/json',
        'Authorization': token_type + " " + token
        }
    });
    return response2;
}

$( document ).ready(function() {
    $("#btn").click(async function(){
        // get the form data
        var formData = new FormData(document.forms[0]);
        var username = formData.get("username");
        var password = formData.get("password");

        // Blank user/pass - dont bother authenticating
        if (username == "" || password == "") {
            $("#result").html("User/pass cannot be blank.");
            return;
        }
        
        var response = await getToken(username, password);
        
        // Not Authorized - Incorrect User/Pass
        if (response.hasOwnProperty("detail")) {
            $("#result").html(response["detail"]);
        
        // Authorized 
        } else if (response.hasOwnProperty("access_token")) {
            $("#login").hide();
            
            // Use the token to get user's email address from the database
            var userInfo = await (await getInfo(response["token_type"], response["access_token"])).text();
            $("#result").html("Authentication succeeded! To prove it, here is your email address from the mock database:<br><strong>" + JSON.parse(userInfo)["email"] + "</strong>");
        }
        });
});
