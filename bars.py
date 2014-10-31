#!/usr/bin/env python

import urwid
import logging as log
log.basicConfig(filename='/var/tmp/log', level=log.DEBUG, format='%(asctime)s %(message)s')
log.debug("~~~~~~~~~~~~~~~~~~~~~~~~")


palette = [
    ('normal', 'dark blue', 'dark gray'),
    ('inverse', 'dark gray', 'dark blue'),
]

def main():
    graph = urwid.BarGraph(
        ['normal', 'inverse'],
        ['normal', 'inverse'],
        { (1,0): 'normal', }, 
    )
    bardata = [(1,), (2,), (4,), (8,), (16,), (32,)]
    # lines = [2.0, 10.0]
    lines = [20, 10]
    graph.set_data(bardata, 40, lines)
    loop = urwid.MainLoop(graph, palette)
    loop.run()

if __name__ == "__main__":
    main = main()

