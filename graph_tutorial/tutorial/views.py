from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from requests_oauthlib import OAuth2Session

#from tutorial.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from tutorial.graph_helper import get_user, get_calendar_events, get_xa_events, get_big_events, \
    get_wlq_events, get_hpy_events, get_bj_events, get_hz_events, get_km_events, get_nanj_events, get_qd_events, \
    get_qh_events, get_sanya_events, get_sc_events, get_trn_events, get_vc_events
import dateutil.parser
import datetime
import json
import re
import pytz

from tutorial.models import Events, Attendees, User

graph_url = 'https://graph.microsoft.com/v1.0'
def home(request):
  context = initialize_context(request)

  return render(request, 'tutorial/home.html', context)

def initialize_context(request):
  context = {}

  # Check for any errors in the session
  error = request.session.pop('flash_error', None)

  if error != None:
    context['errors'] = []
    context['errors'].append(error)

  # Check for user in the session
  context['user'] = request.session.get('user', {'is_authenticated': False})
  return context

def sign_in(request):
  return render(request, 'tutorial/home.html')

def callback(request):
  return render(request, 'tutorial/home.html')

def sign_out(request):
    return render(request, 'tutorial/home.html')

def calendar(request,pIndex):
    # 将新会议添加到数据库中
    #updatemeeting(gettoken())
    now = datetime.datetime.now()
    start = now - datetime.timedelta(days=1)
    stop = now + datetime.timedelta(days=1)
    meetings=Events.objects.all().filter(Start__gte=start, Start__lte=stop).order_by("-Id")
    if pIndex == '':
        pIndex = '8'
    people=Attendees.objects.filter(Eventid=pIndex).all()
    return render(request, 'tutorial/calendar.html', {"meetings": meetings,"people": people,'pIndex':pIndex})

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

def updatemeeting(token):
    # 将新会议添加到数据库中
    meetinglists=[]

    data123=get_user(token)#发送邮件

    events = get_calendar_events(token)#获取meetinginfo近两天的会议记录
    bjevents = get_bj_events(token)#获取北京会议室近两天的会议记录
    hzevents = get_hz_events(token)#获取杭州会议室近两天的会议记录
    kmevents = get_km_events(token)#获取昆明会议室近两天的会议记录
    hpyevents = get_hpy_events(token)#获取Happyroom近两天的会议记录
    njevents = get_nanj_events(token)  # 获取南京会议室近两天的会议记录
    qdevents = get_qd_events(token)  # 获取青岛会议室近两天的会议记录
    qhevents = get_qh_events(token)  # 获取情海会议室近两天的会议记录
    syevents = get_sanya_events(token)  # 获取三亚会议室近两天的会议记录
    scevents = get_sc_events(token)  # 获取四川会议室近两天的会议记录
    trnevents = get_trn_events(token)  # 获取training会议室近两天的会议记录
    vcevents = get_vc_events(token)  # 获取VideoCenter会议室近两天的会议记录
    bigevents = get_big_events(token)  # 获取VideoRoom会议室近两天的会议记录
    wlqevents = get_wlq_events(token)  # 获取乌鲁木齐近两天的会议记录
    xaevents = get_xa_events(token)  # 获取西安会议室近两天的会议记录
    meetinglists.append(events)
    meetinglists.append(bjevents)
    meetinglists.append(hzevents)
    meetinglists.append(hpyevents)
    meetinglists.append(kmevents)
    meetinglists.append(njevents)
    meetinglists.append(qdevents)
    meetinglists.append(qhevents)
    meetinglists.append(syevents)
    meetinglists.append(scevents)
    meetinglists.append(trnevents)
    meetinglists.append(vcevents)
    meetinglists.append(bigevents)
    meetinglists.append(wlqevents)
    meetinglists.append(xaevents)
    for i in range(0,len(meetinglists)):
        try:
            newevents(meetinglists[i], token)
        except Exception as e:
            print(e)
    #if (wlqevents['value']):
    #    for event in wlqevents['value']:
    #        print(event)
