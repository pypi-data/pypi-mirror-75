# -*- coding: utf-8 -*-
import logging.handlers

class Setting:
    """로거 세팅 클래스
        ::
            Setting.LEVEL = logging.INFO # INFO 이상만 로그를 작성
    """
    LEVEL         = logging.INFO
    FILENAME      = "xingapi.log" 
    MAX_BYTES     = 10 * 1024 * 1024
    BACKUP_COUNT  = 10
    FORMAT        = "%(asctime)s[%(levelname)s|%(name)s,%(lineno)s] %(message)s"

def Logger(name):
    """파일 로그 클래스
        :param name: 로그 이름
        :type name: str
        :return: 로거 인스턴스
        ::
            logger = Logger(__name__)
            logger.info('info 입니다')          
    """

    # 로거 & 포매터 & 핸들러 생성
    logger          = logging.getLogger(name)
    formatter       = logging.Formatter(Setting.FORMAT)
    streamHandler   = logging.StreamHandler()
    fileHandler     = logging.handlers.RotatingFileHandler(
        filename    = Setting.FILENAME, 
        maxBytes    = Setting.MAX_BYTES, 
        backupCount = Setting.BACKUP_COUNT)
    
    # 핸들러 & 포매터 결합
    streamHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    # 로거 & 핸들러 결합
    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)

     # 로거 레벨 설정
    logger.setLevel(Setting.LEVEL)

    return logger