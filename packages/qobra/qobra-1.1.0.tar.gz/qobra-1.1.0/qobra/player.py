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
import random

import qobra.aidees as f
from qobra.song import Song

sys.path.insert(1, os.path.expanduser('~/.config/qobra/'))

try:
    from config import (
        shuffle_mode_fg,
        shuffle_mode_bg,
        normal_mode_fg,
        normal_mode_bg,
        statusbar_song_fg,
        statusbar_song_bg,
        paused_fg,
        paused_bg,
        playing_fg,
        playing_bg,
        songs_fg,
        songs_bg,
        current_song_fg,
        current_song_bg,
    )
except ImportError:
    try:
        from qobra.config import (
            shuffle_mode_fg,
            shuffle_mode_bg,
            normal_mode_fg,
            normal_mode_bg,
            statusbar_song_fg,
            statusbar_song_bg,
            paused_fg,
            paused_bg,
            playing_fg,
            playing_bg,
            songs_fg,
            songs_bg,
            current_song_fg,
            current_song_bg,
        )
    except ImportError:
        raise ImportError('Couldn\'t find path to config file')


class Player:
    '''Manages state of the program.

    Attributes:
    root -- the path to the user's music directory
    song_index -- index of the curent song
    group_index -- index of the current group
    songs -- list with the songs in the provided path
    groups -- sublists of songs divided in window-sized chunks
    current_group -- current group displayed on the screen
    song -- name of the currently playing song
    '''
    def __init__(self, root, shuffle, stdscr, colors, window):
        self.stdscr = stdscr
        self.colors = colors
        self.shuffle = shuffle
        self.window = window

        self.songs = [os.path.join(root, song) for song in os.listdir(root)]
        self.song_index, self.group_index = 0, 0
        self.groups = list(f.get_chunks(self.songs, self.window.height - 3))
        self.current_group = self.groups[self.group_index]
        self.song = Song(self.current_group[self.song_index])
        self.init_colors()

    def display_songs(self):
        '''Displays songs on the screen.

        Display the songs contained in the current group. It
        starts drawing them 1 line after the window start to
        compensate for the border. The curren song is given
        different colors.
        '''
        x_offset, y_offset = 3, 1
        for idx, song in enumerate(self.current_group):
            song = os.path.basename(song)
            free_space = self.window.width - len(song) - x_offset
            song_color = curses.color_pair(
                1) if idx == self.song_index else curses.color_pair(2)
            self.stdscr.addnstr(idx + y_offset, x_offset,
                                song + ' ' * free_space, self.window.width - 5,
                                song_color)

    def update_group_size(self, new_height):
        '''Updates the chunk size on window resize

        Parameters:
        new_height -- the new height of the window
        '''
        self.groups = list(f.get_chunks(self.songs, new_height - 3))

    def update(self):
        '''Play next song after song_index one ends

        Checks if a song is playing and if the last mpg123 process has
        terminated. If a song is playing and there are no living processes,
        play the next song.
        '''
        if self.song.playing and not self.song.running:
            self.song_index = self.playing_song_index
            self.move_down()
            self.play()

    def play(self):
        '''
        Plays a song. Stop the current process first to make sure no duplicate
        processes are running.
        '''
        self.song.stop()
        if self.shuffle:
            this_song = self.select_random()
        else:
            this_song = self.current_group[self.song_index]
        self.playing_song_index = self.song_index
        self.song = Song(this_song)
        self.song.play()

    def select_random(self):
        '''Set a random song to be the song_index one'''
        random_song = random.choice(self.songs)
        for group_number, group in enumerate(self.groups):
            for song_number, song in enumerate(group):
                if song == random_song:
                    self.group_index = group_number
                    self.current_group = self.groups[self.group_index]
                    self.song_index = song_number

        return random_song

    def toggle_mode(self):
        '''Toggles between Normal and Shuffle mode.'''
        self.shuffle = not self.shuffle

    def pause(self):
        '''Pauses the player.'''
        # im working on a way to send keys to mpg123 portably
        self.song.pause()

    def move_down(self):
        '''Moves down a song.

        If the song is the last one in the current group,
        moves to the first song in the next chunk, else
        it just moves down a song.
        '''
        if self.song_index < len(self.current_group) - 1:
            self.song_index += 1
        elif self.group_index < len(self.groups) - 1:
            self.song_index = 0
            self.group_index += 1
            self.current_group = self.groups[self.group_index]
        else:
            self.song_index, self.group_index = 0, 0

    def move_up(self):
        '''Moves up a song

        If the song is the the first one in the current group,
        move to the last song in the previous one,
        else just move back a song.
        '''
        if self.song_index > 0:
            self.song_index -= 1
        elif self.group_index > 0:
            self.group_index -= 1
            self.current_group = self.groups[self.group_index]
        else:
            self.group_index = len(self.groups) - 1
            self.current_group = self.groups[self.group_index]
            self.song_index = len(self.current_group) - 1

    def init_colors(self):
        '''Initializes colors.'''
        # songs colors
        curses.init_pair(1, self.colors[current_song_fg],
                         self.colors[current_song_bg])
        curses.init_pair(2, self.colors[songs_fg], self.colors[songs_bg])
        # statusline
        curses.init_pair(4, self.colors[playing_fg], self.colors[playing_bg])
        curses.init_pair(5, self.colors[paused_fg], self.colors[paused_bg])
        curses.init_pair(6, self.colors[statusbar_song_fg],
                         self.colors[statusbar_song_bg])
        curses.init_pair(7, self.colors[normal_mode_fg],
                         self.colors[normal_mode_bg])
        curses.init_pair(8, self.colors[shuffle_mode_fg],
                         self.colors[shuffle_mode_bg])
