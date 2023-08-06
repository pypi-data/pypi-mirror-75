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
from subprocess import Popen, DEVNULL, STDOUT, PIPE


class Song:
    def __init__(self, path):
        self.path = path
        self.playing = False
        self.process = None

    @property
    def name(self):
        '''Sets the song name.'''
        return os.path.basename(self.path)

    @property
    def running(self):
        '''Returns True if current process has finished.'''
        return self.process.poll() is None

    def play(self):
        '''Spawns a new mpg123 process to play a song.'''
        self.playing = True
        self.process = Popen(
            ['mpg123', self.path, '--title', '--name', self.name],
            stdin=PIPE,
            stdout=DEVNULL,
            stderr=STDOUT)

    def pause(self):
        '''Sends space key to current process to stop song.

        mpg123 also accepts "s" to toggle playing state of song.
        '''
        supported_terminals = ['xterm', 'rxvt', 'screen', 'iris-ansi']
        if os.environ['TERMINAL'] in supported_terminals or os.environ[
                'TERM'] in supported_terminals:
            # TODO test this
            xdotool = Popen(['xdotool', 'search', '--name', self.name],
                            stdout=PIPE)
            winid, _ = xdotool.communicate()
            pauser = Popen(['xdotool', 'key', '--window', winid, 'space'])
            pauser.wait()
            self.playing = not self.playing
        else:
            self.stop()

    def stop(self):
        '''Sends SIGTERM signal to current process.'''
        try:
            self.playing = False
            self.process.terminate()
        except AttributeError:
            pass
