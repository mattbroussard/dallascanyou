
(function() {

    var spinner = null;

    var loginWarn = function() {

        $("#login").addClass("login_warning");
        
        $("#main").stop(true).animate({"left": "-30px"}, 70, "swing", function() {
            $(this).animate({"left": "30px"}, 140, "swing", function() {
                $(this).animate({"left": "0px"}, 70, "swing");
            })
        });

    };

    var displayPost = function(post) {

        // TODO: use React?

        var postDiv = $("<div>").addClass("post");

        var portrait = $("<img>")
            .addClass("portrait")
            .attr("src", "http://graph.facebook.com/"+post.userID+"/picture?width=128")
            .appendTo(postDiv);
        
        var meta = $("<div>")
            .addClass("meta")
            .appendTo(postDiv);
        var author = $("<h3>")
            .addClass("author")
            .text(post.authorName)
            .appendTo(meta);
        var timestamp = $("<span>")
            .addClass("timestamp")
            .text("Loading...")
            .attr("title", post.timestamp)
            .appendTo(meta)
            .timeago();

        var content = $("<p>")
            .addClass("content")
            .text("Dallas, can you " + post.content + "?")
            .appendTo(postDiv);

        $("#posts .post.empty").remove();
        postDiv.prependTo("#posts");

    };

    var setInflight = function(isInflight) {

        if (isInflight) {
            $("#main").addClass("inflight");
            $("#entry").attr("disabled", true);
        } else {
            $("#main").removeClass("inflight");
            $("#entry")
                .attr("disabled", false)
                .val("")
                .blur();
        }

    };

    var success = function(data, reenable) {

        if (reenable) {
            setInflight(false);
        }

        for (var i = data.length-1; i >= 0; --i) {
            displayPost(data[i]);
        }

    };

    var error = function() {
        
        setInflight(false);
        alert("An unexpected error occurred. Try again?");

    };

    var badAuth = function() {

        $("#login .fb-login-button").hide();
        $("#login_message").text("Sorry, only friends of Dallas may ask him to do things.");
        loginWarn();
        disableLogin();

    };

    var submit = function() {
        
        var userInfo = window.getFBUserInfo();
        var message = $("#entry").val();
        if (!userInfo) {
            loginWarn();
            return;
        }

        setInflight(true);

        $.ajax("/submit", {
            "type": "POST",
            "cache": false,
            "success": function(data, textStatus, jqXHR) {
                if (data.success) {
                    success(data, true);
                } else if (data.badauth) {
                    badAuth();
                }
            },
            "error": function(data, textStatus, jqXHR) {
                error({"error": textStatus});
            },
            "data": {
                "userID": userInfo.userID,
                "accessToken": userInfo.accessToken,
                "message": message
            }
        });

    };

    $(function() {

        $("#entry").bind("keyup", function(event) {
            if (event.which == 10 || event.which == 13) {
                submit();
            }
        });

        spinner = new Spinner({
            lines: 13,
            length: 9,
            width: 3,
            radius: 12,
            corners: 1,
            rotate: 0,
            direction: 1,
            color: '#000',
            speed: 2,
            trail: 40,
            shadow: false,
            hwaccel: true,
            className: 'spinner',
            zIndex: 2e9,
            top: '67px',
            left: '1110px'
        }).spin($("#spinner")[0]);

        $.ajax("/history", {
            "cache": false,
            "type": "GET",
            "success": function(data, textStatus, jqXHR) {
                success(data, false);
            },
            "error": function(data, textStatus, jqXHR) {
                $("#posts .post.empty:first").text("An error occurred while loading posts.");
            }
        });

    });

})();