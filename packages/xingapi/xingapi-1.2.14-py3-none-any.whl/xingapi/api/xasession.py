import pythoncom
import win32com.client
from xingapi.api.log import Logger
from xingapi.api.xaquery import Query

log = Logger(__name__)

class _SessionEvents:
    def __init__(self):
        self.reset()

    def reset(self):
        self.code = -1
        self.msg = '세션 초기화'

    def OnLogin(self, code, msg):
        self.code = str(code)
        self.msg = str(msg)

    def OnDisconnect(self):
        self.reset()

class Session:
    def __init__(self):
        self.com = win32com.client.DispatchWithEvents("XA_Session.XASession", _SessionEvents)
        
    def login(self, id, pwd, cert):
        self.com.reset()
        self.com.ConnectServer("hts.ebestsec.co.kr", 20001)
        self.com.Login(id, pwd, cert, 0, False)
        while self.com.code == -1:
            pythoncom.PumpWaitingMessages()
        if self.com.code == "0000":
            return True
        else:
            return False

    def logout(self):
        self.com.reset()
        self.com.DisconnectServer()
        if not self.is_connected:
            log.info(f'로그아웃')
            return True
        else:
            return False

    @property
    def is_connected(self):
        return self.com.IsConnected()

    @property
    def status(self):
        return self.com.code, self.com.msg

    @property
    def now(self):
        date, time = Query("t0167")()['t0167OutBlock'].values[0]
        return dict(date=date, time=time[:6])

    @property
    def date(self):
        return self.now['date']

    @property
    def time(self):
        return self.now['time']

    @property
    def accounts(self):
        num_acc = self.com.GetAccountListCount()
        accounts = {}
        for i in range(num_acc):
            account = {}
            account['계좌번호'] = self.com.GetAccountList(i)
            account['계좌이름'] = self.com.GetAccountName(i)
            account['계좌별명'] = self.com.GetAcctNickname(i)
            account['계좌상세'] = self.com.GetAcctDetailName(i)
            accounts[i] = account
        return accounts