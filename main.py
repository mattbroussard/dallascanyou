#!/usr/bin/env python

import os
from flask import Flask, Response

app = Flask(__name__, static_url_path='')

@app.route("/fbinit.js")
def facebookInit():
    template = """
    window.fbAsyncInit = function() {
        FB.init({
            appId: '%s',
            xfbml: true,
            status: true,
            version: 'v2.2'
        });
        FB.getLoginStatus(window.onFBLoginCallback);
    };

    (function(d, s, id){
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) {return;}
        js = d.createElement(s); js.id = id;
        js.src = "//connect.facebook.net/en_US/sdk.js";
        fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));
    """

    return Response(
        template % os.environ.get("FB_APP_ID", 0),
        mimetype='text/javascript'
    )

@app.route("/")
def root():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
