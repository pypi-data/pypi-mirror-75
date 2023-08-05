from xingapi.api.xasession import Session
from xingapi.api.xaquery import Query
from xingapi.api.xareal import Real, RealManager

from xingapi.app.stockcode import StockCode
from xingapi.app.stockinfo import StockInfo
from xingapi.app.stockreal import StockReal

class App:

    def __init__(self, login_txt=None, *login_args, **login_kwargs):
        """app instance 시작            
        """

        self.Session = Session
        self.Query = Query
        self.RealManager = RealManager

        self.session = self.Session()
        self.query = self.Query()
        self.real = self.RealManager()

        if login_txt:
            self.login_from_txt(login_txt)
        elif login_args:
            self.login(*login_args)
        elif login_kwargs:
            self.login(**login_kwargs)

        self.종목코드   = StockCode(app=self)
        self.종목정보   = StockInfo(app=self)
        self.실시간     = StockReal(app=self)

    def login(self, id, pw, cert):
        self.session.login(id, pw, cert)

    def login_from_txt(self, txt_path):
        with open(txt_path) as f:
            id, pw, cert = f.read().split()
        self.login(id, pw, cert)