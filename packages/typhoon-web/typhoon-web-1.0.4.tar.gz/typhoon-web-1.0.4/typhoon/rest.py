"""
typhoon.rest module
"""
import json
import logging
import re
from functools import wraps

import tornado.ioloop

from . import __version__
from .settings import settings
from .status import INTERNAL_SERVER_ERROR, OK, UNAUTHORIZED
from .util import camel_to_snake, get_banner, json_camel_to_snake, json_snake_to_camel
from .web import Application, RequestHandler, run_in_executor

logger = logging.getLogger(__name__)


class RestCallback(object):
    """
    Callback object.

    Parameters
    ----------
    func_name : str
        name of func to call. should be a method of controller's.
    args : tuple, optional
        args, by default None
    kwargs : dict, optional
        kwargs, by default None
    """

    def __init__(self, func_name, args=None, kwargs=None):
        self.__func_name = func_name
        self.__args = args or ()
        self.__kwargs = kwargs or {}

    @property
    def func_name(self):
        """
        func_name
        """
        return self.__func_name

    @property
    def args(self):
        """
        args
        """
        return self.__args

    @property
    def kwargs(self):
        """
        kwargs
        """
        return self.__kwargs


class RestResult(object):
    """
    RestResult object.

    Parameters
    ----------
    status : int, optional
        HTTP status, by default 200
    content : Union[str, dict], optional
        response content, by default None
    callback : RestCallback, optional
        RestCallback object, by default None
    """

    def __init__(self, status=OK, content=None, callback=None):
        self.__status = status
        self.__content = content
        self.__callback = callback

    @property
    def status(self):
        """
        status
        """
        return self.__status

    @property
    def content(self):
        """
        content
        """
        return self.__content

    @property
    def callback(self):
        """
        callback
        """
        return self.__callback


class RestHandler(RequestHandler):
    """
    RestHandler object.
    """

    def __init__(self, *args, **kwargs):
        super(RestHandler, self).__init__(*args, **kwargs)
        self.params: dict

    def prepare(self):
        url_params = {}
        if settings.convert_case:
            for key in self.request.arguments:
                url_params[camel_to_snake(key)] = self.get_argument(name=key)

            try:
                camel_json = self.decode_argument(self.request.body)
                snake_json = json_camel_to_snake(camel_json)
                body_params = json.loads(snake_json)
            except:
                body_params = {}
        else:
            for key in self.request.arguments:
                url_params[key] = self.get_argument(name=key)
            try:
                body_json = self.decode_argument(self.request.body)
                body_params = json.loads(body_json)
            except:
                body_params = {}

        self.params = {**url_params, **body_params}

    @staticmethod
    def serialize(content):
        if isinstance(content, str):
            return content
        content_json = json.dumps(content)
        if settings.convert_case:
            return json_snake_to_camel(content_json)
        return content_json

    @run_in_executor
    def process(self, *args, **kwargs):
        return self.application._process(*args, **kwargs)

    async def handle(self, _func, *args, **kwargs):
        kwargs = {**kwargs, **self.params}
        result = await self.process(_func, *args, **kwargs)

        status = result.status
        self.set_status(status)

        content = result.content
        if content:
            self.write(self.serialize(content))
        self.finish()

        callback = result.callback
        if callback:
            await self.process(callback.func_name, *callback.args, **callback.kwargs)

    def compute_etag(self):
        return None

    def data_received(self, chunk):
        pass


_HANDLERS = {}


def route(uri, method='get', auth_required=False):
    """
    Decorator for methods of RestController.

    Typhoon will generate a RequestHandler for each distinct uri, and
    create a http method as specified which is binded to the decorated method.

    Parameters
    ----------
    uri : str
        Endpoint of the api.
    method : str, optional
        HTTP method, by default 'get'
    auth_required : bool, optional
        whether authorization is required, by default False
    """
    method = method.lower()
    assert method in ('get', 'post', 'put', 'patch',
                      'delete', 'head', 'options')

    def decorator(func):
        func_name = func.__name__
        hdlr_name = '%s_handler' % '_'.join(re.split(r'[^\w]', uri))

        if uri not in _HANDLERS:
            _HANDLERS[uri] = type(hdlr_name, (RestHandler,), dict())

        async def method_body(self, *args, **kwargs):
            authorized = True
            if auth_required:
                auth_header = self.request.headers.get('Authorization')
                authorized = await self.process(_func='authorize', auth_header=auth_header)
            if authorized:
                await self.handle(func_name, *args, **kwargs)
            else:
                self.set_status(UNAUTHORIZED)
                content = {'error': 'authorization is required for this method.'}
                self.write(self.serialize(content))

        setattr(_HANDLERS[uri], method, method_body)

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
            except Exception as e:
                logger.error('%s', e, exc_info=True)
                result = RestResult(
                    status=INTERNAL_SERVER_ERROR,
                    content={'error': f'{e}'}
                )
            return result
        return wrapper
    return decorator


class RestController(object):
    """
    RestController object.
    """

    def __init__(self):
        banner = get_banner(__version__)
        logger.info(banner)

    def authorize(self, auth_header):
        """
        override this method to check authorization.

        Parameters
        ----------
        auth_header : Union[dict, None]
            Authorization header of the request.
        """
        raise NotImplementedError

    @route(uri=r'/typhoon/banner', method='get')
    def _get_typhoon_banner(self):
        return RestResult(content=f'<pre>{get_banner(__version__)}')

    @route(uri=r'/typhoon/version', method='get')
    def _get_typhoon_version(self):
        return RestResult(
            content={
                'typhoon': __version__,
                'tornado': tornado.version
            }
        )


class RestApplication(Application):
    """
    RestApplication object.
    """

    def __init__(self, controller: RestController) -> None:
        handlers = []
        for uri in _HANDLERS:
            handlers.append((uri, _HANDLERS[uri]))

        super(RestApplication, self).__init__(handlers=handlers)

        self._controller = controller

    def _process(self, _func, *args, **kwargs):
        return getattr(self._controller, _func)(*args, **kwargs)


def start_server(controller: RestController, port: int = 9999) -> None:
    """
    start a HTTP server.

    Parameters
    ----------
    controller : RestController
        controller.
    port : int, optional
        port to listen to, by default 9999
    """
    try:
        app = RestApplication(controller=controller)
        app.listen(port)
        tornado.ioloop.IOLoop.current().start()
    except:
        logger.error('oops! server crashed...', exc_info=True)