def insert(geteventid,name,address,time):
    lists = Attendees.objects.filter(Eventid=geteventid, Address=address).all()
    if (len(lists) != 0):
        # print('已存在该数据！')
        users = User.objects.filter(Address=address).all()
        if (len(users) == 0):
            User.objects.create(Name=name, Address=address, Passwd="ames@12345")
        else:
            if (name != users[0].Name):
                for user in users:
                    User.objects.filter(Address=address).update(Name=name)
    else:
        # print('这是一个新数据！')
        if (address != "amemeetinginfo@analogic.com" and
                    name != "MeetingInfo, Ames"):
            Attendees.objects.create(Eventid=geteventid, Name=name,
                                     Address=address, Isattend='0', Meetingtime=time)
            users = User.objects.filter(Address=address).all()
            if (len(users) == 0):
                User.objects.create(Name=name, Address=address)

def newevents(events,token):
    graph_client1 = OAuth2Session(token=token)
    graph_client1.headers = json.dumps(
        {'Content-Type': 'application/json', 'User-Agent': 'python-requests/2.22.0', 'Accept-Encoding': 'gzip, deflate',
         'Accept': '*/*', 'Connection': 'keep-alive'})
    if events:
        if(events['value']):
            for event in events['value']:
                #print(event['subject'])
                # if (event['organizer']['emailAddress']['name']=="ConfRm, Shanghai Video Room (Auto)"):
                #     print(event)
                strs = event['location']['displayName']
                s = strs.split()
                if (len(s) == 3):
                    if (s[2] == "Qinghai(Auto)"):
                        location = "Qinghai"
                elif (len(s) == 4):
                    if (s[3] == "(Auto)"):
                        location = s[2]
                    elif (s[3] == "Center"):
                        location = s[3]
                elif (len(s) == 5):
                    if (s[2] == "Happy" or s[2] == "Video"):
                        location = s[2]+" "+s[3]
                else:
                    location = strs#将得到的会议信息中的location信息进行过滤
                o = datetime.timedelta(hours=8)
                if(location=="Happy Room"):
                    pass
                    #print(event["attendees"])
                event['start']['dateTime'] = dateutil.parser.parse(event['start']['dateTime'])+o  # 修改会议开始时间格式，将utc时间+8
                event['end']['dateTime'] = dateutil.parser.parse(event['end']['dateTime'])+o  # 修改会议结束时间格式，将utc时间+8
                if(event['isCancelled']):#如果会议取消查询数据库中是否有该会议，如果有就删除
                    listcancel = Events.objects.filter(Graphid=event['id']).all()
                    if(len(listcancel)):
                        for cancel in listcancel:
                            Events.objects.filter(Id=cancel.Id).delete()
                            Attendees.objects.filter(Eventid=cancel.Id).delete()
                            #print("123")
                else:
                    lists1 = Events.objects.filter(Graphid=event['id']).all()#查找数据库中是否有相同数据
                    if (len(lists1)):
                        if(lists1[0].Subject!=event['subject']):
                            Events.objects.filter(Id=lists1[0].Id).update(Subject=event['subject'])
                        if (lists1[0].Start != event['start']['dateTime']):
                            Events.objects.filter(Id=lists1[0].Id).update(Start=event['start']['dateTime'])
                            Attendees.objects.filter(Eventid=lists1[0].Id).update(Meetingtime=event['start']['dateTime'])
                        if (lists1[0].End != event['end']['dateTime']):
                            Events.objects.filter(Id=lists1[0].Id).update(End=event['end']['dateTime'])
                        if (lists1[0].Location != location):
                            Events.objects.filter(Id=lists1[0].Id).update(Location=location)
                        #print('已存在该会议！'+event['subject'])
                    else:
                        print('这是一个新会议！'+event['subject'])
                        Events.objects.create(Subject=event['subject'], Organizer=event['organizer']['emailAddress']['name'],Organizeraddress=event['organizer']['emailAddress']['address'],
                                              Start=event['start']['dateTime'],End=event['end']['dateTime'], Location=location,Graphid=event['id'])
                    eventid = Events.objects.filter(Graphid=event['id']).all()
                    for attendee in event['attendees']:
                        #print(attendee['emailAddress']['address'])
                        mail = graph_client1.get("{0}/groups?$filter=startswith(mail,'".format(graph_url)+attendee['emailAddress']['address']+"')").json()["value"]
                        if (len(mail)):#判断收件人是否为组
                            members = graph_client1.get("{0}/groups/".format(graph_url) + mail[0]["id"] + "/members").json()["value"]
                            #print(members)
                            for member in members:
                                if (member["@odata.type"]=="#microsoft.graph.group"):#判断组中成员是组还是个人
                                    mail2 = graph_client1.get(
                                    "{0}/groups?$filter=startswith(mail,'".format(graph_url) + member["mail"] + "')").json()["value"]
                                    members2 = graph_client1.get("{0}/groups/".format(graph_url) + mail2[0]["id"] + "/members").json()["value"]
                                    for member2 in members2:
                                        insert(eventid[0].Id, member2["displayName"], member2["mail"], event['start']['dateTime'])
                                else:
                                    insert(eventid[0].Id, member["displayName"], member["mail"], event['start']['dateTime'])
                        else:
                            if(attendee['status']['response']=="declined"):#如果用户拒绝该会议
                                attlist=Attendees.objects.filter(Eventid=eventid[0].Id,Address=attendee['emailAddress']['address']).all()
                                if(len(attlist)!=0):
                                    for declined in attlist:
                                        Attendees.objects.filter(Id=declined.Id).delete()
                            else:
                                lists = Attendees.objects.filter(Eventid=eventid[0].Id, Address=attendee['emailAddress']['address']).all()
                                if (len(lists) != 0):
                                    #print('已存在该数据！')
                                    users=User.objects.filter(Address=attendee['emailAddress']['address']).all()
                                    if(len(users)==0):
                                        User.objects.create( Name=attendee['emailAddress']['name'],Address=attendee['emailAddress']['address'],Passwd="ames@12345")
                                    else:
                                        for user in users:
                                            User.objects.filter(Address=attendee['emailAddress']['address']).update(Name=attendee['emailAddress']['name'])
                                else:
                                    #print('这是一个新数据！')
                                    #if(event['subject']=="change"):
                                    if(len(event['locations'])!=0):
                                        if(attendee['emailAddress']['address']!="amemeetinginfo@analogic.com" and attendee['emailAddress']['name']!="MeetingInfo, Ames" and attendee['emailAddress']['address']!=event['locations'][0]['uniqueId']):
                                            Attendees.objects.create(Eventid=eventid[0].Id, Name=attendee['emailAddress']['name'],
                                                                 Address=attendee['emailAddress']['address'],Isattend='0',Meetingtime=event['start']['dateTime'])
                                            users = User.objects.filter(Address=attendee['emailAddress']['address']).all()
                                            if (len(users) == 0):
                                                User.objects.create(Name=attendee['emailAddress']['name'],Address=attendee['emailAddress']['address'])
                                    else:
                                        if (attendee['emailAddress']['address'] != "amemeetinginfo@analogic.com" and
                                                    attendee['emailAddress']['name'] != "MeetingInfo, Ames"):
                                            Attendees.objects.create(Eventid=eventid[0].Id,Name=attendee['emailAddress']['name'],
                                                                     Address=attendee['emailAddress']['address'],Isattend='0',
                                                                     Meetingtime=event['start']['dateTime'])
                                            users = User.objects.filter(Address=attendee['emailAddress']['address']).all()
                                            if (len(users) == 0):
                                                User.objects.create(Name=attendee['emailAddress']['name'],Address=attendee['emailAddress']['address'])
def Monitor():
    try:
        import time
        acctoken = gettoken()
        updatemeeting(acctoken)
        #time.sleep(10)
        #print("time sleeped")
    except Exception as e:
        print(e)