+ [x] OBS Text(FreeType2) has a size limitation. It seems that if ticker size goes above a certain threshold, it does not display it in OBS.
    + __Its not specific to FreeType2. Any OBS source when rendered if crosses the width limit of 16380 its not rendered. This is irrespective of Video Output Resolution__
        + To check width in OBS, Right click > Transform > Edit Transform. Here you will find the size of any source.
    + Max-width of texttype2 depends on ~~font, font-size~~ OBS Source size. Max-width for current selection (Roboto,Mono,22) is 1260.
    + When the file is rewritten the start of the file moves if the length of text changes.
    + [ ] Windows supports TextGDI+ which is supposed to be different than freetype. Not available in Mac. To be checked on windows machine.
+ [x] Does changing font type affect the cpv and thereby cps?
    + cpv : characters per viewport.
            since size of viewport is fixed at X pixels and character size depends on font, YES it will affect.
    + cps : characters per second.
            text speed depends on OBS filter scroll speed which is pixel/second. Since character width depends on font it YES it will affect. 
+ [x] The width of all characters in a font is not the same. Calculate the no of blank space for a clean slate frame of ticker.
    ~~__Workaround: Use Monospace fonts.__ Currently using Roboto Mono.~~
    + Since switch time is being decided on pixel count any font can be chosen.
+ [x] Make file location fetching cross platform and location agnostic.
+ [ ] One feed will have different padding based on different tickers. One ticker can have multiple feeds.
+ [ ] How to define an attribute for the feed based on the ticker. I want to set the padding of feed based on ticker. But the same feed is used by another ticker it will overwrite the first ticker's padding. Since the Ticker class can't hold the state of a feed class without making it the attribute of ticker.
+ [x] The ticker restarts from the beginning when transitioned from a scene not having a ticker.  
    Run code on scene Transition  
    + [x] Start code when transitioning to scene with ticker
    + [x] Stop code when transitioning to scene without ticker  
    OR  
    + [ ] Add ticker to all scenes and hide where not required. Open OBS and main.py together.
+ [ ] Some parody headlines don't make sense without reading the article and getting the context. 
+ [x] ~~Make the Feed class take argument of url as input and the rest as **kw.~~ use parameter name wherever required.
+ [ ] Refine OOP.
    + [ ] Convert to staticmethod or classmethod wherever required.
+ [x] Calculate relation between text_speed and FONT and OBS_SCROLL_SPEED
    + text_speed (characters per second) = OBS_SCROLL_SPEED/FONT-WIDTH
+ [x] Find out ways to dynamically update feed text when the courtesy text or the separator text or the number of headlines change.
    + Changed structure of Feed and Feed text. 
    + Realised python takes Object arguments by reference and not by value i.e.
    ```python
    class A:
    def __init__(self):
        self.x = 12
        self.y = 24
        self.z = 32

    class B:
        def __init__(self,a:A):
            self.a = a
            self.b =13

    example_A = A()
    example_B = B(example_A)
    example_B.a.z=77
    print(example_A.z)#will return 77
    ```
+ [x] Automatically reset the feed text if it goes above the ticker max length.
+ [x] End the program gracefully.
+ [x] Add feedback to switch feed on receiving some kind of feedback from OBS.
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

+ [x] Add feeds to ticker concurrently.
    + 4x faster than sequential. Refer threadresult.txt

+ [x] We know when we switch from a non-ticker scene to a ticker scene, the ticker is refreshed i.e. The ticker starts from the beginning. Using websocket, we can identify when we switch from a non-ticker scene to a ticker scene and then run main.py.
    + [x] To be specific we build a ticker and wait. Then we switch scene and then start the ticker.
    + [x] When we switch to a non-ticker scene we must ~~kill main.py~~ stop ticker to be resumed later.
    + [ ] The TransitionBegin event isn't called while the program is within the while loop of ticker.start whereas it does work when its main.py sleep. How does it differentiates between different sleeps?
    + [x] Typically there is no need to switch from TheStart to any other scene more than once and its done only at the beginning. But eventually if a scene is added that doesn't have the ticker and to switch back to a ticker scene, the ticker must be restarted.
    + [x] Instead of checking scenes by name, check whether they contain the ticker or not. And the scene they are switching to has ticker or not. Based on that start or stop the ticker. Another check whether the ticker is rendered or not even if its present in a scene.
    + [x] Basically, add a stop feature in ticker. And when start is called again, restart the ticker.
    + [x] Instead of checking scenes by name, check whether they contain the ticker or not. And the scene they are switching to has ticker or not. Based on that start or stop the ticker.
    + [x] Basically, add a stop feature in ticker. And when start is called again, restart the ticker.
+ [x] Run main.py of master branch whenever obs is run.
    + ~~Achieved externally through Shortcuts app on Mac.~~
