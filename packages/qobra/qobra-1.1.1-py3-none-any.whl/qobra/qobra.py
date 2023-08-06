#!/usr/bin/env python3

#   qobra is a simple terminal music player
#   Contribute at agoussas@espol.edu.ec

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

import qobra.aidees as f
from qobra.player import Player
from qobra.searchbox import SearchBox
from qobra.window import Window

colors = {
    'white': curses.COLOR_WHITE,
    'black': curses.COLOR_BLACK,
    'red': curses.COLOR_RED,
    'green': curses.COLOR_GREEN,
    'yellow': curses.COLOR_YELLOW,
    'blue': curses.COLOR_BLUE,
    'magenta': curses.COLOR_MAGENTA,
    'cyan': curses.COLOR_CYAN,
}


def main(stdscr):
    '''Run the main loop.

    Parameters:
    stdscr -- the screen object used to draw the window
    '''
    curses.curs_set(False)
    path, shuffle = f.get_opts()

    window = Window(stdscr, colors)
    player = Player(path, shuffle, stdscr, colors, window)
    searchbox = SearchBox(player, stdscr, colors)

    while True:
        stdscr.erase()
        window.draw(player)
        player.update()
        stdscr.refresh()
        f.handle_input(stdscr, player, searchbox, window)


curses.wrapper(main)
if __name__ == '__main__':
    main()
