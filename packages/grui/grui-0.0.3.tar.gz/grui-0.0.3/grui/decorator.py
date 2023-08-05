from abc import ABC, abstractmethod
from typing import Any

from .service import AbstractGruiService, GruiFunction, GruiFunctionProperties
from .utils import dash_case


def _grui_decorator(default_param=()):
    def __inner(cls):
        def ___wrapper(*args, **kwargs):
            if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
                # actual decorated function
                return cls(*default_param)(*args)
            else:
                # decorator arguments
                return lambda *a, **kw: cls(*args, **kwargs)(*a, **kw)
        return ___wrapper
    return __inner


class _AbstractGruiDecorator(ABC):
    def __init__(self, _=None):
        self.method = None

    def __call__(self, action):
        return GruiFunction(action, self)

    @abstractmethod
    def update_props(self, props: GruiFunctionProperties, service: AbstractGruiService):
        pass


class _AbstractHttpRoute(_AbstractGruiDecorator):
    def __init__(self, path=""):
        super().__init__("")
        self.path = path

    def update_props(self, props: GruiFunctionProperties, service: AbstractGruiService):
        if service is None:
            if self.path == "":
                props.url_path = "/"+dash_case(self.method.__name__).replace(".", "/")+"/"
            else:
                props.url_path = "/"+self.path+"/"
        else:
            props.url_path = "/".join(("", service.__class__.url_prefix, self.path))
        props.http_method = self.__class__.__name__.upper()


@_grui_decorator(("",))
class Get(_AbstractHttpRoute):
    pass


@_grui_decorator(("",))
class Post(_AbstractHttpRoute):

    def update_props(self, props: GruiFunctionProperties, service: AbstractGruiService):
        super().update_props(props, service)
        props.default_http_return_code = 202  # Created


@_grui_decorator(("",))
class Put(_AbstractHttpRoute):
    pass


@_grui_decorator(("",))
class Delete(_AbstractHttpRoute):
    pass


@_grui_decorator(())
class NotFoundIfNone(_AbstractGruiDecorator):

    def update_props(self, props: GruiFunctionProperties, service: AbstractGruiService):
        def _(result: Any, code: int):
            if result is None:
                return [], 404
            return result, code
        props.next_actions.append(_)


@_grui_decorator(())
class NotFoundIfEmpty(_AbstractGruiDecorator):

    def update_props(self, props: GruiFunctionProperties, service: AbstractGruiService):
        def _(result: Any, code: int):
            if len(result) == 0:
                return [], 404
            return result, code
        props.next_actions.append(_)


@_grui_decorator(())
class MultipleCallAtOnce(_AbstractGruiDecorator):

    def update_props(self, props: GruiFunctionProperties, service: AbstractGruiService):
        props.multiple_action = True
