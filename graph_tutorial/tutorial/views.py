from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from tutorial.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from tutorial.graph_helper import get_user, get_calendar_events, get_xa_events, get_big_events, \
    get_wlq_events, get_hpy_events
import dateutil.parser
import re

from tutorial.models import Events, Attendees, User


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
  # Get the sign-in URL
  sign_in_url, state = get_sign_in_url()
  # Save the expected state so we can validate in the callback
  request.session['auth_state'] = state
  # Redirect to the Azure sign-in page
  return HttpResponseRedirect(sign_in_url)

def callback(request):
  # Get the state saved in session
  expected_state = request.session.pop('auth_state', '')
  # Make the token request
  token = get_token_from_code(request.get_full_path(), expected_state)

  # Get the user's profile
  user = get_user(token)

  # Save token and user
  store_token(request, token)
  store_user(request, user)
  #将新会议添加到数据库中
  #updatemeeting(request)
  return HttpResponseRedirect(reverse('home'))

def sign_out(request):
  # Clear out the user and token
  remove_user_and_token(request)

  return HttpResponseRedirect(reverse('home'))

def calendar(request,pIndex):
    # 将新会议添加到数据库中
    updatemeeting(request)
    meetings=Events.objects.all().order_by("-Id")
    if pIndex == '':
        pIndex = '8'
    people=Attendees.objects.filter(Eventid=pIndex).all()
    return render(request, 'tutorial/calendar.html', {"meetings": meetings,"people": people,'pIndex':pIndex})
def updatemeeting(request):
    # 将新会议添加到数据库中
    context = initialize_context(request)
    token = get_token(request)
    events = get_calendar_events(token)#获取meetinginfo近三天的会议记录
    wlqevents = get_wlq_events(token)#获取乌鲁木齐会议室近三天的会议记录
    bigevents = get_big_events(token)#获取VideoRoom会议室近三天的会议记录
    xaevents = get_xa_events(token)#获取西安会议室近三天的会议记录
    hpyevents = get_hpy_events(token)
    newevents(events)
    newevents(xaevents)
    newevents(wlqevents)
    newevents(bigevents)
    #newevents(hpyevents)
def newevents(events):
    if events:
        for event in events['value']:
            # if (event['organizer']['emailAddress']['name']=="ConfRm, Shanghai Video Room (Auto)"):
            #     print(event)
            str = event['location']['displayName']
            str1 = re.findall(r'[^ConfRm, Shanghai ].*', str)
            if (len(str1)):
                str2 = re.findall(r'(.+ ?).(Auto)', str1[0])
                if (len(str2)):
                    location = str2[0][0]
                else:
                    location = str1[0]
            else:
                location = str#将得到的会议信息中的location信息进行过滤
            if(event['isCancelled']):#如果会议取消查询数据库中是否有该会议，如果有就删除
                listcancel = Events.objects.filter(Subject=event['subject'],
                                               Organizer=event['organizer']['emailAddress']['name'],
                                               Start=event['start']['dateTime'],
                                               End__gte=event['start']['dateTime'],
                                               Location=location).all()
                if(len(listcancel)):
                    for cancel in listcancel:
                        Events.objects.filter(Id=cancel.Id).delete()
                        Attendees.objects.filter(Eventid=cancel.Id).delete()
                        #print("123")
            else:
                event['start']['dateTime'] = dateutil.parser.parse(event['start']['dateTime'])#修改会议开始时间格式
                event['end']['dateTime'] = dateutil.parser.parse(event['end']['dateTime'])#修改会议结束时间格式
                lists1 = Events.objects.filter(Organizer=event['organizer']['emailAddress']['name'],
                                               Start=event['start']['dateTime'],
                                               End__gte=event['start']['dateTime'],
                                               Location=location).all()#查找数据库中是否有相同数据
                if (len(lists1) != 0):
                    print('已存在该会议！')
                else:
                    print('这是一个新会议！')
                    Events.objects.create(Subject=event['subject'], Organizer=event['organizer']['emailAddress']['name'],Organizeraddress=event['organizer']['emailAddress']['address'],
                                          Start=event['start']['dateTime'],End=event['end']['dateTime'], Location=location)
                eventid = Events.objects.filter(Organizer=event['organizer']['emailAddress']['name'],
                                                Start=event['start']['dateTime'],
                                                End=event['end']['dateTime'],
                                                Location=location).all()
                for attendee in event['attendees']:
                    if(attendee['status']['response']=="declined"):#如果用户拒绝该会议
                        attlist=Attendees.objects.filter(Eventid=eventid[0].Id,Address=attendee['emailAddress']['address']).all()
                        if(len(attlist)!=0):
                            for declined in attlist:
                                Attendees.objects.filter(Id=declined.Id).delete()
                    else:
                        lists = Attendees.objects.filter(Eventid=eventid[0].Id, Address=attendee['emailAddress']['address']).all()
                        if (len(lists) != 0):
                            print('已存在该数据！')
                            users=User.objects.filter(Address=attendee['emailAddress']['address']).all()
                            if(len(users)==0):
                                User.objects.create( Name=attendee['emailAddress']['name'],Address=attendee['emailAddress']['address'])
                            else:
                                for user in users:
                                    User.objects.filter(Address=attendee['emailAddress']['address']).update(Name=attendee['emailAddress']['name'])
                        else:
                            print('这是一个新数据！')
                            if(attendee['emailAddress']['address']!="amemeetinginfo@analogic.com"):
                                Attendees.objects.create(Eventid=eventid[0].Id, Name=attendee['emailAddress']['name'],
                                                     Address=attendee['emailAddress']['address'],Isattend='0',Meetingtime=event['start']['dateTime'])
                                users = User.objects.filter(Address=attendee['emailAddress']['address']).all()
                                if (len(users) == 0):
                                    User.objects.create(Name=attendee['emailAddress']['name'],Address=attendee['emailAddress']['address'])