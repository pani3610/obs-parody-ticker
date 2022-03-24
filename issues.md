+ [ ] OBS Text(FreeType2) has a size limitation. It seems that if ticker size goes above a certain threshold, it does not display it in OBS.
    + Max-width of texttype2 depends on font, font-size. Max-width for current selection (Roboto,Mono,22) is 1260.
    + When the file is rewritten the start of the file moves if the length of text changes.
+ [ ] Does changing font type affect the cpv and thereby cps?
+ [x] The width of all characters in a font is not the same. Calculate the no of blank space for a clean slate frame of ticker.
    __Workaround: Use Monospace fonts.__ Currently using Roboto Mono.
+ [x] Make file location fetching cross platform and location agnostic.
+ [ ] One feed will have different padding based on different tickers. One ticker can have multiple feeds.
+ [ ] How to define an attribute for the feed based on the ticker. I want to set the padding of feed based on ticker. But the same feed is used by another ticker it will overwrite the first ticker's padding. Since the Ticker class can't hold the state of a feed class without making it the attribute of ticker.
+ [ ] The ticker restarts from the beginning when transitioned from a scene not having a ticker.  
    Run code on scene Transition  
    + [ ] Start code when transitioning to scene with ticker
    + [ ] Stop code when transitioning to scene without ticker  
    OR  
    + [ ] Add ticker to all scenes and hide where not required. Open OBS and main.py together.
+ [ ] Some parody headlines don't make sense without reading the article and getting the context. 
+ [x] ~~Make the Feed class take argument of url as input and the rest as **kw.~~ use parameter name wherever required.
+ [ ] Refine OOP.
+ [ ] Calculate relation between text_speed and FONT and OBS_SCROLL_SPEED
+ [ ] Find out ways to dynamically update feed text when the courtesy text or the separator text or the number of headlines change.
+ [x] Automatically reset the feed text if it goes above the ticker max length.
+ [ ] End the program gracefully.
+ [ ] Add feedback to switch feed on receiving some kind of feedback from OBS.
    + [ ] CV2 OBS Virtual Cam approach:
        + [ ] Reduce video input processed so as to actually reduce processing work.  
            + [ ] Reduce fps
            + [ ] Reduce resolution
            + [ ] make grayscale
+ [x] Optimise performance.
    + Python is slow. But there surely is scope for optimisation.
    + Using timeit to measure the execution time shows the main.py takes around 2 seconds to run on average.
    + exectime.py creates a report to diagnose the per function call performance. Run the following after executing exectime.py
        ```bash
        snakeviz ./filename.prof
        ```
    + __Analyzing the data shows that over 95% execution time is for the http calls to retrieve rss feeds which is executed by the library. Not much scope of improvement in user-written code.__

+ [ ] If execution time cannot be predicted correctly, atleast it can be made consistent by ensuring the code executes exactly at let say 7 seconds by padding the program execution time.

+ [ ] We know when we switch from a non-ticker scene to a ticker scene, the ticker is refreshed i.e. The ticker starts from the beginning. Using websocket, we can identify when we switch from a non-ticker scene to a ticker scene and then run main.py.
    + [ ] To be specific we build a ticker and wait. Then we switch scene and then start the ticker.
    + [ ] When we switch to a non-ticker scene we must kill main.py
    + [ ] The TransitionBegin event isn't called while the program is within the while loop of ticker.start whereas it does work when its main.py sleep. How does it differentiates between different sleeps?
    + [ ] Typically there is no need to switch from TheStart to any other scene more than once and its done only at the beginning. But eventually if a scene is added that doesn't have the ticker and to switch back to a ticker scene, the ticker must be restarted.
    + [ ] Instead of checking scenes by name, check whether they contain the ticker or not. And the scene they are switching to has ticker or not. Based on that start or stop the ticker.
    + [ ] Basically, add a stop feature in ticker. And when start is called again, restart the ticker.
 