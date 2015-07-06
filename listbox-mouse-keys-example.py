#!/usr/bin/env python

import urwid

class MyListBox(urwid.ListBox):
    def keypress(self, size, key):
        if key == 'home':
            self.set_focus(0)
            key = None
        elif key == 'end':
            self.set_focus(len(self.body) - 1)
            key = None

        super(MyListBox, self).keypress(size, key)
        return key

    def mouse_event(self, size, event, button, col, row, focus):
        currentfocus = self.focus_position
        newfocus = None
        maxindex = len(self.body) - 1

        if button == 4 and currentfocus > 0:
            newfocus = self.body.prev_position(currentfocus)
        elif button == 5 and  currentfocus < maxindex:
            newfocus = self.body.next_position(currentfocus)

        if newfocus is None:
            return False
        self.set_focus(newfocus)
        super(MyListBox, self).mouse_event(size, event, button, col, row, focus)
        return True

listwalker = urwid.SimpleFocusListWalker(list())
for i in range(100):
    listwalker.append(urwid.Button(str(i)))

box = MyListBox(listwalker)
loop = urwid.MainLoop(box)
loop.run()

