
(function() {

    var spinner = null;

    var loginWarn = function() {

        console.log("loginWarn called");

        $("#login").addClass("login_warning");
        
        $("#main").stop(true).animate({"left": "-30px"}, 70, "swing", function() {
            $(this).animate({"left": "30px"}, 140, "swing", function() {
                $(this).animate({"left": "0px"}, 70, "swing");
            })
        });

    };

    var submit = function() {
        
        var userInfo = window.getFBUserInfo();
        if (!userInfo) {
            loginWarn();
            return;
        }

        $("#entry").attr("disabled", true);
        $("#main").addClass("inflight");

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

    });

})();