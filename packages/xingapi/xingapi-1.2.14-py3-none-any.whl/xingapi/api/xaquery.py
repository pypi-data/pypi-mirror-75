import time
import pandas as pd
import pythoncom
import win32com.client
from datetime import timedelta
from xingapi.api.res import Res
from xingapi.api.log import Logger

log = Logger(__name__)

class _QueryEvents:
    def __init__(self):
        self.received = False

    def OnReceiveData(self, trcode):
        log.debug(f'{trcode}')
        self.received = True

    def OnReceiveMessage(self, err, code, msg):
        log.debug(f'[{code}] {err} {msg}')

class Query:
    def __init__(self, trcode=None):
        self.com = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", _QueryEvents)
        if trcode:
            self.set_trcode(trcode)

    def set_trcode(self, trcode):
        self.res = Res(trcode)
        self.com.LoadFromResFile(self.res.path)

    def __call__(self, **input_kwargs):
        return self.call(**input_kwargs).data

    def set_inputs(self, block_name, **kwargs):
        for k, v in kwargs.items():
            self.com.SetFieldData(block_name, k, 0, v)

    def get_outputs(self, block_name, *args):
        counts = self.com.GetBlockCount(block_name)
        data = []
        for i in range(counts):
            datum = {}
            for k in args:
                label = self.res.blocks[block_name][k]
                value = self.com.GetFieldData(block_name, k, i)
                datum[label] = value
            data.append(datum)
        return pd.DataFrame(data)

    def request(self, occurs=False):
        self.com.received = False
        self.com.Request(occurs)
        while not self.com.received:
            pythoncom.PumpWaitingMessages()

    def wait(self):
        delay = 1/self.com.GetTRCountPerSec(self.res.name)
        time.sleep(delay)

        limit = self.com.GetTRCountLimit(self.res.name)
        count = self.com.GetTRCountRequest(self.res.name)
        log.info(f'[{count:4}/{limit:4} 조회수/조회제한]')
        
        if count==limit:
            remaining = 600-count*delay
            start = time.time()
            log.info(f'[{count:4}/{limit:4} 조회수/조회제한] 조회제한 해제 대기')
            while True:
                elapsed = time.time()-start
                time.sleep(0.1)
                print(f'조회제한 해제까지 남은시간 {timedelta(seconds=remaining-elapsed)}', end='\r')
                if elapsed>remaining:
                    break

    def block_request(self, is_next=False, **input_kwargs):
        for block_name, block_codes in self.res.blocks.items():
            if 'InBlock' in block_name:
                self.set_inputs(block_name, **input_kwargs)
        
        self.request(is_next)
        self.wait()

        data = {}
        for block_name, block_codes in self.res.blocks.items():
            if 'OutBlock' in block_name: 
                output_args = tuple(block_codes.keys())
                block_data = self.get_outputs(block_name, *output_args)
                data[block_name] = block_data
        return data

    def call(self, **input_kwargs):
        """조회 [DevCenter 조회 버튼]

            query = xa.Query("t1310")
            data = query.call(daygb=0, timegb=1, shcode='005930').data
        """
        self.data = self.block_request(is_next=False, **input_kwargs)
        return self
    
    def nextcall(self, **input_kwargs):
        """다음조회 [DevCenter 다음조회 버튼]

            call function에서 수신한 데이터 중 
            다음조회에 필요한 항목을 추가하면 된다

            query = xa.Query("t1310")
            data = query.call(daygb=0, timegb=1, shcode='005930').nextcall(cts_time='1558080001').data
        """
        self.data = self.block_request(is_next=True, **input_kwargs)
        return self

    @property
    def isnext(self):
        return self.com.IsNext

    def next(self, keypairs, total=-1):
        """다음조회 여러번 하는것을 간편하게.

            query = xa.Query("t1302")
            data = query.call(shcode='005930', cnt=1).next(keypairs={'time':'cts_time'}, total=3)

            설명 : cts_time의 연속조회 데이터값을 time인풋필드에 넣는다
        """
        assert isinstance(keypairs, dict), 'keypairs should be dict'
        
        count=0
        next_input_kwargs = {}
        base_data = self.data
        while self.isnext:
            if count == total:
                break
            # 주어진 nextkey로 수신한 self.data에서 값을 찾는다
            for block_name, block_data in self.data.items():
                for input_key, next_key in keypairs.items():
                    next_label = self.res.blocks[block_name].get(next_key)
                    if block_name.endswith('OutBlock'):
                        next_input_kwargs[input_key] = block_data[next_label][0]

            # 연속데이터를 수신 후 base_data에 append한다
            next_data = self.nextcall(**next_input_kwargs).data
            for block_name, block_data in next_data.items():
                base_data[block_name] = base_data[block_name].append(block_data, ignore_index=True)

            count+=1
        return base_data

        