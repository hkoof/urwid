#!/usr/bin/env python

import sys
import urwid

import logging

i = 0

def keypress(key):
    global i
    if key == 'esc':
        raise urwid.ExitMainLoop()
    if key == 'meta a':
        i += 1
        edit1 = urwid.Edit('', 'Holla')
        edit2 = urwid.Edit('', str(6*i))
        duo = urwid.Columns([edit1, edit2])
        duo.set_focus(0)
        listwalker.append(duo)
        mainwidget.focus_position = len(listwalker)-1

log = logging.getLogger('hko')
log.setLevel(logging.DEBUG)
log.addHandler(logging.FileHandler("/tmp/log"))

log.info("started")

listwalker = urwid.SimpleFocusListWalker([])
mainwidget = urwid.ListBox(listwalker)
mainloop = urwid.MainLoop(mainwidget, unhandled_input=keypress)
mainloop.run()

