import time
import datetime
from requests_oauthlib import OAuth2Session
import json

from tutorial.models import Attendees, Events, User

graph_url = 'https://graph.microsoft.com/v1.0'

def getquery_params():
  now = datetime.datetime.now()
  start = now - datetime.timedelta(days=2)
  stop = now + datetime.timedelta(days=2)
  query_params = {
      'startDateTime': start,
      'endDateTime': stop
    }
  return query_params

body ={
  "timeConstraint": {
    "timeslots": [
      {
        "start": {
          "dateTime": "2019-11-26T13:52:46.483Z",
          "timeZone": "Pacific Standard Time"
        },
        "end": {
          "dateTime": "2019-12-03T13:52:46.483Z",
          "timeZone": "Pacific Standard Time"
        }
      }
    ]
  },
  "locationConstraint": {
    "isRequired": "false",
    "suggestLocation": "true",
    "locations": [
      {
        "displayName": "Conf Room 32/1368",
        "locationEmailAddress": "conf32room1368@imgeek.onmicrosoft.com"
      }
    ]
  },
}
body2={
  "message": {
    "subject": "会议签到率",
    "body": {
      "contentType": "HTML",
      "content": """  <h3>会议主题</h3>
	   <br>开始时间: 111</br>
		<br>结束时间: 222</br>
		<br>组织者: aaa</br>
		<br>地点: Analogic</br>
		<br>
		<div id="table" style="width: 400px; height: 400px; padding-top: 20px; -ms-user-select: none; -webkit-tap-highlight-color: transparent;" _echarts_instance_="ec_1574902933374">
		<table
			style="width: 70%;border:0;solid:#F00;border-collapse: collapse;" cellpadding="10" border="1" cellspacing="0">
		<thead>
			<tr class="info" style="background-color: #d9edf7;">
				<th style="min-width:40px">序号</th>
				<th style="min-width:70px">部门</th>
				<th style="min-width:70px">姓名</th>
				<th style="min-width:120px">会议时间</th>
				<th style="min-width:120px">签到时间</th>
			</tr>
		  </thead>
		  <tbody id="tbody" >
		  <tr style="background-color: #fcf8e3;"><td>1</td><td border="1">Project</td><td>Wu, Alicia</td><td>2019-11-27 15:30:00</td><td></td></tr>
		  <tr style="background-color: #fcf8e3;"><td>2</td><td>Engineering</td><td>Yang, Anderson</td><td>2019-11-27 15:30:00</td><td></td></tr>
		  <tr style="background-color: #fcf8e3;"><td>3</td><td></td><td>Wang, Charles</td><td>2019-11-27 15:30:00</td><td></td></tr>
		  <tr style="background-color: #fcf8e3;"><td>4</td><td>QA</td><td>Weng, Haiming</td><td>2019-11-27 15:30:00</td><td></td></tr>
		  <tr style="background-color: #fcf8e3;"><td>5</td><td></td><td>Huang, Maggie</td><td>2019-11-27 15:30:00</td><td></td></tr>
		  <tr style="background-color: #fcf8e3;"><td>6</td><td></td><td>Liu, Xuelin</td><td>2019-11-27 15:30:00</td><td></td></tr>
		  <tr style="background-color: #fcf8e3;"><td>7</td><td>Project</td><td>Chen, Jessica</td><td>2019-11-27 15:30:00</td><td></td></tr>
		  </tbody>
		  </table>
		  </div>"""
    },
    "toRecipients": [
      {
        "emailAddress": {
          "address": "yqi@analogic.com"
        }
      }
    ],
    "internetMessageHeaders":[
      {
        "name":"x-custom-header-group-name",
        "value":"Nevada"
      },
      {
        "name":"x-custom-header-group-id",
        "value":"NV001"
      }
    ]
  }
}
def getbody(eventid):
  event=Events.objects.filter(Id=eventid).last()
  body="<h3>"+event.Subject+"</h3><br>开始时间: "+str(event.Start)+"<br>结束时间: "+str(event.End)+\
       "</br><br>组织者: "+event.Organizer+"<br>地点: "+event.Location+"</br></br>"
  body+="""
  <div id="table" style="width: 400px; height: 400px; padding-top: 20px; -ms-user-select: none; -webkit-tap-highlight-color: transparent;" _echarts_instance_="ec_1574902933374">
		<table
			style="width: 60%;border:0;solid:#F00;border-collapse: collapse;" cellpadding="10" border="1" cellspacing="0">
		<thead>
			<tr class="info" style="background-color: #d9edf7;">
				<th style="min-width:40px">序号</th>
				<th style="min-width:70px">部门</th>
				<th style="min-width:70px">姓名</th>
				<th style="min-width:120px">签到时间</th>
			</tr>
		  </thead>
		  <tbody id="tbody" >
		  """
  addresses = Attendees.objects.filter(Eventid=eventid)
  i=0
  for address in addresses:
      i+=1
      user = User.objects.filter(Address=address.Address).values("Group")
      group=user[0].get("Group")
      if(address.Isattend==0 or address.Isattend==3):
        body += "<tr style=\"background-color: #FF0000;\"><td>" + str(i) + "</td><td>" + group + "</td><td>" + address.Name + "</td><td>未签到</td></tr>"
      elif(address.Isattend==2):
          body+="<tr style=\"background-color: #FFA500;\"><td>"+str(i)+"</td><td>"+group+"</td><td>"+address.Name+"</td><td>" + str(address.Attendtime) + " (迟到)</td></tr>"
      elif(address.Isattend==1):
          body += "<tr style=\"background-color: #dff0d8;\"><td>" + str(i) + "</td><td>" + group + "</td><td>" + address.Name + "</td><td>" + str(address.Attendtime) + "</td></tr>"
  body+="</tbody></table></div></br></br></br>"
  return body
