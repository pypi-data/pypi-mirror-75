from inspect import getmembers, isclass, signature
from functools import wraps
from flask import Flask, json, request
from collections.abc import Iterable   # drop `.abc` with Python 2.7 or lower

from .typing import *
from .service import AbstractGruiService, GruiFunction


class ArgumentMatchError(RuntimeError):
    pass


def dict2list(dict_: dict) -> List[dict]:
    result = []
    for key in dict_:
        for i, value in enumerate(dict_[key]):
            try:
                result[i][key] = value
            except IndexError:
                result.append({key: value})
    return result


def _convert_argument_list(type_: type, value: Any) -> List[Any]:
    result = []
    if isinstance(value, str):
        for tmp in value.split(","):
            result.append(_convert_argument(type_, tmp, False))
    elif isinstance(value, Iterable):
        for tmp in value:
            result.append(_convert_argument(type_, tmp, False))
    return result


def _convert_argument(type_: type, value: Any, to_list: bool) -> Any:
    if to_list:
        return _convert_argument_list(type_, value)
    else:
        if type_ is int:
            return int(value)
        elif type_ is float:
            return float(value)
        elif isinstance(type_, List.__class__):
            return _convert_argument_list(type_.__args__[0], value)
    return value


def _match_argument(method: GruiFunction, input_: dict, additional_data: Any = None) -> Any:
    result = {}
    parameters = method.__annotations__
    param_found = []

    for param_name, param_class in parameters.items():
        if param_name in input_:
            result[param_name] = _convert_argument(param_class, input_[param_name], method.props.multiple_action)
            param_found.append(param_name)

    unfounded = None
    for param_name in parameters:
        if param_name not in param_found:
            unfounded = param_name
            break

    if additional_data is not None and unfounded is not None and len(parameters) == len(param_found) + 1:
        result[unfounded] = _convert_argument(parameters[unfounded], additional_data, method.props.multiple_action)
        param_found.append(unfounded)

    if len(parameters) != len(param_found):
        raise ArgumentMatchError

    if method.props.multiple_action:
        return dict2list(result)

    return result


def _map_method_to_flask_app(method: GruiFunction):
    @wraps(method)
    def _(*args, **kwargs):
        try:
            if isinstance(request.json, dict):
                kwargs.update(request.json)
                method_arguments = _match_argument(method, kwargs)
            else:
                method_arguments = _match_argument(method, kwargs, request.json)
        except ArgumentMatchError:
            return "Error", 400
        code = method.props.default_http_return_code
        if method.props.multiple_action:
            result = []
            for kw in method_arguments:
                for previous_action in method.props.previous_actions:
                    previous_action(code)
                res = method(*args, **kw)
                for next_action in method.props.next_actions:
                    (result, code) = next_action(result, code)
                result.append(res)
            return json.dumps(result), code
        else:
            for previous_action in method.props.previous_actions:
                previous_action(code)
            result = method(*args, **kwargs)
            for next_action in method.props.next_actions:
                (result, code) = next_action(result, code)
            return json.dumps(result), code
    return _


class GruiApp:

    def __init__(self, service_package, debug=False):
        self._flask_app = Flask(__name__)
        self._flask_app.url_map.strict_slashes = False
        self._debug = debug
        self._services = {}
        self.register_package(service_package)
        self._flask_app.route('/shutdown', methods=['GET'])(GruiApp.shutdown)

    def register_package(self, package):
        for _, service_class in getmembers(package, lambda c: isclass(c) and issubclass(c, AbstractGruiService)):
            self.register_service(service_class)

    def register_service(self, service_class):
        service = service_class()
        self._services[service_class.__module__+"."+service_class.__name__] = service

        for _, method in getmembers(service, lambda m: isinstance(m, GruiFunction)):
            self.register_function(method)

    def register_function(self, method: GruiFunction):
        self._flask_app.route(method.props.url_path, methods=[method.props.http_method])\
            (_map_method_to_flask_app(method))

    def run(self):
        self._flask_app.run(debug=self._debug)

    @staticmethod
    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    @staticmethod
    def shutdown():
        GruiApp.shutdown_server()
        return 'Server shutting down...'
