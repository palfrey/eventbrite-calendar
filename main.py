import os
from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from urllib.request import urlopen, Request
from urllib.parse import urlencode
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

@app.route('/', endpoint="index")
def index():
	if "code" in request.args:
		return redirect("/oauth/%s" % request.args["code"])
	return render_template('index.html', eventbrite_api_key = eventbrite_api_key)

@app.route("/oauth/<code>")
def oauth(code: str):
	url = "https://www.eventbrite.com/oauth/token"
	data = urlopen(url, urlencode({
		"code": code,
		"client_secret": os.environ["EVENTBRITE_OAUTH_SECRET"],
		"client_id": eventbrite_api_key,
		"grant_type": "authorization_code"}).encode('utf-8'))
	values = json.loads(data.read())
	return redirect("/calendar/%s"%values["access_token"])

@app.route('/calendar/<code>')
def calendar(code: str):
	url = "https://www.eventbriteapi.com/v3/users/me/orders/?expand=event,event.venue"
	data = urlopen(Request(url = url, headers= {"Authorization": "Bearer %s"%code})).read()
	data = json.loads(data)
	if "error" in data:
		raise Exception(data["error"])

	cal = Calendar()
	cal.add('prodid', '-//Eventbrite calendar//tevp.net//')
	cal.add('version', '2.0')
	if "orders" in data:
		cal.add('X-WR-CALNAME', 'Eventbrite Calendar for %s'%(data["orders"][0]["email"]))

		for order in data["orders"]:
			event_data = order["event"]
			event = Event()
			event.add('summary', event_data["name"]["text"])
			event.add('description', event_data["description"]["text"])
			if event_data["venue"] is not None:
				event.add('location', event_data.get("venue",{}).get("address", {}).get("localized_address_display"))
			dformat = "%Y-%m-%dT%H:%M:%SZ"
			utc = pytz.timezone("UTC")
			event.add('dtstart', datetime.strptime(event_data["start"]["utc"], dformat).replace(tzinfo=utc))
			event.add('dtend', datetime.strptime(event_data["end"]["utc"], dformat).replace(tzinfo=utc))
			event.add('dtstamp', datetime.strptime(event_data["changed"], dformat).replace(tzinfo=utc))
			if "url" in event_data:
				event.add('url', event_data["url"])
			event['uid'] = order["id"]
			cal.add_component(event)
	else:
		cal.add('X-WR-CALNAME', 'Eventbrite Calendar')

	return cal.to_ical()

if '__main__' == __name__:
	app.run(debug=True)