def getaddress(eventid):
  addresslist=[]
  addresses=Attendees.objects.filter(Eventid=eventid).values("Address")
  for address in addresses:
    emailAddress = {}
    emailAddress["emailAddress"] = {"address": address.get("Address")}
    addresslist.append(emailAddress)
  return addresslist
def gettoken():
  import requests

  url = "https://login.microsoftonline.com/8d6cef01-7674-4e8e-9b9f-1753140a64ea/oauth2/v2.0/token"

  payload = "client_id=86e9bc73-bf36-4597-b92e-1704a2b5a057&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default&grant_type=client_credentials&client_secret=XU%5B%3D18V%2FBsgJ%2Byrm8k314YDPSx%40y6wi9"
  headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Host': "login.microsoftonline.com",
  }

  response = requests.request("POST", url, data=payload, headers=headers)
  #print(payload.get("message"))
  return(json.loads(response.text))

def sendevents(graph_client1):
    now = datetime.datetime.now()
    begin = now - datetime.timedelta(minutes=10)
    meetings = Events.objects.all().filter(End__gte=begin, End__lte=now).order_by("-Id")
    for meet in meetings:
        if (meet.Mailsend == 0):
            body2["message"]["toRecipients"] = getaddress(meet.Id)
            body2["message"]["body"]["content"] = getbody(meet.Id)
            body2["message"]["subject"] = "会议签到率--" + Events.objects.filter(Id=meet.Id).last().Subject
            graph_client1.post('{0}/users/amemeetinginfo@analogic.com/sendMail'.format(graph_url), json=body2)
            Events.objects.filter(Id=meet.Id).update(Mailsend=1)

def senduser(day,graph_client1):
    addresses = Attendees.objects.all().filter(Meetingtime__contains=day).distinct().values("Address")#今天有会议的全部用户邮箱（已去重）
    for address in addresses:
        eventids=Attendees.objects.all().filter(Meetingtime__contains=day,Address=address["Address"]).distinct().values("Eventid")#该用户今天的全部会议id
        bodys=""
        for eventid in eventids:
            body=getbody(eventid["Eventid"])
            bodys+=body
        body2["message"]["toRecipients"] = [{"emailAddress": address}]
        body2["message"]["body"]["content"] = bodys
        body2["message"]["subject"] = "会议签到率--" + str(day)
        graph_client1.post('{0}/users/amemeetinginfo@analogic.com/sendMail'.format(graph_url), json=body2)
            #Events.objects.filter(Id=meet.Id).update(Mailsend=1)

def get_user(token):
  acctoken=gettoken()
  graph_client = OAuth2Session(token=token)
  # Send GET to /me
  user = graph_client.get('{0}/me'.format(graph_url))
  # Return the JSON result
  #data111 =graph_client.post('{0}/me/findMeetingTimes'.format(graph_url),data = body)
  #print(data111.json())
  graph_client.headers = json.dumps({'Content-Type': 'application/json','User-Agent': 'python-requests/2.22.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*',
                                     'Connection': 'keep-alive'})
  #print(graph_client.headers)
  #data222 = graph_client.post('{0}/me/sendMail'.format(graph_url), json=body2)
  #print(data222)
  graph_client1 = OAuth2Session(token=acctoken)
  graph_client1.headers = json.dumps(
    {'Content-Type': 'application/json', 'User-Agent': 'python-requests/2.22.0', 'Accept-Encoding': 'gzip, deflate',
     'Accept': '*/*', 'Connection': 'keep-alive'})
  #data222 = graph_client1.post('{0}/users/amemeetinginfo@analogic.com/sendMail'.format(graph_url), json=body2)
  #sendevents(graph_client1)
  now = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
  weekday=now.weekday()
  if(weekday<5):
      #print("Today: 周"+str(weekday))
      now = int(time.time() - time.timezone) % 86400
      begin = 9 * 3600
      end = 9 * 3600 + 10 * 60
      if (begin < now and now < end):#早上9点发送邮件
          if(weekday==0):
              day = datetime.date.today() + datetime.timedelta(days=-3)
          else:
              day = datetime.date.today() + datetime.timedelta(days=-1)
          events=Events.objects.filter(Start__contains=day).all()
          if(events):
              if(events[0].Mailsend==0):
                  print(str(day)+" Send mails")
                  senduser(day,graph_client1)
                  for event in events:
                      Events.objects.filter(Id=event.Id).update(Mailsend=1)

  return user.json()


