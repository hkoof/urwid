#!/usr/bin/env python
import sys
# sys.path.insert(0, "./3")

import urwid

class EditWithCallbacks(urwid.Edit):
    def __init__(self, *args, **kwargs):
        self._on_accept = kwargs.pop("on_accept")
        self._on_cancel = kwargs.pop("on_cancel")
        self.__super.__init__(*args, **kwargs)

    def keypress(self, size, key):
        if key in ('enter',) and self._on_accept:
            self._on_accept(self.get_edit_text())
            return None
        elif key in ('esc','ctrl g') and self._on_cancel:
            self._on_cancel(self.get_edit_text())
            return None
        else:
            return self.__super.keypress(size, key)

class EditItemWidget(urwid.WidgetWrap):
    def __init__(self, item):
        self._item = item  # simple dictionary
        self._walker = urwid.SimpleFocusListWalker([])
        for key,value in self._item.items():
            self._walker.append(EditItemLineWidget(key, value))
        self._listbox = urwid.ListBox(self._walker)
        self.__super.__init__(self._listbox)

    def add_keyvaluepair(self):
        new_kvp = EditItemLineWidget('', '')
        self._walker.append(new_kvp)
        self._listbox.focus_position = len(self._walker)-1
        self._listbox.focus.rename(on_cancel=self.remove_keyvaluepair)

    def rename_keyvaluepair(self):
        self._listbox.focus.rename()

    def remove_keyvaluepair(self, *args):
        del(self._walker[self._listbox.focus_position])

    def keypress(self, size, key):
        if self.__super.keypress(size, key) is None:
            return None
        elif key in ('meta a'):
            self.add_keyvaluepair()
            return None
        elif key in ('meta r',):
            self.remove_keyvaluepair()
            return None
        elif key in ('meta n',):
            self.rename_keyvaluepair()
            return None
        return key

class EditItemLineWidget(urwid.WidgetWrap):
    def __init__(self, key, value):
        self.key = key
        label = urwid.Text(key.capitalize(), align='right')
        value = urwid.Edit(edit_text=str(value))
        self._columns = urwid.Columns([
            (20, label),
            urwid.AttrMap(value, 'textfield'),
        ], dividechars=1)
        self.__super.__init__(self._columns)

    def rename(self, on_accept=None, on_cancel=None):
        options = self._columns.options('given', 20)
        def close_rename():
            label = urwid.Text(self.key.capitalize(), align='right', wrap='clip')
            self._columns.contents[0] = (label, options)
            self._columns.focus_position = 1
        def cancel_rename(new_key):
            close_rename()
            if on_cancel:
                on_cancel(new_key)
        def commit_rename(new_key):
            self.key = new_key
            close_rename()
            if on_accept:
                on_accept(new_key)
        label = EditWithCallbacks(edit_text=self.key.lower(), align='left',
                                  on_accept=commit_rename,
                                  on_cancel=cancel_rename)
        self._columns.contents[0] = (urwid.AttrMap(label, 'textfield'), options)
        self._columns.focus_position = 0


item = dict(firstname='Guybrush', lastname='Threepwood', age='No')

def keypress(key):
    if key == 'esc':
        raise urwid.ExitMainLoop()

palette = [
    ('topbar',    'black','light gray'),
    ('textfield', 'black','brown'),
]

topbar = urwid.Columns([
    urwid.AttrMap(urwid.Text('esc:Quit/Cancel  Meta-a:Add  Meta-r:Remove  Meta-n:Rename'), 'topbar'),
    ('pack', urwid.Text('Urwid %s' % urwid.__version__))
])
explanation = urwid.Text('''
Adding a new key/value pair (meta-a) should focus the key of the newly created
line, not the value. Hitting "pos1/home" before "meta a" seems to produce the
desired behaviour reliably.
''')
mainwidget = urwid.Pile([
    ('pack', urwid.AttrMap(topbar, 'topbar')),
    ('pack', explanation),
    EditItemWidget(item)
])
mainloop = urwid.MainLoop(mainwidget, palette,
                          unhandled_input=keypress)
mainloop.run()
