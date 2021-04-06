from view import View
class Presenter:

    def __init__(self, view):
        self._init_view(view)

    def _init_view(self, view):
        self._view = view

    def show(self):
        self._view.show()