def get_calendar_events(token):
  query_params=getquery_params()
  graph_client = OAuth2Session(token=token)
  events = graph_client.get('{0}/users/amemeetinginfo@analogic.com/calendar/calendarView'.format(graph_url),params=query_params)
  # Return the JSON result
  return events.json()

def get_wlq_events(token):
  query_params = getquery_params()
  graph_client = OAuth2Session(token=token)
  wlq = graph_client.get('{0}/users/crameswlq@analogic.com/calendar/calendarView'.format(graph_url), params=query_params)
  return wlq.json()
def get_big_events(token):
  query_params = getquery_params()
  graph_client = OAuth2Session(token=token)
  big = graph_client.get('{0}/users/cramesbig@analogic.com/calendar/calendarView'.format(graph_url), params=query_params)
  # Return the JSON result
  return big.json()
def get_hpy_events(token):
  query_params = getquery_params()
  graph_client = OAuth2Session(token=token)
  hpy = graph_client.get('{0}/users/crameshpy@analogic.com/calendar/calendarView'.format(graph_url), params=query_params)
  # Return the JSON result
  return hpy.json()
def get_xa_events(token):
  query_params = getquery_params()
  graph_client = OAuth2Session(token=token)
  xa = graph_client.get('{0}/users/cramesxa@analogic.com/calendar/calendarView'.format(graph_url),params=query_params)
  #xa = graph_client.get('{0}/users/cramesxa@analogic.com/calendar/events'.format(graph_url))
  # Return the JSON result
  return xa.json()
def get_bj_events(token):
  query_params = getquery_params()
  graph_client = OAuth2Session(token=token)
  bj = graph_client.get('{0}/users/CRAmesSmall@analogic.com/calendar/calendarView'.format(graph_url), params=query_params)
  return bj.json()
def get_hz_events(token):
  query_params = getquery_params()
  graph_client = OAuth2Session(token=token)
  hz = graph_client.get('{0}/users/crameshz@analogic.com/calendar/calendarView'.format(graph_url), params=query_params)
  return hz.json()
def get_km_events(token):
  query_params = getquery_params()
  graph_client = OAuth2Session(token=token)
  km = graph_client.get('{0}/users/crameskm@analogic.com/calendar/calendarView'.format(graph_url), params=query_params)
  return km.json()
def get_nanj_events(token):
  query_params = getquery_params()
  graph_client = OAuth2Session(token=token)
  nanj = graph_client.get('{0}/users/cramesnanj@analogic.com/calendar/calendarView'.format(graph_url), params=query_params)
  return nanj.json()
def get_qd_events(token):
  query_params = getquery_params()
  graph_client = OAuth2Session(token=token)
  qd = graph_client.get('{0}/users/cramesqd@analogic.com/calendar/calendarView'.format(graph_url), params=query_params)
  return qd.json()
def get_qh_events(token):
  query_params = getquery_params()
  graph_client = OAuth2Session(token=token)
  qh = graph_client.get('{0}/users/cramesqh@analogic.com/calendar/calendarView'.format(graph_url), params=query_params)
  return qh.json()
def get_sanya_events(token):
  query_params = getquery_params()
  graph_client = OAuth2Session(token=token)
  sanya = graph_client.get('{0}/users/cramessanya@analogic.com/calendar/calendarView'.format(graph_url), params=query_params)
  return sanya.json()
def get_trn_events(token):
  query_params = getquery_params()
  graph_client = OAuth2Session(token=token)
  trn = graph_client.get('{0}/users/cramestrn@analogic.com/calendar/calendarView'.format(graph_url), params=query_params)
  return trn.json()
def get_sc_events(token):
  query_params = getquery_params()
  graph_client = OAuth2Session(token=token)
  sc = graph_client.get('{0}/users/cramessc@analogic.com/calendar/calendarView'.format(graph_url), params=query_params)
  return sc.json()
def get_vc_events(token):
  query_params = getquery_params()
  graph_client = OAuth2Session(token=token)
  vc = graph_client.get('{0}/users/SHVideoRoom@analogic.com/calendar/calendarView'.format(graph_url), params=query_params)
  return vc.json()