import time
from gi.repository import GLib

# This line disables KeyboardInterrupt exception
loop = GLib.MainLoop()

print "Press ctrl-c"
time.sleep(60)
print "sleep finished"