+ [ ] OBS allows to run python from its Scripts tool. Try to integrate this as a obsscript. [Details here](https://github.com/obsproject/obs-studio/wiki/Getting-Started-With-OBS-Scripting)
    + [ ] It lets you provide inputs via GUI component. It can be used to provide options. Some feasible options maybe:
        + [ ] Tickbox list of feed sources
        + [ ] Name and url prompt to add your own feed sources.
        + [ ] Slider to control scroll speed
        + [ ] Font selection
        + [ ] Checkbox of all scenes where to add the ticker
        + [ ] Time between 2 feeds
    + [ ] Also provides support for callback functions on events without websockets. To be integrated if feasible python-script possible.
    + [ ] It doesn't seem to support venv of Python3.9. The docs say in windows it supports 3.6. venv doesn't allow making environments of different versions.
        + Installing virtualenv which allows this feature but requires installation path to the version required, which means one has to install manually the version required.
        + [ ] '$ brew install python3.6' or @3.6/3.7 throws error. Installing .pkg from python.org.[This post](https://obsproject.com/forum/threads/python-scripts-on-mac.121235/post-462492) provides hint as to which installation folder path is to be provided. __This has not worked for me. I have replied to the author of the post. I have raised this query on the OBS discord server with no satisfactory answer.__ ___Pausing this for now___ [Continue here](https://github.com/obsproject/obs-studio/wiki/Scripting-Tutorial-Source-Shake) when solution found.
+ [x] Quit main.py when OBS is closed.
    + Add a hook to detect OBS exit.
    + Add a obs quit event and make it wait for hook. As the hook is activated, the event is set and main.py is closed.
+ [ ] When the transition isn't complete and we switch scene again, it raises an error and exits ticker.
+ [ ] Add logging to the project instead of using print statements.
+ [x] Import feed logo from feed website.
    + [x] Get image URL
    + [x] Download and ~~resize to 38x38~~ ~~OBS takes care of resizing.~~ but OBS doesn't care about alignment so standardizing size.
    + [x] Retain option to provide local file as feed logo
+ [ ] Feed Last updated date exception handling
+ [ ] Windows testing
    + [x] Replace FreeTypeText with TextGDI+
        + TextGDI+ also has an upper limit based on font size and file size. Now I understand the purpose of GDI and FreeType is to 'render' text to graphics so naturally they have to have a limit.
        + Emojis don't work when tested. 😀 gives 🖾 even in GDI+. It works only on one font Segoe UI Emoji but there the emojis are colorless and 🇮🇳 renders as IN.
    + [x] Install python and check obsscript  
        + When python installed path is provided the scripts are __working__. OBS-Script on the works for sure.
        + [ ] Change from websocket to intrisic implementation
    + [x] Exception handling for Pillow.Image.open() on windows. This is not expected to happen. There is no such error thrown on Mac.
        + Replacing ```except:``` with ```except Exception:``` does the trick.
+ [x] Kill orphan threads when starting and stopping ticker.
+ [ ] Add ticker OBS source dynamically and integrate with OBS source. Set its height width position based on OBS settings of resolution etc. Make all of this part of ticker class.
    + [ ] Set scroll speed multiple of single character length
    + Source settings and source properties both can be manipulated from the websocket.
    + GetTextFreetype2Properties and GetSourceSettings give the same results. Better to use GetSourceSettings for settings and GetSceneItemProperties to get properties.
    + Source width and height cannot be changed through SetSceneItemProperties. Use SetSceneItemTransform.
    + [ ] calculate switching time based on pixel count rather than character count.
    + [ ] Check if scene has Ticker Source. If not import from a JSON file.
    + [ ] If found, set the source settings (font,text etc.)
    + [ ] When switching ticker,update textfile and get the size of the rendered OBS source and calculate the switchToNextFeed time based on it.
    + [ ] Remove padding text. Add padding in terms of sleep.
+ [ ] Since image is already stored as a feed attribute why store it as a file as well? Instead write to container from feedLogo data.
+ [ ] Erratic values of single space width when ran. Expected value 13. The pixel widths of feeds incorrects as well
    ```
    (.venv) f&p@💻 parody-ticker %/Users/pani3610/code/parody-ticker/.venv/bin/python /Users/pani3610/code/parody-ticker/ticker.py
    Connected to OBS
    testing
    {'enabled': True, 'name': 'Scroll', 'settings': <extrafunctions.convertDictToObject.<locals>.Data object at 0x10284c9a0>, 'type': 'scroll_filter'}
    SSW 136.11
    THIS IS START
    The Betoota Advocate 13611
    The Onion 15470
    (.venv) f&p@💻 parody-ticker %/Users/pani3610/code/parody-ticker/.venv/bin/python /Users/pani3610/code/parody-ticker/ticker.py
    Connected to OBS
    testing
    {'enabled': True, 'name': 'Scroll', 'settings': <extrafunctions.convertDictToObject.<locals>.Data object at 0x102efbc70>, 'type': 'scroll_filter'}
    SSW 247.13
    THIS IS STAR
    ```
    + Tried resolving by splitting 
        ```
        value = self.obs.getVideoData().baseWidth
        ```

        into

        ```
        video_data = self.obs.getVideoData()
        value = video_data.baseWidth
        ```
        but error persists. Every run of program gives different values for different variables.
    + Adding sleep after file-writes is mitigating some errors.
    + [x] Try to get feedback from OBS when text updated.
        + Transform changes when tickertext sourcewidth is updated. Can be used to wait for file-write to complete.
        + The ```SceneItemTransformChanged``` event is triggered multiple times when tickertext updated once. Items other than tickertext are also _transformed_.
            + when tickertext updated; tickertext, white-bg, News-logo, ticker-tape, tickertext, TIcker-tape all are updated.
            + __tickertext updated twice__
            + Since parent is updated only once, it can be attached to update event.
                + [x] But if any other item is changed it will also trigger the parent.
                    + Added extra flag to check when text has to be updated.
            
            + Tests give 'Not match' when scene transitioned
    + [ ] SSW value now consistent and accurate but headlines count is still behaving erratic. Optimise reducing headline count