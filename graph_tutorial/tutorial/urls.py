from django.conf.urls import url

from . import views
from apscheduler.scheduler import Scheduler
from tutorial.views import  Monitor
sched = Scheduler()  # 实例化，固定格式


@sched.interval_schedule(seconds=120)  # 装饰器，seconds=120意思为该函数为2分钟运行一次
def mytask():
  Monitor()

sched.start()  # 启动该脚本

urlpatterns = [
  # /tutorial

  url('signin', views.sign_in, name='signin'),
  url('callback', views.callback, name='callback'),
  url('signout', views.sign_out, name='signout'),
  url(r"^calendar(?P<pIndex>[0-9]*)/$", views.calendar, name='calendar'),
url('', views.home, name='home'),
]