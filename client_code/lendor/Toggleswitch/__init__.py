from ._anvil_designer import ToggleswitchTemplate
from anvil import *
import anvil.server

class Toggleswitch(ToggleswitchTemplate):
    def __init__(self, **properties):
        self.internal = False
        self._checked = properties.get('checked', False)
        self._enabled = properties.get('enabled', True)
        self._visible = properties.get('visible', True)
        self._shape = properties.get('shape', 'round')
        self.init_components(**properties)
        self.shape = self._shape

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        value = str(value.lower())
        if value in ["round", "square"]:
            self.check_box_1.role = "toggleswitch-" + str(value)
            self._shape = value

    @property
    def checked(self):
        return self.check_box_1.checked

    @checked.setter
    def checked(self, value):
        if type(value) is bool:
            self._checked = value
            self.update()
            self.check_box_1_change()

    @property
    def enabled(self):
        return self.check_box_1.enabled

    @enabled.setter
    def enabled(self, value):
        if type(value) is bool:
            self._enabled = value
            self.update()

    @property
    def visible(self):
        return self.check_box_1.visible

    @visible.setter
    def visible(self, value):
        if type(value) is bool:
            self.internal = not self.internal
            if self.internal:
                self._visible = value
                self.update()
                self.internal = not self.internal

    @property
    def spacing_above(self):
        return self.check_box_1.spacing_above

    @spacing_above.setter
    def spacing_above(self, value):
        if value in ['none', 'small', 'medium', 'large']:
            self.check_box_1.spacing_above = value
            self.update()

    def update(self):
        self.check_box_1.checked = self._checked
        self.check_box_1.enabled = self._enabled
        self.check_box_1.visible = self._visible

    def toggle_form_visibility(self, internal=False):
        pass

    def check_box_1_change(self, **event_args):
        self.raise_event("x_change")

    def check_box_1_show(self, **event_args):
        self.raise_event("x_show")

    def check_box_1_hide(self, **event_args):
        self.raise_event("x_hide")
