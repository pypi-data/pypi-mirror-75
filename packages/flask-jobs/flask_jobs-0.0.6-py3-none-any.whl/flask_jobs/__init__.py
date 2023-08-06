'''
All datetimes are in UTC
'''
import datetime
import pickle
from dictabase import RegisterDBURI as dictabase_RegisterDBURI
from dictabase import (
    New, FindAll, FindOne,

)
from .jobs import Job
from .worker import Worker

global _worker
_worker = None


def init_app(app=None):
    global _worker

    if app:
        dictabase_RegisterDBURI(app.config['DATABASE_URL'])
    else:
        dictabase_RegisterDBURI()

    _worker = Worker()
    _worker.Refresh()


def AddJob(func, args=(), kwargs={}, name=None):
    '''
    Schedule a job to be run ASAP
    :param func: callable
    :param args: tuple
    :param kwargs: dict
    :return:
    '''
    newJob = New(
        Job,
        dt=datetime.datetime.utcnow(),
        func=pickle.dumps(func),
        args=pickle.dumps(args),
        kwargs=pickle.dumps(kwargs),
        kind='asap',
        name=name,
    )
    if _worker:
        _worker.Refresh()
    return newJob


def ScheduleJob(dt, func, args=(), kwargs={}, name=None):
    '''
    Schedule a job to be run once at a future time
    :param dt: datetime
    :param func: callable
    :param args: tuple
    :param kwargs: dict
    :return:
    '''
    newJob = New(
        Job,
        dt=dt,
        func=pickle.dumps(func),
        args=pickle.dumps(args),
        kwargs=pickle.dumps(kwargs),
        kind='schedule',
        name=name,
    )
    # print('newJob=', newJob)
    if _worker:
        _worker.Refresh()
    return newJob


def RepeatJob(startDT=None, func=None, args=(), kwargs={}, name=None, **k):
    '''
    :param func: callable
    :param args: tuple
    :param kwargs: dict
    :param k: weeks, days, hours, minutes, seconds (anything supported by datetime.timedelta.__init__
    :return:
    '''
    if len(k) == 0:
        raise KeyError('You must pass one of the following kwargs (weeks, days, hours, minutes, seconds)')
    startDT = startDT or datetime.datetime.utcnow()

    newJob = New(
        Job,
        startDT=startDT,
        dt=startDT,
        func=pickle.dumps(func),
        args=pickle.dumps(args),
        kwargs=pickle.dumps(kwargs),
        kind='repeat',
        deltaKwargs=k,
        name=name,
    )
    # print('newJob=', newJob)
    if _worker:
        _worker.Refresh()
    return newJob


def GetJobs():
    for job in FindAll(Job, status='pending'):
        yield job


def GetJob(jobID):
    return FindOne(Job, id=jobID)


if _worker:
    _worker.Refresh()
