# About Parody Ticker Tape

<img src="https://github.com/pani3610/obs-parody-ticker/blob/master/readme_resource/ticker.gif" width="400">
This is a small project to create a news ticker-tape at the bottom of video streams. The news items are imported from the RSS feeds of various parody news websites. This project modifies and controls the elements of the ticker.  

Come to think of it, any news feed can be added in this ticker.  

List of known issues and TODO can be found in [issues.md](https://github.com/pani3610/obs-parody-ticker/blob/master/issues.md)

## Pre-requisites
+ Mac(non-OBS script) : The following packages/librarires/binaries needs to be installed before running the program:  
    + obswebsocket
    + tkinter
    + Python libraries listed in requirements.txt
## [main.py](https://github.com/pani3610/obs-parody-ticker/blob/master/main.py)
+ This file creates the ticker text and stores in a text file. This text file is set as the source for the OBS Text(FreeType 2). This text has a filter of horizontal scroll which gives it the effect of ticker.
+ This file also updates the image of the news source. Since all the rss feeds do not provide the logo of the source, these have been resized (400x400) and stored locally.
+ This file switches the ticker through multiple feeds depending on the size of the feeds.
+ Run main.py with [obs websocket](https://github.com/obsproject/obs-websocket) running. Whenever scene is transitioned:  
    + from non-ticker scene to ticker scene -> ticker is (re)started.
    + from ticker-scene to non-ticker scene -> ticker is paused.

## [ticker.py](https://github.com/pani3610/obs-parody-ticker/blob/master/ticker.py)
+ Contains details about the Ticker class.

## [feed.py](https://github.com/pani3610/obs-parody-ticker/blob/master/feed.py)
+ Contains details about the Feed and FeedText class.