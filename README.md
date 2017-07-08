﻿# FBTools

>FBTools allows you to access Facebook via command-line.

This project was made for learning purpose and is not maintained currently. It should work fine nonetheless. In case of any bug, please file an issue and I'll rectify it.

## Highlight
It does not use Facebook Graph API.
So a lot of features like fetching full friend list are now available.
And its blazing fast because it uses the mobile version.


## Current Features

* Check if someone unfriended you.
* Like all posts on a friend's timeline.
* Browse through your News Feed.
* Like any item in the feed.
* Comment on any item in the feed.
* Check your notifications.

### Upcoming Features

[None]

## Requirements

* Python3
* [PhantomJS 2.0.0](https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.0.0-windows.zip)
  * Steps for setting up PhantomJS on Windows:
    * Make a folder `C:\PhantomJS`
    * Copy the contents of `phantomjs-2.0.0-windows` folder to `C:\PhantomJS`
    * Add `C:\PhantomJS\bin\` to your PATH environment variable.
* Python packages required:
  * selenium (`pip install selenium`)
  * pyfiglet (`pip install pyfiglet`)
  * requests (`pip install requests`)

## Issue

Posts not in English are skipped in the news feed due to decoding issues when writing the feed in command prompt (windows). Output on Python3 IDLE works fine though.

## Screenshots

### Mainscreen
![FBTools](http://i.imgur.com/GsvnBk2.png)

### Autoliker
![FBTools](http://i.imgur.com/jvZDN8u.png)

Tested with Python 3.4.3 on Windows.

## License

MIT © [Ashish Chaudhary](http://tocttou.mit-license.org/)
