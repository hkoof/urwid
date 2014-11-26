import urwid
import sys

def handle_input(key):
    if key == 'q': raise urwid.ExitMainLoop()

def main():
    #w = urwid.BigText('Aloha', urwid.font.Thin6x6Font())
    w = urwid.Text('Aloha')
    w = urwid.Padding(w)
    w = urwid.LineBox(w)
    loop = urwid.MainLoop(w, unhandled_input=handle_input)
    loop.run()

if __name__ == "__main__":
    main()

