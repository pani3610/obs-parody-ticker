+ Ticker
    + SCREEN_SIZE (cpv)
    + SPEED (cps)
    + switchToNextFeed()
        + changeFeedText()
        + changeFeedImage()
    + SAVE_FILE
    + FONT_SIZE
    + EMPTY_TIME : Amount of time in secs we want to ticker to go blank in order to switch feeds
    + startFeed()
    
    + Feed
        + SOURCE_NAME
        + SOURCE_IMAGE
        + SOURCE_URL
        + SIZE: f(FeedText)
        + TIME_TO_CYCLE
        + calculateTimeToCycle(SIZE,SCREEN_SIZE,SPEED,EMPTY_TIME) -> Depends on parameters based off all 3 classes.
        + saveToFile()

        + FeedText (To be used only within Feed. Every feed will have only 1 feed text. Must be initialzied as soon as an instance of Feed is created)
            + HEADLINES_LIST f(Feed,NUMBER_OF_HEADLINES)
            + extractHeadlines()
            + SEPARATOR
            + PADDING
            + calculatePadding() : f(TIME_TO_CYCLE) -> Depends on Ticker
            + addPadding()
            + NUMBER_OF_HEADLINES
            + COURTESY_TEXT
            + raw_string
            
        

