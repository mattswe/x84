import msgbase # FIX, work on msging...
import ini
from strutils import chompn, asctime, ansilen, chkseq, seqc, maxanswidth
from dbproxy import DBProxy
from userbase import User, getuser, finduser, userexist, authuser, listusers
from session import getsession, logger
from fileutils import abspath, fopen, ropen
from output import echo, oflush, delay
from input import getch, getpos, readline, readlineevent
from ansiwin import AnsiWindow
from editor import HorizEditor
from leftright import LeftRightClass, YesNoClass, PrevNextClass
from lightwin import LightClass
from pager import ParaClass
from sauce import SAUCE

__all__ = [
    'logger',
    'maxanswidth',
    'chompn',
    'asctime',
    'ansilen',
    'chkseq',
    'seqc',
    'DBProxy',
    'User',
    'finduser',
    'userexist',
    'authuser',
    'getuser',
    'listusers',
    'ini',
    'AnsiWindow',
    'HorizEditor',
    'LeftRightClass',
    'YesNoClass',
    'PrevNextClass',
    'LightClass',
    'ParaClass',
    'disconnect',
    'goto',
    'gosub',
    'sendevent',
    'broadcastevent',
    'readevent',
    'flushevent',
    'flushevents',
    'getsession',
    'getterminal',
    'gethandle',
    'getch',
    'getpos',
    'delay',
    'oflush',
    'echo',
    'abspath',
    'fopen',
    'ropen',
    'showfile',
    'readline',
    'readlineevent',
    'msgbase',
    'SAUCE',
]

def getterminal():
  return getsession().terminal


def gethandle():
  return getsession().handle


def disconnect():
  import exception as exception
  raise exception.Disconnect('disconnect')


def goto(*arg):
  import exception
  raise exception.Goto(arg)


def gosub(*arg):
  return getsession().runscript(*(arg[0],) + arg[1:])


def sendevent(pid, event, data):
  return getsession().send_event('event', (pid, event, data))


def broadcastevent(event, data):
  return getsession().send_event('global', (getsession().pid, event, data))


def readevent(events = ['input'], timeout = None):
  return getsession().read_event(events, timeout)


def flushevent(event = 'input', timeout = -1):
  return getsession().flush_event(event, timeout)


def flushevents(events = ['input'], timeout = -1):
  return [flushevent(e, timeout) for e in events]


def loginuser(handle):
  import time as time
  u = userbase.getuser(handle)
  u.calls += 1
  u.lastcall = time.time()


def showfile(filename, bps=0, pause=0.1, cleansauce=True):
  # glob magic
  fobj = ropen(filename, 'rb') \
    if '*' in filename or '?' in filename \
      else fopen(filename, 'rb')

  data = chompn(str(SAUCE(fobj)) if cleansauce else fobj.read())

  if 0 == bps:
    echo (data)
    echo (getterminal().normal)
    return

  # display at a timed speed, re-expereince the pace of 9600bps ...
  cpp = (float(bps)/8) *pause
  for n, ch in enumerate(data):
    if 0 == (n % cpp):
      getsession().read_event(events=['input'], timeout=pause)
    echo (ch)