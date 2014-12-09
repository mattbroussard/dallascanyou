#!/usr/bin/env python

import os, datetime, json
from flask import Flask, Response, request

app = Flask(__name__, static_url_path='')

@app.route("/fbinit.js")
def facebookInitHandler():
    template = """
    window.fbAsyncInit = function() {
        FB.init({
            appId: '%s',
            xfbml: true,
            status: true,
            cookie: true,
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
def rootHandler():
    return app.send_static_file('index.html')

def dummyResponse(content='implement the backend', userID='mattbroussard', authorName='Your Name Here (requires additional FB API call)'):
    now = datetime.datetime.utcnow().isoformat() + "+0000"
    return json.dumps([{
        'userID': userID,
        'authorName': authorName,
        'timestamp': now,
        'content': content,
    }])
    

@app.route("/submit", methods=['POST'])
def submitHandler():
    return Response(
        dummyResponse(request.form['message'], request.form['userID']),
        mimetype='application/json'
    )

@app.route("/history")
def historyHandler():
    now = datetime.datetime(2014, 12, 5).isoformat()
    return Response(
        dummyResponse(authorName='Matt B.'),
        mimetype='application/json'
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
