import time
import datetime
from requests_oauthlib import OAuth2Session

graph_url = 'https://graph.microsoft.com/v1.0'

def get_user(token):
  graph_client = OAuth2Session(token=token)
  # Send GET to /me
  user = graph_client.get('{0}/me'.format(graph_url))
  # Return the JSON result
  return user.json()

def get_calendar_events(token):
  # graph_client = OAuth2Session(token=token)
  # query_params = {
  #   '$select': 'subject,organizer,attendees,start,end,location',
  #   '$orderby': 'createdDateTime DESC'
  # }
  # events = graph_client.get('{0}/me/events'.format(graph_url), params=query_params)
  graph_client = OAuth2Session(token=token)
  now = datetime.datetime.now()
  start = now - datetime.timedelta(days=3)
  stop = now + datetime.timedelta(days=3)
  # Configure query parameters to
  # modify the results
  query_params = {
    'startDateTime': start,
    'endDateTime': stop
  }
  events = graph_client.get('{0}/users/amemeetinginfo@analogic.com/calendar/calendarView'.format(graph_url),params=query_params)
  # Return the JSON result
  return events.json()

def get_wlq_events(token):
  graph_client = OAuth2Session(token=token)
  now = datetime.datetime.now()
  start = now - datetime.timedelta(days=3)
  stop = now + datetime.timedelta(days=3)
  # Configure query parameters to
  # modify the results
  query_params = {
    'startDateTime': start,
    'endDateTime': stop
  }
  # Send GET to /me/calendarView
  #a='{0}/me/calendarview'.format(graph_url), params=query_params
  wlq = graph_client.get('{0}/users/crameswlq@analogic.com/calendar/calendarView'.format(graph_url), params=query_params)
  # Return the JSON result
  return wlq.json()
def get_big_events(token):
  graph_client = OAuth2Session(token=token)
  now = datetime.datetime.now()
  start = now - datetime.timedelta(days=3)
  stop = now + datetime.timedelta(days=3)
  # Configure query parameters to
  # modify the results
  query_params = {
    'startDateTime': start,
    'endDateTime': stop
  }
  # Send GET to /me/calendarView
  #a='{0}/me/calendarview'.format(graph_url), params=query_params
  big = graph_client.get('{0}/users/cramesbig@analogic.com/calendar/calendarView'.format(graph_url), params=query_params)
  # Return the JSON result
  return big.json()
def get_hpy_events(token):
  graph_client = OAuth2Session(token=token)
  now = datetime.datetime.now()
  start = now - datetime.timedelta(days=3)
  stop = now + datetime.timedelta(days=3)
  # Configure query parameters to
  # modify the results
  query_params = {
    'startDateTime': start,
    'endDateTime': stop
  }
  # Send GET to /me/calendarView
  #a='{0}/me/calendarview'.format(graph_url), params=query_params
  hpy = graph_client.get('{0}/users/crameshpy@analogic.com/calendar/calendarView'.format(graph_url), params=query_params)
  # Return the JSON result
  return hpy.json()
def get_xa_events(token):
  graph_client = OAuth2Session(token=token)
  # Send GET to /me/calendarView
  #a='{0}/me/calendarview'.format(graph_url), params=query_params
  xa = graph_client.get('{0}/users/cramesxa@analogic.com/calendar/events'.format(graph_url))
  # Return the JSON result
  return xa.json()