
(function() {
    
    var loggedIn = false;
    var authResponse = null;

    var loginInfo = function() {
        return loggedIn ? {
            userID: authResponse.userID,
            accessToken: authResponse.accessToken
        } : null;
    };

    var updateLoginStatus = function(response) {

        $("#login").removeClass("login_warning");
        authResponse = response.authResponse;

        if (response.status == "connected") {    

            FB.api(
                "/me",
                function (resp) {
                    if (resp && !resp.error) {
                        loggedIn = true;
                        $("#login_message")
                            .text("You are logged in as ");
                        $("<img>")
                            .attr("id", "login_portrait")
                            .attr("src", "http://graph.facebook.com/"+authResponse.userID+"/picture?width=32")
                            .appendTo("#login_message");
                        $("<span>")
                            .attr("id", "login_name")
                            .text(resp.name)
                            .appendTo("#login_message");
                    }
                }
            );

        } else {

            loggedIn = false;
            $("#login_message").text("Only friends of Dallas can ask him to do things.");

        }

    };

    window.onFBLoginCallback = updateLoginStatus;
    window.getFBUserInfo = loginInfo;

})();