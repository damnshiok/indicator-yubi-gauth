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
* Might need yubi_goog.py from https://github.com/Ramblurr/yubi-goog
* Need some packages from Yubico, which you can install on Ubuntu by running these in the command line:

`sudo add-apt-repository ppa:yubico/stable`

`sudo apt-get update`

`sudo apt-get install yubikey-personalization-gui yubikey-personalization`

Note: You have to make the python scripts executable by running `chmod +x script.py`

Setup for use on Gmail, Mt. Gox or CampBX
-----------------------------------------
To set up 2-factor authentication at the following websites, you will need to generate a secret key.
* For Gmail, go to https://www.google.com/settings/security and click on "Settings" under "2-step verification", and then on "Android" under "Mobile application". Then click on "Can't scan the barcode?" to get your base32-encoded secret key. Go to step 1.
* For CampBX, go to "MY PROFILE", "EDIT PROFILE", re-enter your passwords, check "2-Factor with Google Authenticator", click "SAVE MY PROFILE". You should see the base32-encoded secret key. Go to step 1.
* For Mt. Gox, go to "Security Settings", click on "ADD NEW" under "Software Authenticators". You will see both a "Standard Private Key" and a "Secure Private Key". Use "Standard Private Key" as it is already in hex. You can skip step 1 and go straight to step 2.

1. We need to convert the secret key from base32 to hex. Run `./yubi_goog.py --convert-secret` from https://github.com/Ramblurr/yubi-goog. It will prompt you for your secret key in base32 and output a result in hex.
2. Run `yubikey-personalization-gui` to program your hex secret into your Yubikey as a HMAC-SHA1 challenge-response key. Take care to choose slot 2 so as not to overwrite slot 1 which normally contains your Yubicloud OTP configuration. Also, decide whether you want to have to "require user input". Enabling it is more secure. You can refer to this [Youtube video for a walkthrough][walkthrough]. 
3. Run `./indicator-yubi-gauth.py`. Click on indicator icon and select "Get OTP". If you enabled "require user input", touch your Yubikey. Your OTP will be pasted into the clipboard. Paste it into your webpage to complete the setup. The OTP will be cleared from the clipboard after 10 seconds for security purposes.

Features to be added
--------------------
* Toggle between paste to clipboard or active window
* Toggle to challenge slot 1 or 2 (currently set to 2)
* Toggle on/off notifications

[walkthrough]: http://www.youtube.com/watch?v=VDxJCkx7N4E
