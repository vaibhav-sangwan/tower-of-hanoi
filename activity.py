from gettext import gettext as _

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import pygame

from sugar3.activity.activity import Activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import StopButton


import sugargame.canvas
import main


class TowerOfHanoiActivity(Activity):

    def __init__(self, handle):
        Activity.__init__(self, handle)

        self.game = main.TowerOfHanoi()

        self.build_toolbar()
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self, main=self.game.run, modules=[pygame.display])

        self.set_canvas(self._pygamecanvas)
        self._pygamecanvas.grab_focus()

    def build_toolbar(self):
        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()
        stop_button.connect('clicked', self._stop_cb)

    def _stop_cb(self, button):
        self.game.is_running = False
