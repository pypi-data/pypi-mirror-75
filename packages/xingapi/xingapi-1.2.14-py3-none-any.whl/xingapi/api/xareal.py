import pythoncom
import win32com.client
import pandas as pd
from queue import Queue
from threading import Thread
from xingapi.api.res import Res
from xingapi.api.log import Logger


log = Logger(__name__)

class _RealEvents:
    def __init__(self):
        self.queue = None

    def OnReceiveRealData(self, trcode):
        log.debug(f'{trcode}')
        self.res = Res(trcode)
        data = {}
        for key, label in self.res.blocks['OutBlock'].items():
            data[label] = self.GetFieldData("OutBlock", key)
        df = pd.DataFrame([data])
        self.queue.put((trcode, df))


class Real:
    def __init__(self, trcode, queue):
        self.com = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", _RealEvents)
        self.res = Res(trcode)
        self.com.LoadFromResFile(self.res.path)
        self.com.queue = queue

    def set_inputs(self, block_name, **kwargs):
        for k, v in kwargs.items():
            self.com.SetFieldData(block_name, k, v)
    
    def advise(self, **input_kwargs):
        self.set_inputs('InBlock', **input_kwargs)
        self.com.AdviseRealData()
        return self

    def run(self):
        while True:
            pythoncom.PumpWaitingMessages()

    def unadvise(self):
        self.com.UnadviseRealData()
        return self

class RealManager:
    def add(self, trcode, callback=None):

        if not callback:
            callback = print

        def target(queue):
            while True:
                data = queue.get()
                callback(data)

        queue = Queue()
        real = Real(trcode, queue)
        th = Thread(target=target, args=(queue,), daemon=True)
        th.start()
        return real
