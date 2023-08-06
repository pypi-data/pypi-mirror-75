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

import os
import sys
import curses
from curses.textpad import Textbox

sys.path.insert(1, os.path.expanduser('~/.config/qobra/'))

try:
    from config import search_fg, search_bg, search_box_fg, search_box_bg
except ImportError:
    from qobra.config import (search_fg, search_bg, search_box_fg,
                              search_box_bg)


class SearchBox:
    '''Text box to filter songs.

    Creates a text box at the bottom of the window when the
    search event is triggered.

    Attributes:
    stdscr -- the screen object
    player -- the player object
    colors -- mapping of curses colors
    height -- the TextBox instance height
    widht -- the TextBox instance width
    x -- the TextBox instance x offset
    y -- the TextBox instance y offset
    action -- the action performed when exiting the textbox
    '''
    def __init__(self, player, stdscr, colors):
        self.stdscr = stdscr
        self.colors = colors
        self.player = player

        self.height = 1
        self.width = self.stdscr.getmaxyx()[1] - 11
        self.x, self.y = 10, self.stdscr.getmaxyx()[0] - 2
        self.searched = False

    def draw_search_box(self):
        '''Draws the search box.

        Draws a search box at the bottom of the screen and let's the user
        filter songs. The contents of the search box are then dispatched
        to a filter function to update the current song and chunk.
        '''
        curses.init_pair(9, self.colors[search_fg], self.colors[search_bg])
        curses.init_pair(10, self.colors[search_box_fg],
                         self.colors[search_box_bg])
        self.stdscr.addstr(self.y, 2, 'Search: ', curses.color_pair(9))
        self.stdscr.refresh()

        editwin = curses.newwin(self.height, self.width, self.y, self.x)
        editwin.bkgd(' ', curses.color_pair(10))

        box = Textbox(editwin)
        box.edit(self.__handle_keys)

        if self.searched:
            self.__filter_songs(box.gather())

        self.searched = False

    def __filter_songs(self, match):
        '''Updates the current song and chunk.

        Uses the string provided in the match parameter to update the
        current chunk to the one containing the song name that matches
        it.
        '''
        for song in self.player.songs:
            if match.strip().lower() in song.strip().lower():
                matched_song = song
                for idx, group in enumerate(self.player.groups):
                    if matched_song in group:
                        self.player.group_index = idx
                        self.player.current_group = self.player.groups[
                            self.player.group_index]
                        self.player.song_index = self.player.current_group.index(
                            matched_song)
                        break
                break

    def __handle_keys(self, ch):
        '''Helper function for the edit() method

        Handles key events that occur when the search box is spawned
        '''
        if ch == 27:  # Escape key
            return 7
        elif ch == 10:  # Enter key
            self.searched = True
            return 7
        else:
            return ch
