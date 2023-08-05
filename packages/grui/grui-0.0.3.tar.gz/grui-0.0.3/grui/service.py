from .utils import dash_case


# This class allow us to generate the url path from the name of the class
# If the developer want to specify a specific name he can use the _url_prefix class variable
class _AbstractGruiServiceMeta(type):

    @property
    def url_prefix(cls):
        try:
            name = cls.__dict__["_url_prefix"]
        except KeyError:
            name = dash_case(cls.__name__)
            if name.endswith('-service'):
                name = name[:-8]
        return name


class AbstractGruiService(metaclass=_AbstractGruiServiceMeta):
    pass


# Every function decorated by any GruiDecorator will be replace by this class.
# Like that the GruiApp will be able to expose the function (or method of a service class)
class GruiFunction:

    def __init__(self, callable_, grui_decorator):
        self._instance = None
        self._owner = None
        if isinstance(callable_, GruiFunction):
            self._callable = callable_._callable
            self.grui_decorators = callable_.grui_decorators
            self._properties = callable_._properties
        else:
            self._callable = callable_
            self.grui_decorators = []
            self._properties = GruiFunctionProperties(self)
        grui_decorator.method = self
        self.grui_decorators.append(grui_decorator)

    def __get__(self, instance, owner):
        # We save the instance of the object from the method class. In case the function is a method
        self._instance = instance
        self._owner = owner
        return self

    def __call__(self, *args, **kwargs):
        # Invoked on every call of any decorated method
        if self._instance:
            return self._callable(self._instance, *args, **kwargs)
        else:
            return self._callable(*args, **kwargs)

    @property
    def props(self):
        if not self._properties.updated:
            self._properties.update(self._instance)
        return self._properties

    # To trick the inspect python module we override the 5 following properties:
    # code, defaults, kwdefaults, annotation and name.
    # Like that the method inspect.signature() return the same result as an undecorated function.
    @property
    def __code__(self):
        return self._callable.__code__

    @property
    def __defaults__(self):
        return self._callable.__defaults__

    @property
    def __kwdefaults__(self):
        return self._callable.__kwdefaults__

    @property
    def __annotations__(self):
        return self._callable.__annotations__

    @property
    def __name__(self):
        if self._owner:
            return "%s.%s.%s" % (self._callable.__module__, self._owner.__name__, self._callable.__name__)
        else:
            return "%s.%s" % (self._callable.__module__, self._callable.__name__)

    @property
    def __doc__(self):
        return self._callable.__doc__


# This class contains all the properties updated by the grui decorators.
# This code is wrote in a way that the properties are generated only if the code is executed into a GruiApp
class GruiFunctionProperties:

    def __init__(self, function: GruiFunction):
        self._function = function
        self.url_path = None
        self.http_method = None
        self.default_http_return_code = 200  # OK
        self.previous_actions = []
        self.next_actions = []
        self.multiple_action = False
        self._updated = False

    def update(self, service: AbstractGruiService):
        for grui_decorator in self._function.grui_decorators:
            grui_decorator.update_props(self, service)
        self._updated = True

    @property
    def updated(self):
        return self._updated
