#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tower Of Hanoi
# Copyright (C) 2024 Vaibhav Sangwan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact information:
# Vaibhav Sangwan    sangwanvaibhav02@gmail.com

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import pygame

pygame.init()

from gamestatemanager import GameStateManager
from states.level import Level
from states.mainmenu import MainMenu
from states.helpmenu import HelpMenu
from states.levelselectmenu import LevelSelectMenu
from states.pausemenu import PauseMenu
from utils import Utils

from gettext import gettext as _

FPS = 30
BASE_RES = 640, 360


class TowerOfHanoi:
    def __init__(self):
        pygame.display.set_caption(_("Tower Of Hanoi"))
        self.clock = pygame.time.Clock()

    def fill_bg(self):
        part1 = Utils.get_act_pos((0, 322))[1]
        part2 = Utils.get_act_pos((0, 342))[1]
        pygame.draw.rect(
            self.render_screen,
            "#bee7fb",
            (0, 0, self.render_screen.get_width(), part1)
        )
        pygame.draw.rect(
            self.render_screen,
            "#4d913c",
            (0, part1, self.render_screen.get_width(), part2),
        )
        pygame.draw.rect(
            self.render_screen,
            "#7cab41",
            (
                0,
                part2,
                self.render_screen.get_width(),
                self.render_screen.get_height()
            ),
        )

    def run(self):
        self.screen = pygame.Surface(BASE_RES)
        self.render_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen_width = self.render_screen.get_width()
        screen_height = self.render_screen.get_height()
        x_ratio = screen_width / BASE_RES[0]
        y_ratio = screen_height / BASE_RES[1]
        self.scale = min(x_ratio, y_ratio)
        act_sw = BASE_RES[0] * self.scale
        act_sh = BASE_RES[1] * self.scale
        self.scaled_screen_rect = pygame.Rect(0, 0, act_sw, act_sh)
        self.scaled_screen_rect.center = (screen_width / 2, screen_height / 2)
        Utils.scaled_screen_rect = self.scaled_screen_rect

        self.gameStateManager = GameStateManager("main-menu")
        self.states = {}
        for i in range(1, 8):
            self.states["level " + str(i)] = Level(i, self)
        self.states["main-menu"] = MainMenu(self)
        self.states["help-menu"] = HelpMenu(self)
        self.states["level-select-menu"] = LevelSelectMenu(self)
        self.states["pause-menu"] = PauseMenu(self)

        self.is_running = True
        while self.is_running:
            curr_state = self.states[self.gameStateManager.get_state()]
            while Gtk.events_pending():
                Gtk.main_iteration()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                curr_state.handle_event(event)

            curr_state.run()

            self.fill_bg()
            scaled_screen = pygame.transform.scale(
                self.screen,
                (self.scale * BASE_RES[0], self.scale * BASE_RES[1])
            )
            self.render_screen.blit(scaled_screen, self.scaled_screen_rect)

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    g = TowerOfHanoi()
    g.run()
