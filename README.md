indicator-yubi-gauth
======================
by damnshiok@gmail.com

An Ubuntu indicator to use your Yubikey to generate OTPs like Google Authenticator, and sends Ubuntu notifcations when used.

This can be set up to use your Yubikey at any website that advertises 2 factor authetication via Google Authenticator. Aside from Gmail, examples described here are bitcoin exchanges Mt. Gox and CampBX.

If you find this useful, you are welcome to buy me a beer.
My bitcoin address is 1GeGQciPbEPr2QoAJMZGGYNT2iYw1zKe4E

Contains code from yubi-goog https://github.com/Ramblurr/yubi-goog
Released under ISC License.

Prerequisites
-------------
* Ubuntu >= 12.04 
* Yubikey >= 2.x
* Some packages from Yubico, which you can install on Ubuntu by running these in the command line:

`sudo add-apt-repository ppa:yubico/stable`
`sudo apt-get update`
`sudo apt-get install yubikey-personalization-gui yubikey-personalization`

Note: You have to make the python scripts executable by `chmod +x script.py`

Setup for use on Gmail, Mt. Gox or CampBX
-----------------------------------------
1. First you need to get your secret key.
1.1. For Gmail, go to https://www.google.com/settings/security and click on "Settings" under "2-step verification", and then on "Android" under "Mobile application". Then click on "Can't scan the barcode?" to get your base32-encoded secret key. Go to step 2.
1.2. For CampBX, go to "MY PROFILE", "EDIT PROFILE", re-enter your passwords, check "2-Factor with Google Authenticator", click "SAVE MY PROFILE". You should see the secret key. Go to step 2.
1.3. For Mt. Gox, go to "Security Settings", click on "ADD NEW" under "Software Authenticators". You will see both a "Standard Private Key" and a "Secure Private Key". The "Standard Private Key" is the right secret to use as it is already in hex. You can skip step 2 and go straight to step 3.

2. Run `yubi_goog.py --convert-secret` from https://github.com/Ramblurr/yubi-goog. It will prompt you for your base32-encoded secret and output a result in hex.
3. Run `yubikey-personalization-gui` to program your hex secret into your Yubikey as a HMAC-SHA1 challenge-response key. Take care to choose slot 2 so as not to overwrite slot 1 which normally contains your Yubicloud OTP configuration. Also, decide whether you want to have to "require user input". Enabling it is more secure. You can refer to this [Youtube video for a walkthrough][walkthrough]. 
4. Run `indicator-yubi-gauth.py`. Click on "Get OTP". If you enabled "require user input", touch your Yubikey. Your OTP will be pasted into the clipboard. Paste it into your webpage to complete the setup. The OTP will be clear from the clipboard after 10 seconds for security purposes.

Features to be added
--------------------
* Toggle between paste to clipboard or active window
* Toggle to challenge slot 1 or 2 (currently set to 2)
* Toggle on/off notifications

[walkthrough]: http://www.youtube.com/watch?v=VDxJCkx7N4E
