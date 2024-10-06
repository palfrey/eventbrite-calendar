Eventbrite Calendar
===================

[Eventbrite](https://www.eventbrite.com/) lets you list your tickets, but it doesn't let you automagically export events to a calendar. This app fixes that.

Usage
=====

Goto https://eventbrite.tevp.net/ and follow the instructions to get an iCalendar URL.

Local setup
===========
1. Goto https://www.eventbrite.com/account-settings/apps and setup an app
2. Copy `env.sh.example` to `env.sh`. Replace the following with items from step 1:
   * `EVENTBRITE_API_KEY` with the API key
   * `EVENTBRITE_OAUTH_SECRET` with the "Client secret"
3. `source env.sh`
4. Run `make run`
5. Goto http://localhost:5000/