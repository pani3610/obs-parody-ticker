# About Parody Ticker Tape

<img src="https://github.com/pani3610/obs-parody-ticker/blob/master/readme_resource/ticker.gif" width="600"> 

This is a small project to create a news ticker-tape at the bottom of video streams. The news items are imported from the RSS feeds of various parody news websites. ***Come to think of it, any news feed can be added in this ticker.*** This project modifies and controls the elements of the ticker with a GUI interface.  


<img src="https://github.com/pani3610/obs-parody-ticker/blob/master/readme_resource/GUI.png" width="400"> 


List of known issues and TODO can be found in [issues.md](https://github.com/pani3610/obs-parody-ticker/blob/master/issues.md)

## Pre-requisites
+ Written in Python 3.9.12
+ Mac(non-OBS script) : The following packages/librarires/binaries needs to be installed before running the program:  
    + obswebsocket
    + tkinter
    + Python libraries listed in requirements.txt
## [main.py](https://github.com/pani3610/obs-parody-ticker/blob/master/main.py)
+ Run main.py to launch the program.
## [ticker.py](https://github.com/pani3610/obs-parody-ticker/blob/master/ticker.py)
+ Contains details about the Ticker class.
+ This file creates the ticker text and stores in a text file. This text file is set as the source for the OBS Text(FreeType 2). This text has a filter of horizontal scroll which gives it the effect of ticker.
+ This file also updates the image of the news source. 
+ This file switches the ticker through multiple feeds depending on the size of the feeds.

## [feed.py](https://github.com/pani3610/obs-parody-ticker/blob/master/feed.py)
+ Contains details about the Feed and associated classes.  

## [gui.py](https://github.com/pani3610/obs-parody-ticker/blob/master/gui.py)
+ Responsible for the GUI component to take user input before creating ticker in OBS.
+ GUI is created on top of tkinter.


## [graphics.py](https://github.com/pani3610/obs-parody-ticker/blob/master/graphics.py)
+ Responsible for the background graphics of the ticker.  
+ Graphics are created using HTML/CSS are converted into PNG files.