import functools
from inspect import signature, Signature
import typing
import collections




def _check_iteratable(type) -> bool:
    if isinstance(typing._GenericAlias):
        type = type.__origin__
    return issubclass(type, collections.abc.Iterable)


def _check_argument(sig: Signature, arguments, to_ignore) -> bool:
    i = 0
    if len(sig.parameters) - len(to_ignore) != len(arguments):
        return False
    for argument_name in sig.parameters:
        if argument_name in to_ignore:
            continue
        argument_type = sig.parameters[argument_name].annotation
        if isinstance(argument_type, typing.List.__class__):
            intern_type = argument_type.__args__[0]
            for aa in arguments[i]:
                if not isinstance(aa, intern_type):
                    return False
        elif not isinstance(arguments[i], argument_type):
            return False
        i += 1
    return True


def _object_to_json(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return "WORKING"
        sig = signature(func)
        print(args, kwargs, request.data, request.args, request.data, request.files, request.values, request.json, signature(func))
        print(kwargs)
        input = []
        if request.json:
            input.append(request.json)
        if _check_argument(sig, input, kwargs.keys()):
            for key in kwargs:
                kwargs[key] = int(kwargs[key])
            return json.dumps(func(*input, **kwargs))
        else:
            return "400"
    return inner


class AbstractDecorator:
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper._container_class = self
        return wrapper


class _AbstractHttpRoute(AbstractDecorator):
    def __init__(self, path=""):
        self._path = path

    @classmethod
    def apply(cls, app, service, method):
        print("/".join(("", service.__class__.__name__, method._container_class._path)), [cls.__name__.upper()])
        #app.route("/".join(("", services.__class__.__name__, method._container_class._path)), methods=[cls.__name__.upper()])(lambda *a, **kw: method(*a, **kw))
        app.route("/".join(("", service.__class__.__name__, method._container_class._path)), methods=[cls.__name__.upper()])(_object_to_json(method))


