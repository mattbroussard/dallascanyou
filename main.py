#!/usr/bin/env python

import os, datetime, json
from flask import Flask, Response, request
import facebook
from twilio.rest import TwilioRestClient
from db import DB

app = Flask(__name__, static_url_path='')

class JSONResponse(Response):
    def __init__(self, obj):
        Response.__init__(
            self,
            json.dumps(obj),
            mimetype='application/json'
        )

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

def sendText(content, name):
    sid = os.environ.get("TWILIO_ACCOUNT_SID", "")
    authToken = os.environ.get("TWILIO_AUTH_TOKEN", "")
    src = os.environ.get("TWILIO_PHONE", "")
    dest = os.environ.get("DEST_PHONE", "")
    client = TwilioRestClient(sid, authToken)

    body = "Dallas, can you %s? -%s (via http://j.mp/dallascan)" % (content, name)

    client.messages.create(
        body=body,
        to=dest,
        from_=src,
    )


def parseName(meObj):
    if "first_name" not in meObj or "last_name" not in meObj or meObj["first_name"] == meObj["last_name"]:
        return meObj["name"]
    return "%s %s." % (meObj["first_name"], meObj["last_name"][0])

# returns a string containing the user's name if successful, None otherwise
def verifyIdentity(accessToken, userID):
    fb = facebook.GraphAPI(accessToken)
    
    legal = os.environ.get("AUTHORIZED_FB_FRIENDS", "").split(",")
    whitelistMode = os.environ.get("AUTHORIZATION_MODE", "whitelist") == "whitelist"
    foundFriend = False
    
    for friend in legal:
        if friend == userID:
            foundFriend = True
            break

        if whitelistMode:
            continue

        result = fb.get_connections("me", "friends/%s" % friend)
        if len(result["data"]) > 0:
            foundFriend = True
            break
    
    if not foundFriend:
        return None

    me = fb.get_object("me")

    if "id" not in me or me["id"] != userID:
        return None

    return parseName(me)

@app.route("/submit", methods=['POST'])
def submitHandler():
    now = datetime.datetime.utcnow().isoformat() + "+0000"
    name = verifyIdentity(request.form["accessToken"], request.form["userID"])

    if not name:
        return JSONResponse({"badAuth": True})

    entry = {
        "userID": request.form["userID"],
        "content": request.form["content"],
        "authorName": name,
        "timestamp": now
    }

    with DB() as db:
        db.put(entry)
    
    sendText(request.form["content"], name)

    return JSONResponse([entry])

@app.route("/history")
def historyHandler():
    with DB() as db:
        return JSONResponse(db.get())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.run(host='0.0.0.0', port=port)
