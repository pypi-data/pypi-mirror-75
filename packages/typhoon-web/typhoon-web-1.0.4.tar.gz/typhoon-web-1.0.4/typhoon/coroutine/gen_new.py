from functools import wraps

import tornado.gen
import tornado.ioloop

from ..log import trace


def _run_in_executor(func):
    @wraps(func)
    @tornado.gen.coroutine
    def wrapper(self, *args, **kwargs):
        trace_id = self.application.get_trace_id(self)

        def _func(self, args, kwargs):
            with trace(trace_id):
                _result = func(self, *args, **kwargs)
            return _result

        result = yield tornado.ioloop.IOLoop.current().run_in_executor(None, _func, self, args, kwargs)
        return result
    return wrapper
