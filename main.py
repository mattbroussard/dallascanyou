#!/usr/bin/env python

import os, datetime, json
from flask import Flask, Response, request
from db import DB

app = Flask(__name__, static_url_path='')

class JSONResponse(Response):
    def __init__(self, obj):
        Response.__init__(
            self,
            json.dumps(obj),
            mimetype='application/json')

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

@app.route("/submit", methods=['POST', 'GET'])
def submitHandler():
    now = datetime.datetime.utcnow().isoformat() + "+0000"
    entry = {
        "userID": request.form["userID"],
        "content": request.form["content"],
        "authorName": "This is a test",
        "timestamp": now
    }
    with DB() as db:
        db.put(entry)
    return JSONResponse([entry])

@app.route("/history")
def historyHandler():
    with DB() as db:
        return JSONResponse(db.get())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.run(host='0.0.0.0', port=port)
