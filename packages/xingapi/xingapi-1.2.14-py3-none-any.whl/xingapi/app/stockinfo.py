from xingapi.api.xasession import Session
from xingapi.api.xaquery import Query
from xingapi.api.xareal import Real, RealManager

class StockInfo:
    def __init__(self, app=None):
        self.app = app
        self._종목코드 = None
    
    def __call__(self, 종목):
        if self.app:
            if 종목 in self.app.종목코드.전체:
                self._종목코드 = 종목
            else:
                self._종목코드 = self.app.종목코드.종목명으로검색(종목)
        else:
            self._종목코드 = 종목
        return self
    
    @property
    def 현재호가(self):
        return Query('t1101')(shcode=self._종목코드)['t1101OutBlock']

    @property
    def 현재시세(self):
        return Query('t1102')(shcode=self._종목코드)['t1102OutBlock']

    def 체결(self, 구분=0, 종료시간='', 개수=-1):
        """체결 조회

            구분(int): 0:당일 1: 전일
            종료시간(str): HHMMSS 형식
            개수: -1 끝까지
        """
        return self.t1310(daybg=구분, endtime=종료시간, cnt=개수)

    def 호가(self, 작업구분=0):
        """분별호가 조회

            작업구분(int, str): 0:30초 1:1분 2:3분 3:5분 4:10분 5:30분 6:60분
        """
        return Query('t1471').call(shcode=self._종목코드, gubun=작업구분, cnt=500).next(keypairs={'time':'time'})['t1471OutBlock1']

    def 분봉(self, 작업구분=0):
        """분별주가/체결 조회

            작업구분(int, str): 0:30초 1:1분 2:3분 3:5분 4:10분 5:30분 6:60분
        """
        return Query('t1302')(shcode=self._종목코드, gubun=작업구분, cnt=900)['t1302OutBlock1']

    def 일봉(self, 개수=-1):
        """일봉

            개수(int): -1: 끝까지, N: N개까지
        """
        return self.t1305(dwmcode=1, cnt=개수)

    def 주봉(self, 개수=-1):
        """주봉
        
            개수(int): -1: 끝까지, N: N개까지
        """
        return self.t1305(dwmcode=2, cnt=개수)

    def 월봉(self, 개수=-1):
        """월봉
        
            개수(int): -1: 끝까지, N: N개까지
        """
        return self.t1305(dwmcode=3, cnt=개수)
    
    def 분별체결강도(self, 개수=-1):
        """분별체결강도
        
            개수(int): -1: 끝까지, N: N개까지
        """
        return self.t1475(vptype=0, datacnt=개수, gubun=1)
    
    def 일별체결강도(self, 개수=-1):
        """일별체결강도
        
            개수(int): -1: 끝까지, N: N개까지
        """
        return self.t1475(vptype=1, datacnt=개수, gubun=1)

    def 매물대(self, 구분=1):
        """가격대별 매매비중조회

            구분: 당일:1 전일:2 당일+전일:3
        """
        return Query('t1449')(shcode=self._종목코드, dategb=구분)['t1449OutBlock1']

    def 신호(self, 개수=20):
        """신호조회

           개수(int): -1: 끝까지, N: N개까지
        """
        return self.t1809(cnt=개수)
        
    @property
    def 오늘(self):
        """오늘 날짜를 반환. STR, 형식(YYYYMMDD)
        """
        return Query('t0167')()['t0167OutBlock']['일자(YYYYMMDD)'][0]

    @property
    def 테마(self):
        """소속된 테마
        """
        return Query('t1532')(shcode=self._종목코드)['t1532OutBlock']

    def 틱차트(self, N틱=1, 시작일=None, 종료일=None):
        """
            N틱: N개를 1개로. ex) N틱봉
            시작일(str): YYYYMMDD형식, None일경우 오늘날짜
            종료일(str): YYYYMMDD형식, None일경우 오늘날짜
        """
        if not 시작일: 시작일 = self.오늘
        if not 종료일: 종료일 = self.오늘
        return self.t8411(n=N틱, sdate=시작일, edate=종료일)
        
    def 분차트(self, N분=1, 시작일=None, 종료일=None):
        """
            N분: N개를 1개로. ex) N분봉
            시작일(str): YYYYMMDD형식, None일경우 오늘날짜
            종료일(str): YYYYMMDD형식, None일경우 오늘날짜
        """
        if not 시작일: 시작일 = self.오늘
        if not 종료일: 종료일 = self.오늘
        return self.t8412(n=N분, sdate=시작일, edate=종료일)
    
    def 일차트(self, 시작일=None, 종료일=None):
        """
            시작일(str): YYYYMMDD형식, None일경우 오늘날짜
            종료일(str): YYYYMMDD형식, None일경우 오늘날짜
        """
        if not 시작일: 시작일 = self.오늘
        if not 종료일: 종료일 = self.오늘
        return self.t8413(gubun=2, sdate=시작일, edate=종료일)

    def 주차트(self, 시작일=None, 종료일=None):
        """
            시작일(str): YYYYMMDD형식, None일경우 오늘날짜
            종료일(str): YYYYMMDD형식, None일경우 오늘날짜
        """
        if not 시작일: 시작일 = self.오늘
        if not 종료일: 종료일 = self.오늘
        return self.t8413(gubun=3, sdate=시작일, edate=종료일)

    def 월차트(self, 시작일=None, 종료일=None):
        """

            시작일(str): YYYYMMDD형식, None일경우 오늘날짜
            종료일(str): YYYYMMDD형식, None일경우 오늘날짜
        """
        if not 시작일: 시작일 = self.오늘
        if not 종료일: 종료일 = self.오늘
        return self.t8413(gubun=4, sdate=시작일, edate=종료일)

    def t8411(self, n, sdate, edate):
        return Query('t8411').call(
            shcode=self._종목코드,
            ncnt=n,
            qrycnt=500,
            sdate=sdate,
            edate=edate,
            comp_yn='N',
        ).next(
            keypairs={'cts_date':'cts_date','cts_time':'cts_time'}
        )['t8411OutBlock1']

    def t8412(self, n, sdate, edate):
        return Query('t8412').call(
            shcode=self._종목코드,
            ncnt=n,
            qrycnt=500,
            sdate=sdate,
            edate=edate,
            comp_yn='N',
            
        ).next(
            keypairs={'cts_date':'cts_date','cts_time':'cts_time'}
        )['t8412OutBlock1']

    def t8413(self, gubun, sdate, edate):
        return Query('t8413').call(
            shcode=self._종목코드,
            gubun=0,
            qrycnt=500,
            sdate=sdate,
            edate=edate,
            comp_yn='N',
        ).next(
            keypairs={'cts_date':'cts_date'}
        )['t8413OutBlock1']
    

    def t1305(self, dwmcode, cnt):
        """기간별주가조회
        """
        if cnt>0:
            total = cnt//300
        else:
            total = -1 # 끝까지

        return Query('t1305').call(
            shcode=self._종목코드, 
            dwmcode=dwmcode, 
            cnt=300,
        ).next(
            keypairs={'date':'date'}, 
            total=total,
        )['t1305OutBlock1'].head(cnt)
    
    def t1475(self, vptype, datacnt, gubun):
        """체결강도추이

            vptype(int/str): 0:시간별 1:일별구분
            datacnt(int): 개수
            gubun: 0누적거래량/1체결량(분별)
        """
        if datacnt>0:
            total = datacnt//1000
        else:
            total = -1 # 끝까지

        return Query('t1475').call(
            shcode=self._종목코드, 
            vptype=vptype, 
            datacnt=1000,
        ).next(
            keypairs={'date':'date'}, 
            total=total
        )['t1475OutBlock1'].head(datacnt)

    def t1809(self, cnt):
        if cnt>0:
            total = cnt//20
        else:
            total = -1 # 끝까지

        return Query('t1809').call(
            jmcode=self._종목코드,
            gubun='0', 
            jmGb='0',
        ).next(
            keypairs={'cts':'cts'},
            total=total,
        )['t1809OutBlock1'].head(cnt)

    def t1310(self, daybg, endtime, cnt):
        if cnt>0:
            total = cnt//20
        else:
            total = -1 # 끝까지
        
        return Query('t1310').call(
            shcode=self._종목코드,
            daygb=daybg,
            timegb=1,
            endtime=endtime,
        ).next(
            keypairs={'cts_time':'cts_time'},
            total=total,
        )['t1310OutBlock1'].head(cnt)
        
    def __repr__(self):
        return 'Object from StockInfo Class'

