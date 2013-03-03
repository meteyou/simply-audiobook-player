Zero Button Audiobook Player
============================

This project is based on Raspberry Pi and hugely inspired by [The One Button Audiobook player]. I too have grandmother who is visually impaired and loves listening to audiobooks. Until now she has been doing this using old DVD player, which worked quite well, but that player does not save its state. So every time its turned off and back on it begins to play audiobook from the beginning.

So naturally this was a great opportunity for a Raspberry Pi project. However I went a little bit further and did not add any buttons at all. This audiobook player can be controlled using simple HTTP queries (mostly for debugging) or using NFC tag.

So the plan is to add some NFC tag stickers on empty DVD or CD cases. Actually anything might work which is quite bulky. So every NFC tag (or empty CD case in this case) references some audiobook in the internal player memory. When someone puts a tag over the player, it starts playing respective audiobook from its last state.

This player saves its state every couple of seconds. So whenever my grandmother gets bored of listening to it she can plug the player out of the mains socket. When the player is turned back on, it starts right from its last saved state.

I believe this has the smallest learning curve (if any). I will see what my grandmother thinks of it after couple of months using it.

How it came about
=================

This is my first Raspberry Pi project. So here I will try to enumerate every step that I took to make this project be.

Hardware
--------

I got a Raspberry Pi for this project from [ModMyPi]. I also bought a case, SD to microSD card adapter and HDMI to DVI adapter from there.

It took some time to locate a suitable NFC reader. It had to be quite small so it fitted RPi case. I chose [PN532 NFC RFID module kit] which I saw mentioned in couple of SIB Vision blog posts.

Firstly a blog post titled [NFC/RFID for Beagleboard xm with Java] helped me to change NFC module protocol from default _I2C_ to _HSU_ (or _UART_). Secondly, another post [NFC Reader with RaspberryPi GPIO] mentioned everything I needed to know to successfully connect this NFC module to Raspberry Pi.

So I unsoldered 0 Ohm resistor from _bit 1 of HIS0 pin_ and then shortened _bit 0 of HIS0 pin_, which was harder than it sounds because of my gigantic solder. Next I tweaked those mentioned config files and connected NFC module to RPi. It was that easy. I had some problems installing _libnfc_ but more on that later.

Software
--------

I chose to use Python for this project, which comes already in a [Rasbian Weezy] which I installed into microSD card and successfully booted RPi for the first time.

I am quite limited in some parts of working in Linux. For example I was not quite sure how to configure network on Raspberry Pi. This is what helped me to [Share Internet Connection with Linux] from my Windows PC.

For music playing part I installed [MPD] using a tutorial from [here][Installing MPD] and [Python MPD2]. I had some problems with this. Mainly some commands (_seek_ for example) in Python did not work. I believe the problem was caused because _apt-get_ installed _0.16.0_ version of MPD and Python MPD2 already bumped its support to _MPD_ version _0.17.0_ which maybe broke some backwards compatibility.

There are couple of distinctive logical modules in this project:

* audio file player;
* state saver;
* web interface;
* nfc interface.

All of these need to interchange messages when some event occurs. I figured [Actor Model] should work here quite well and installed [Pykka] which is a python implementation of actor model. I am quite new (self taught and worked only on toy projects) to actors, so I am not sure if I used Pykka in a best way. However my code seems to work and it is not very ugly.

NFC part of this project is handled by the open source [libnfc]. To install (compile) this library first I followed an article from Adafruit on [NFC on Raspberry Pi]. However that article is a little bit outdated and _libnfc_ has to be installed a little bit differently from version _1.7.0_. As members of libnfc forum pointed out [here][libnfc forum post] and [here][libnfc forum post #2] before compilation libnfc must be configured with only one parameter. ```./configure --with-drivers=pn532_uart``` Then after ```sudo make install``` a configuration file for Raspberry Pi must be copied to a directory which is checked by libnfc on startup. ```sudo cp contrib/libnfc/pn532_uart_on_rpi.conf.sample /usr/local/etc/nfc/devices.d/pn532_uart_on_rpi.conf``` Make sure to create target directory before issuing this command. After these steps a set of commands can be used to debug or check whether libnfc works as expected.

* ```LIBNFC_LOG_LEVEL=3 nfc-list``` Enabling debug with environment variable is helpful to determine which directories libnfc is scanning for configuration files.
* ```nfc-scan-device -i -v``` Will list all devices detected by libnfc.
* ```nfc-poll``` Will listen for any NFC tags for 30 seconds and will print tag information if it detects any.

That is pretty much it. All of these parts combined make a pretty neat Zero Button Audiobook Player. :)

Software Architecture
=====================

Here I will list logical modules of the software and their relations.

[The One Button Audiobook player]: http://blogs.fsfe.org/clemens/2012/10/30/the-one-button-audiobook-player/
[ModMyPi]: https://www.modmypi.com/
[PN532 NFC RFID module kit]: http://www.elechouse.com/elechouse/index.php?main_page=product_info&cPath=90_93&products_id=2205
[NFC/RFID for Beagleboard xm with Java]: http://blog.sibvisions.com/2012/11/26/nfcrfid-for-beagleboard-xm-with-java/
[NFC Reader with RaspberryPi GPIO]: http://blog.sibvisions.com/2013/01/04/nfc-reader-with-raspberrypi-gpio/
[Rasbian Weezy]: http://www.raspberrypi.org/downloads
[Share Internet Connection with Linux]: http://blog.creativeitp.com/posts-and-articles/windows/share-windows-internet-connection-with-linux/comment-page-1/
[MPD]: http://mpd.wikia.com/wiki/Music_Player_Daemon_Wiki
[Installing MPD]: http://crunchbang.org/forums/viewtopic.php?id=4686
[Python MPD2]: https://github.com/Mic92/python-mpd2
[Actor Model]: http://en.wikipedia.org/wiki/Actor_model
[Pykka]: https://github.com/jodal/pykka
[libnfc]: https://code.google.com/p/libnfc/
[NFC on Raspberry Pi]: http://learn.adafruit.com/adafruit-nfc-rfid-on-raspberry-pi/overview
[libnfc forum post]: http://www.libnfc.org/community/topic/924/no-nfc-device-when-using-libnfc-170-rc5-on-raspberry-pi/
[libnfc forum post #2]: http://www.libnfc.org/community/topic/913/no-nfc-device-found-with-libnfc170rc4-on-raspberry-pi/