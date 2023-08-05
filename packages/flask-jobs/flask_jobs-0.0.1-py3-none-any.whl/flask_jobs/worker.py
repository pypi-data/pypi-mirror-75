import datetime
import threading
from dictabase import FindAll, FindOne
from .jobs import Job, RepeatingJob


class Worker:
    def __init__(self):
        self._timer = None
        self._lock = threading.Lock()

        self._repeatJobsRefreshed = False

    def Refresh(self):
        '''
        Updates the self._timer
        :return:
        '''
        with self._lock:
            if self._timer:
                if self._timer.is_alive():
                    self._timer.cancel()
                else:
                    self._timer = None

            # At startup, the repeating jobs must be refreshed once
            if self._repeatJobsRefreshed is False:
                try:
                    for job in FindAll(RepeatingJob):
                        job.Refresh()
                    self._repeatJobsRefreshed = True
                except Exception as e:
                    print('Error refreshing RepeatJobs', e)

            nextJobList = list(FindAll(Job, status='pending', _orderBy='dt', _limit=1))
            nextJobList += list(FindAll(RepeatingJob, status='pending', _orderBy='dt', _limit=1))

            nextJobList = sorted(nextJobList, key=lambda d: d['dt'])

            if len(nextJobList) > 0:
                nextJob = nextJobList[0]

                nextJobDT = nextJob['dt']  # UTC
                nowDT = datetime.datetime.utcnow()
                delta = (nextJobDT - nowDT).total_seconds()
                if delta < 0:
                    delta = 0
                self._timer = threading.Timer(delta, self._DoOneJob, args=[type(nextJob), nextJob['id']])
                self._timer.start()

            else:
                self._timer = None

    def _DoOneJob(self, typ, jobID):
        ret = None

        with self._lock:
            job = FindOne(typ, id=jobID)
            if job['status'] == 'pending':
                ret = job.DoJob()

        self.Refresh()
        return ret
