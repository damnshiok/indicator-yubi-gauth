#!/usr/bin/env python

##################################################
##						##
##    Yubikey for Google Authenticator          ##
##    by damnshiok 			        ##
##						##
##    Like this? Consider buying me a beer!     ##
##      					##
##    1GeGQciPbEPr2QoAJMZGGYNT2iYw1zKe4E	##
##						##
##################################################

import sys
import gtk
import appindicator
import time
import struct
import pynotify
import yubico

ICON = "/usr/share/pixmaps/yubikey-personalization-gui.png" #from yubikey-personalization-gui (yubico PPA)
SLOT = 2
STEP = 30
DIGITS = 6
TIME_CLEAR = 10 # number of seconds before clearing TOTP from clipboard 

pynotify.init("yubi-totp") #initialize pynotify

class yubikey_totp_indicator:

    def __init__(self):
        self.ind = appindicator.Indicator("yubi-totp", ICON, appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.menu_setup()
        self.ind.set_menu(self.menu)

#indicator menu
    def menu_setup(self):
        self.menu = gtk.Menu()

        self.get_totp_item = gtk.MenuItem("Get TOTP")
        self.get_totp_item.connect("activate", self.get_totp)
        self.get_totp_item.show()
        self.menu.append(self.get_totp_item)

        self.quit_item = gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)

    def get_totp(self, widget):		
        make_totp()

    def main(self):
        gtk.main()

    def quit(self, widget):
        gtk.main_quit()
        sys.exit(0)

def make_totp():   # adapted from Yubico

    try:
        YK = yubico.find_yubikey()
        print YK
        # Do challenge-response
        current_time = int(time.time())
        challenge = struct.pack("> Q", current_time / STEP).ljust(64, chr(0x0))
        print "Sending challenge : %s" % (challenge.encode('hex'))
	print "Press button if you configured your Yubikey Slot 2 to require user input."
        response = YK.challenge_response(challenge, slot=SLOT)
        print "Response received : %s" % (response.encode('hex'))
        # format with appropriate number of leading zeros
        fmt = "%." + str(DIGITS) + "i"
        totp_str = fmt % (yubico.yubico_util.hotp_truncate(response, length=DIGITS))
        print "Response formatted and truncated to %d digits: %s" % (DIGITS, totp_str)
        write_to_clipboard(totp_str)
        gtk.timeout_add(TIME_CLEAR * 1000, clear_totp)

    except yubico.yubico_exception.YubicoError, e:
        print "ERROR: %s" % (e.reason)
        notify_error = pynotify.Notification("Yubikey for Google Authenticator","ERROR: %s" % (e.reason), ICON)
        notify_error.show()
        return 1

    return 0

def write_to_clipboard(totp_str):
    clipboard = gtk.clipboard_get()
    clipboard.set_text(totp_str)
    clipboard.store()
    print "TOTP written to clipboard and will be cleared in %d seconds." % TIME_CLEAR
    notify_totp_written = pynotify.Notification("Yubikey for Google Authenticator", "TOTP written to clipboard and will be cleared in %d seconds" % TIME_CLEAR, ICON)
    notify_totp_written.show()

def clear_totp():
    clipboard = gtk.clipboard_get()
    clipboard.set_text("")
    clipboard.store()
    print "TOTP cleared from clipboard"
    notify_totp_cleared = pynotify.Notification("Yubikey for Google Authenticator", "TOTP cleared from clipboard", ICON)
    notify_totp_cleared.show()

if __name__ == "__main__":
    indicator = yubikey_totp_indicator()
    indicator.main()
