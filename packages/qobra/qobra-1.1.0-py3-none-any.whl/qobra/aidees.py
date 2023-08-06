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
'''This module contains functions to handle the program's options and events

Functions:
get_opts -- manages program options
handle_input -- handles key events
get_chunks -- yields n sized list chunks
'''

import os
import sys
import curses

sys.path.insert(1, os.path.expanduser('~/.config/qobra/'))

try:
    from config import music_dir
except ImportError:
    from qobra.config import music_dir


def usage():
    usage = '''\
Usage

qobra [-d music dir] [options]

-d  music directory
-s  start in shuffle mode
-h  see this message'''
    sys.exit(usage)


def get_opts():
    '''Manages program options

    Returns the path to the music directory along with any set
    options, or exits with an error message if the program was called
    with no arguments and directory is not defined in
    ~/.config/qobra/config.py or an invalid number of options was
    provided.
    '''
    directory, shuffle = music_dir, False
    try:
        for i, arg in enumerate(sys.argv[1:]):
            if arg == '-h':
                usage()
            elif arg == '-d':
                directory = sys.argv[i + 2]
            elif arg == '-s':
                shuffle = True
            else:
                pass
    except IndexError:
        sys.exit('Invalid number of options')

    if not directory:
        sys.exit('Argument missing: directory\nqobra -h to see usage')

    return directory, shuffle


def handle_input(stdscr, player, searchbox, window):
    '''Handle key events

    Parameters:
    stdscr -- the screen object
    player -- the player object
    '''
    curses.halfdelay(1)
    c = stdscr.getch()

    if c == ord('q'):
        player.song.stop()
        sys.exit(0)
    elif c == curses.KEY_RESIZE:
        window.resize(player, searchbox)
    elif c == ord('l'):
        player.play()
    elif c == ord('p'):
        player.pause()
    elif c == ord('k'):
        player.move_up()
    elif c == ord('i'):
        player.move_up()
        player.play()
    elif c == ord('j'):
        player.move_down()
    elif c == ord('o'):
        player.move_down()
        player.play()
    elif c == ord('t'):
        player.toggle_mode()
    elif c == ord('/'):
        searchbox.draw_search_box()


def get_chunks(it, n):
    '''Yields n sized chunks of it

    Parameters:
    list -- list object to be divided in chunks
    n -- integer with the number of chunks to create
    '''
    for i in range(0, len(it), n):
        yield it[i:i + n]
