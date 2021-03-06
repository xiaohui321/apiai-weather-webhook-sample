#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import sendgrid
from sendgrid.helpers.mail import *

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    
    print("Request:")
    print(json.dumps(req, indent=4))
    
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    result = req.get("result")
    parameters = result.get("parameters")
    ordinal = parameters.get("ordinal")
    price = parameters.get("unit-currency")
    which_one = parameters.get("Which-One")
    print(parameters)
    num = -1
    if ordinal == 1 or price == "999 dollars" or which_one == "most expensive one":
        num = 1
    elif ordinal == 2 or price == "499 dollars":
        num = 2
    elif ordinal == 3 or price == "99 dollars" or which_one == "cheapest one":
        num = 3
    print("sending email")
    sendEmail(num);
    
    speech = "Sure. Buying these tickets now. " + \
    "You will receive an confirmation email to finalize your purchase. " + \
    "Hope you will have a fun night there!"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

def sendEmail(num):
    print("test")
    sg = sendgrid.SendGridAPIClient(apikey="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")
    from_email = Email("order-from-google-assistant@vividseats.com")
    subject = "Order Confromation - Concert ticket"
    to_email = Email("zhouxiaohui93321@gmail.com")
    content = Content("text/plain", "Please confirm your purchase by clicking this link:" + num)
    mail = Mail(from_email, subject, to_email, content)
    print("test 2")
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
