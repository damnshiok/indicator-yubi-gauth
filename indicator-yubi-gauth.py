#!/usr/bin/env python

##################################################
##
##    Indicator for Yubikey Google Authenticator
##
##    by damnshiok@gmail.com
##    with adapted code from Casey Link
##
##    Like this? Consider buying me a beer!
##
##    1GeGQciPbEPr2QoAJMZGGYNT2iYw1zKe4E
##
##################################################

import sys
import gtk
import appindicator
import binascii
import time
import subprocess
import struct
import pynotify

#icon from yubikey-personalization-gui (from yubico PPA)
ICON = "/usr/share/pixmaps/yubikey-personalization-gui.png" 
TIME_STEP = 30 # default as per TOTP spec
TIME_CLEAR = 10 # number of seconds before clearing OTP from clipboard

#check for python 3
IS_PY3 = sys.version_info[0] == 3

#initialize pynotify
pynotify.init("yubi-gauth")

class YubiIndicator:

    def __init__(self):
        self.ind = appindicator.Indicator("yubi-gauth", ICON, appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.menu_setup()
        self.ind.set_menu(self.menu)

#indicator menu
    def menu_setup(self):
        self.menu = gtk.Menu()

        self.yubi_item = gtk.MenuItem("Get OTP")
        self.yubi_item.connect("activate", self.YUBI)
        self.yubi_item.show()
        self.menu.append(self.yubi_item)

        self.quit_item = gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)

    def YUBI(self, widget):		
        yubi()

    def main(self):
        gtk.main()

    def quit(self, widget):
        gtk.main_quit()
        sys.exit(0)

#next 3 functions are adapted from Casey Link
def mangle_hash(h):
    if IS_PY3:
        offset = h[-1] & 0x0F
    else:
        offset = ord(h[-1]) & 0x0F
    truncated_hash = h[offset:offset+4]
   
    code = struct.unpack(">L", truncated_hash)[0]
    code &= 0x7FFFFFFF;
    code %= 1000000;
    
    return '{0:06d}'.format(code)
    
def generate_challenges():
    challenges = []
    t = int(time.time())
    tm = t/TIME_STEP
    tm = struct.pack('>q', int(tm))
    challenges.append(tm)
    return challenges
 
def yubi():
    print("Challenge sent to Yubikey")
    n_challenge = pynotify.Notification("Yubikey for Google Authenticator", "Challenge sent to Yubikey", ICON)
    n_challenge.set_timeout(500) #500ms
    n_challenge.show()
    for chal in generate_challenges():
        chal = binascii.hexlify(chal)
        cmd = ['ykchalresp']
        cmd.append('-2x')
        cmd.append(chal)
        if hasattr(subprocess, "check_output"):
            resp = subprocess.check_output(cmd).strip()
        else:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            out, err = proc.communicate()
            if not isinstance(out, basestring):
                raise ValueError("Command {0} returned {1!r}."
                                 .format(" ".join(cmd), out))
            resp = out.strip()
        clipboard = gtk.clipboard_get()
        clipboard.set_text("%s" %(mangle_hash(binascii.unhexlify(resp))))
        clipboard.store()
        print("OTP pasted to clipboard")
        n_received = pynotify.Notification("Yubikey for Google Authenticator", "OTP pasted to clipboard", ICON)
        n_received.show()
        gtk.timeout_add(TIME_CLEAR * 1000, clear_otp)

def clear_otp():
    clipboard = gtk.clipboard_get()
    clipboard.set_text("")
    clipboard.store()
    print("OTP cleared from clipboard")
    n_cleared = pynotify.Notification("Yubikey for Google Authenticator", "OTP cleared from clipboard", ICON)
    n_cleared.show()

if __name__ == "__main__":
    indicator = YubiIndicator()
    indicator.main()
