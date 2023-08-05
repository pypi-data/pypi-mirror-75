"""
typhoon.configure module
"""

from tornado.process import cpu_count


class _LogFormatter(object):
    def __init__(self, fmt, datefmt):
        self.__fmt = fmt
        self.__datefmt = datefmt

    @property
    def fmt(self) -> str:
        """
        fmt
        """
        return self.__fmt

    @fmt.setter
    def fmt(self, fmt: str) -> None:
        self.__fmt = fmt

    @property
    def datefmt(self) -> str:
        """
        datefmt
        """
        return self.__datefmt

    @datefmt.setter
    def datefmt(self, datefmt: str) -> None:
        self.__datefmt = datefmt


class _Settings(object):
    def __init__(self):
        self.__max_excutor_workers = cpu_count() * 5
        self.__convert_case = True
        self.__access_log = _LogFormatter(
            fmt='[%(asctime)s][%(traceId)s][%(levelname)s][%(process)d]%(message)s',
            datefmt='%d/%b/%Y:%H:%M:%S %z'
        )
        self.__app_log = _LogFormatter(
            fmt='{time=%(asctime)s.%(msecs)d, traceId=%(traceId)s, level=%(levelname)s, pid=%(process)d, module=%(module)s, func=%(funcName)s, line=%(lineno)d}%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.__stats_log = _LogFormatter(
            fmt='time=%(asctime)s.%(msecs)d, traceId=%(traceId)s, module=%(module)s, topic=%(topic)s, id=%(recordId)s, message=%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    @property
    def max_excutor_workers(self) -> int:
        """
        max workers of the default thread pool.
        """
        return self.__max_excutor_workers

    @max_excutor_workers.setter
    def max_excutor_workers(self, max_excutor_workers: int) -> None:
        from concurrent.futures import ThreadPoolExecutor
        from tornado.ioloop import IOLoop
        executor = ThreadPoolExecutor(max_workers=max_excutor_workers)
        ioloop = IOLoop.current()
        ioloop.set_default_executor(executor=executor)
        self.__max_excutor_workers = max_excutor_workers

    @property
    def convert_case(self) -> bool:
        """
        Whether to convert the case of keys in request parameters and response content,
        by default True.

        According to the Python style guide, snake_case is used for variable names,
        while Java prefers camelCase.

        By default, `typhoon.rest` API would convert the case of keys in request parameters
        from camelCase into snake_case, and convert the case of keys in response content
        from snake_case into camelCase.
        """
        return self.__convert_case

    @convert_case.setter
    def convert_case(self, convert_case: bool) -> None:
        self.__convert_case = convert_case

    @property
    def access_log(self) -> _LogFormatter:
        """
        Format of access log.
        """
        return self.__access_log

    @property
    def app_log(self) -> _LogFormatter:
        """
        Format of app log.
        """
        return self.__app_log

    @property
    def stats_log(self) -> _LogFormatter:
        """
        Format of stats log.
        """
        return self.__stats_log


settings = _Settings()
