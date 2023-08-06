#   Copyright (C) 2020  Alexander Goussas
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import curses

try:
    from config import window_fg, window_bg, bg_char, border
except ImportError:
    from qobra.config import (window_fg, window_bg, bg_char, border)


class Window:
    def __init__(self, stdscr, colors):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.colors = colors

    def draw(self, player):
        '''Draws the program window'''
        curses.init_pair(3, self.colors[window_fg], self.colors[window_bg])
        self.stdscr.bkgd(bg_char, curses.color_pair(3))
        if border:
            self.stdscr.border()
        self.draw_statusline(player)
        player.display_songs()

    def draw_statusline(self, player):
        '''Draw the statusbar at the bottom of the screen

        Display information about the song_index playing song,
        the playing status and the playing mode. It is drawn
        2 lines above the window bottom to compensate for the
        border.
        '''
        y = self.height - 2
        # player status
        status = 'Playing' if player.song.playing else 'Paused'
        status_color = 4 if player.song.playing else 5
        self.stdscr.addstr(y, 2, status, curses.color_pair(status_color))
        # name of the current song
        self.stdscr.addnstr(y, 10, player.song.name, self.width - 20,
                            curses.color_pair(6))
        # playing mode
        mode = 'Shuffle' if player.shuffle else 'Normal'
        mode_colors = 7 if not player.shuffle else 8
        self.stdscr.addstr(y, self.width - len(mode) - 1, mode,
                           curses.color_pair(mode_colors))

    def resize(self, player, searchbox):
        '''Resizes the window.

        Updates the player's current group size to fit in the new window
        height and makes sure the current song stays selected.
        '''
        self.height, self.width = self.stdscr.getmaxyx()
        player.update_group_size(self.height)
        for group in player.groups:
            if player.song in group:
                player.group_index = player.groups.index(group)
        player.current_group = player.groups[player.group_index]
        player.song_index = player.current_group.index(player.song.path)

        searchbox.width = self.stdscr.getmaxyx()[1] - 11
        searchbox.y = self.stdscr.getmaxyx()[0] - 2
