import os
from flask import Flask, render_template, request, redirect
from flask.ext.bootstrap import Bootstrap
from urllib2 import urlopen, Request
from urllib import urlencode
import json
from icalendar import Calendar, Event
import pytz
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)

app.config['BOOTSTRAP_USE_MINIFIED'] = True
app.config['BOOTSTRAP_USE_CDN'] = True
app.config['BOOTSTRAP_FONTAWESOME'] = True

eventbrite_api_key = os.environ["EVENTBRITE_API_KEY"]

@app.route('/')
def index():
	if request.args.has_key("code"):
		return redirect("/oauth/%s" % request.args["code"])
	return render_template('index.html', eventbrite_api_key = eventbrite_api_key)

@app.route("/oauth/<code>")
def oauth(code):
	url = "https://www.eventbrite.com/oauth/token"
	data = urlopen(url, urlencode({
		"code": code,
		"client_secret": os.environ["EVENTBRITE_OAUTH_SECRET"],
		"client_id": eventbrite_api_key,
		"grant_type": "authorization_code"}))
	values = json.loads(data.read())
	return redirect("/calendar/%s"%values["access_token"])

@app.route('/calendar/<code>')
def calendar(code):
	url = "https://www.eventbrite.com/json/user_list_tickets?type=all"
	print url
	data = urlopen(Request(url = url, headers= {"Authorization": "Bearer %s"%code})).read()
	data = json.loads(data)

	cal = Calendar()
	cal.add('prodid', '-//Eventbrite calendar//tevp.net//')
	cal.add('version', '2.0')

	for order in data["user_tickets"][1]["orders"]:
		order = order["order"]
		event = Event()
		print order.keys()
		event.add('summary', order["event"]["title"])
		event.add('description', order["event"]["description"])
		venue = ", ".join([order["event"]["venue"][k] for k in ("address", "address_2", "city", "postal_code")])
		event.add('location', venue)
		dformat = "%Y-%m-%d %H:%M:%S"
		event.add('dtstart', datetime.strptime(order["event"]["start_date"], dformat))
		event.add('dtend', datetime.strptime(order["event"]["end_date"], dformat))
		event.add('dtstamp', datetime.strptime(order["modified"], dformat))
		event['uid'] = order["id"]
		cal.add_component(event)

	return cal.to_ical()

if '__main__' == __name__:
	app.run(debug=True)
