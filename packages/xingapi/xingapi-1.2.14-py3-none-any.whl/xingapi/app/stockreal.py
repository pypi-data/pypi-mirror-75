from xingapi.api.xasession import Session
from xingapi.api.xaquery import Query
from xingapi.api.xareal import Real, RealManager

class StockReal:
    def __init__(self, app=None):
        self.app = app
        self.real = RealManager()
        self.jobs = []

    def 뉴스(self, callback=print):
        job = self.real.add('NWS', callback=callback).advise(nwcode='NWS001')
        self.jobs.append(job)
        return job
    
    def 코스닥체결(self, callback=print, shcodes=[]):
        job = self.real.add('K3_', callback=callback)
        if not isinstance(shcodes, list):
            shcodes = [shcodes]
        for shcode in shcodes:
            job.advise(shcode=shcode)
        self.jobs.append(job)
        return job

    def 코스피체결(self, callback=print, shcodes=[]):
        job = self.real.add('S3_', callback=callback)
        if not isinstance(shcodes, list):
            shcodes = [shcodes]
        for shcode in shcodes:
            job.advise(shcode=shcode)
        self.jobs.append(job)
        return job

    def 전종목체결(self, callback, num_per_thread=10):
        batchs = [self.app.종목코드.코스피[i:i + num_per_thread] for i in range(0, len(self.app.종목코드.코스피), num_per_thread)]
        for shcodes in batchs:
            self.코스피체결(callback, shcodes)
        batchs = [self.app.종목코드.코스닥[i:i + num_per_thread] for i in range(0, len(self.app.종목코드.코스닥), num_per_thread)]
        for shcodes in batchs:
            self.코스닥체결(callback, shcodes)

    def 시작(self):
        for job in self.jobs:
            job.run()
