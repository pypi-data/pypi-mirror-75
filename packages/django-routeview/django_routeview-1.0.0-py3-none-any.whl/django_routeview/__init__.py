from django.urls import path
from django.views.generic import View

urlpatterns = []

class Watcher(type(View)):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, "_add_route_"):
            getattr(self, "_add_route_")(self)

class RouteView(View, metaclass=Watcher):
    """
     A view able to register itself in the django urls patterns

     route:str The url pattern for the view
     name:str:optional The name of the view. Default to self.__name__
    """

    route = None
    name = None

    def _add_route_(self):
        if self.route is not None:
            if self.name is None:
                self.name = self.__name__
            urlpatterns.append(path(self.route, self.as_view(), name=self.name))
